from django.shortcuts import render, redirect
from .forms import *
from .models import *
from datetime import datetime
from django.http import Http404
from django.utils import timezone


def staff_add(request):
    data = {}
    data['form_type'] = 'add'
    data['order_types'] = OrderType.objects.all()
    data['groups'] = Group.objects.all()

    if request.method == 'POST':
        form_order = AddOrderForm(request.POST)
        form_client = ClientForm(request.POST)
        if form_order.is_valid() and form_client.is_valid():
            client = Client.objects.create()
            client.first_name = form_client.cleaned_data['first_name']
            client.last_name = form_client.cleaned_data['last_name']
            client.surname = form_client.cleaned_data['surname']
            client.phone = form_client.cleaned_data['phone']
            client.email = form_client.cleaned_data['email']
            client.address = form_client.cleaned_data['address']
            client.save()

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
                for worker in order.group.user_set:
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
        form_order = ChangeOrderForm(initial={'id': id, 'appointed_time': order.appointed_time.astimezone().time(),
                                              'appointed_date': order.appointed_time.astimezone().date(),
                                              'order_type': order.order_type.id,
                                              'group': order.group.id,
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

    return render(request, 'Order/OrdersList.html', {'order_list': order_list})

def worker_orders(request):
    user = request.user
    order_list = Order.objects.filter(workers=user)

    return render(request, 'Order/WorkerOrders.html', {'order_list': order_list})

#order form for worker
def worker_order(request, id):
    data = {}
    data['work_types'] = WorkType.objects.all()
    order = Order.objects.filter(id=id).first()
    if order:
        if request.method == 'POST':
                materials = order.materials
                form_order = OrderForWorkerForm(request.POST, instance=order)
                form_mat = MaterialsForm(request.POST, instance=materials)
                is_complete = order.is_complete
                if form_order.is_valid() and form_mat.is_valid():
                    order.work_type.clear()
                    ts = datetime.combine(form_order.cleaned_data['date_start'], form_order.cleaned_data['time_start']).astimezone()
                    te = timezone.datetime.combine(form_order.cleaned_data['date_end'], form_order.cleaned_data['time_end']).astimezone()
                    order.time_start = ts
                    order.time_end = te

                    for work_type in form_order.cleaned_data['work_type']:
                        order.work_type.add(work_type)
                    order.is_complete = is_complete
                    if not order.is_complete:
                        if form_order.cleaned_data['is_complete'] and order.group:
                            order.is_complete = True
                            order.workers.clear()
                            for worker in order.group.user_set:
                                order.workers.add(worker)
                    order.save()
                    form_mat.save()

                    request.session['order_saved'] = True
                    return redirect('/order/worker/list/')
                data['form_order'] = form_order
                data['form_mat'] = form_mat
                return render(request, 'Order/WorkerOrderForm.html', data)
        order = Order.objects.get(id=id)
        data['form_order'] = OrderForWorkerForm(instance=order, initial={'time_start': order.time_start.astimezone().time(),
                                                                         'date_start': order.time_start.astimezone().date(),
                                                                         'time_end': order.time_end.astimezone().time(),
                                                                         'date_end': order.time_end.astimezone().date()})
        data['form_mat'] = MaterialsForm(instance=order.materials)
        return render(request, 'Order/WorkerOrderForm.html', data)
    raise Http404

