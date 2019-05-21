from django.shortcuts import render, redirect
from .forms import *
from .models import *
from datetime import datetime
from django.http import Http404
from django.utils import timezone
from django.db.models import Q
import googlemaps, os
from TehPro.settings import BASE_DIR


def staff_add(request):
    data = {}
    data['form_type'] = 'add'
    data['order_types'] = OrderType.objects.all()
    data['cities'] = City.objects.all()
    data['groups'] = Group.objects.all()

    if request.method == 'POST':
        form_order = AddOrderForm(request.POST)
        form_client = ClientForm(request.POST)
        if form_order.is_valid() and form_client.is_valid():

            client = form_client.save()

            dt = datetime.combine(form_order.cleaned_data['appointed_date'], form_order.cleaned_data['appointed_time'])
            used_materials = UsedMaterials.objects.create()

            order = Order.objects.create(cable_number=form_order.cleaned_data['cable_number'],
                                         appointed_time=dt,
                                         client=client,
                                         materials=used_materials,
                                         order_type=OrderType.objects.get(id=form_order.cleaned_data['order_type']))
            group = form_order.cleaned_data['group']
            if group:
                order.group = Group.objects.get(id=group)
                for worker in order.group.extuser_set:
                    order.workers.add(worker)
            order.remark = form_order.cleaned_data['remark']
            order.save()

            request.session['order_added'] = True
            return redirect('/order/list/')
        return render(request, 'Order/StaffOrderForm.html', {'form_order': form_order, 'form_client': form_client})
    return render(request, 'Order/StaffOrderForm.html', data)


def staff_change(request, id):
    data = {}
    data['form_type'] = 'change'
    data['order_types'] = OrderType.objects.all()
    data['cities'] = City.objects.all()
    data['groups'] = Group.objects.all()
    order = Order.objects.filter(id=id).first()
    if order:
        if request.method == 'POST':
            client = order.client
            form_order = ChangeOrderForm(request.POST)
            form_client = ClientForm(request.POST, instance=client)
            if form_order.is_valid() and form_client.is_valid():

                dt = datetime.combine(form_order.cleaned_data['appointed_date'], form_order.cleaned_data['appointed_time']).astimezone()
                order.cable_number = form_order.cleaned_data['cable_number']
                order.appointed_time = dt
                group = form_order.cleaned_data['group']
                if group:
                    order.group = Group.objects.get(id=group)

                order.remark = form_order.cleaned_data['remark']
                order.order_type = OrderType.objects.get(id=form_order.cleaned_data['order_type'])
                order.save()
                form_client.save()
                request.session['order_changed'] = True
                return redirect('/order/list/')
            return render(request, 'Order/StaffOrderForm.html', {'form_order': form_order, 'form_client': form_client})
        order = Order.objects.get(id=id)
        group_id = None
        if order.group:
            group_id = order.group.id
        form_order = ChangeOrderForm(initial={'id': id, 'appointed_time': order.appointed_time.astimezone().time(),
                                              'appointed_date': order.appointed_time.astimezone().date(),
                                              'order_type': order.order_type.id,
                                              'group': group_id,
                                              'cable_number': order.cable_number,
                                              'remark': order.remark})
        client = order.client
        form_client = ClientForm(instance=client)
        data['form_order'] = form_order
        data['form_client'] = form_client
        return render(request, 'Order/StaffOrderForm.html', data)
    raise Http404

def orders_list(request):
    order_list = Order.objects.all()
    order_list = order_list.order_by('appointed_time')
    return render(request, 'Order/OrdersList.html', {'order_list': order_list})

def worker_orders(request):
    user = request.user
    group = user.extuser.group
    order_list = Order.objects.filter(Q(group=group) | Q(workers=user)).distinct()
    order_list = order_list.order_by('appointed_time')
    return render(request, 'Order/OrdersList.html', {'order_list': order_list, 'worker_list': True})

#order form for worker
def worker_order(request, id):
    data = {}
    data['work_types'] = WorkType.objects.all()
    order = Order.objects.filter(id=id).first()
    if order:
        data['order'] = order
        if request.method == 'POST':
                materials = order.materials
                form_order = OrderForWorkerForm(request.POST, instance=order)
                form_mat = MaterialsForm(request.POST, instance=materials)
                is_complete = order.is_complete


                #запоминаем текущие значения материалов
                current_mt = {}
                current_mt['plug'] = materials.plug
                current_mt['cable'] = materials.cable
                current_mt['rosette'] = materials.rosette
                current_mt['connector'] = materials.connector

                if form_order.is_valid() and form_mat.is_valid():
                    order.work_type.clear()
                    ts = timezone.datetime.combine(form_order.cleaned_data['date_start'], form_order.cleaned_data['time_start'])#.astimezone()
                    te = timezone.datetime.combine(form_order.cleaned_data['date_end'], form_order.cleaned_data['time_end'])
                    order.time_start = ts
                    order.time_end = te

                    for work_type in form_order.cleaned_data['work_type']:
                        order.work_type.add(work_type)
                    order.is_complete = is_complete
                    if not order.is_complete:
                        if form_order.cleaned_data['is_complete'] and order.group:
                            order.is_complete = True
                            order.workers.clear()
                            for worker in order.group.extuser_set.all():
                                order.workers.add(worker.user)
                    order.save()
                    form_mat.save()

                    #вычитаем разницу материалов из материалов группы
                    group = order.group
                    group.plug = max(0, group.plug - (materials.plug - current_mt['plug']))
                    group.cable = max(0, group.cable - (materials.cable - current_mt['cable']))
                    group.connector = max(0, group.plug - (materials.connector - current_mt['connector']))
                    group.rosette = max(0, group.rosette - (materials.rosette - current_mt['rosette']))
                    group.save()

                    request.session['order_saved'] = True
                    return redirect('/order/worker/list/')
                data['form_order'] = form_order
                data['form_mat'] = form_mat
                return render(request, 'Order/WorkerOrderForm.html', data)
        order = Order.objects.get(id=id)
        datetimes = {}
        if order.time_start:
            datetimes['time_start'] = order.time_start.astimezone().time()
            datetimes['date_start'] = order.time_start.astimezone().date()
        else:
            datetimes['time_start'] = None
            datetimes['date_start'] = None
        if order.time_end:
            datetimes['time_end'] = order.time_end.astimezone().time()
            datetimes['date_end'] = order.time_end.astimezone().date()
        else:
            datetimes['time_end'] = None
            datetimes['date_end'] = None
        data['form_order'] = OrderForWorkerForm(instance=order, initial=datetimes)
        data['form_mat'] = MaterialsForm(instance=order.materials)
        return render(request, 'Order/WorkerOrderForm.html', data)
    raise Http404


def order_full(request, id):
    order = Order.objects.filter(id=id).first()
    if order and request.user.is_staff:
        data = {}
        data['order'] = order
        return render(request, 'Order/OrderFull.html', data)
    raise Http404

def get_distance_matrix(request):
    with open(os.path.join(BASE_DIR, 'api_key.txt')) as f:
        api_key = f.readline().strip()
    client = googlemaps.Client(api_key)

    origins = ['Биробиджан, пер.Угольный 4', 'Биробиджан, Советская 64', 'Биробиджан, Осенняя 13а']

    matrix = client.distance_matrix(origins, origins, language="ru-RU")

    dst_matrix = {}
    dst_matrix['orders'] = []
    dst_matrix['matrix'] = [[{}]*len(origins)]*len(origins)

    for i, row in enumerate(matrix['rows']):
        for j, col in enumerate(row['elements']):
            dst_matrix['matrix'][i][j]['distance'] = col['distance']['value']
            dst_matrix['matrix'][i][j]['duration'] = col['duration']['value']
            print('{0}-{1}: dist = {2}, dur = {3}'.format(i, j, col['distance']['value'], col['duration']['value']))

    return render(request, 'Main/Index.html')


def division_of_orders(request):
    data = {}
    data['groups'] = Group.objects.all()

    if request.method == 'POST':
        groups = request.POST['groups']
        return render(request, 'Order/DivisionResult.html', data)
    return render(request, 'Order/DivisionOfOrder.html', data)
