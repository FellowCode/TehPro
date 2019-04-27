from django.shortcuts import render, redirect
from .forms import *
from .models import *
from datetime import datetime


def staff_add(request):
    data = {}
    data['form_type'] = 'add'
    data['order_types'] = []
    for order_type in OrderType.objects.all():
        data['order_types'].append({'id': order_type.id, 'name': order_type.name})
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
            order.remark = form_order.cleaned_data['remark']
            order.save()

            data['order_added'] = True
            return render(request, 'Order/StaffOrderForm.html', data)
        return render(request, 'Order/StaffOrderForm.html', {'form_order': form_order, 'form_client': form_client})
    return render(request, 'Order/StaffOrderForm.html', data)


def staff_change(request, id):
    data = {}
    data['form_type'] = 'change'
    data['order_types'] = []
    for order_type in OrderType.objects.all():
        data['order_types'].append({'id': order_type.id, 'name': order_type.name})
    if request.method == 'POST':
        form_order = ChangeOrderForm(request.POST)
        form_client = ClientForm(request.POST)
        if form_order.is_valid() and form_client.is_valid():
            order = Order.objects.get(id=id)
            dt = datetime.combine(form_order.cleaned_data['appointed_date'], form_order.cleaned_data['appointed_time'])
            order.cable_number = form_order.cleaned_data['cable_number']
            order.appointed_time = dt
            order.remark = form_order.cleaned_data['remark']
            order.order_type = OrderType.objects.get(id=form_order.cleaned_data['order_type'])
            order.save()

            client = order.client
            client.first_name = form_client.cleaned_data['first_name']
            client.last_name = form_client.cleaned_data['last_name']
            client.surname = form_client.cleaned_data['surname']
            client.phone = form_client.cleaned_data['phone']
            client.email = form_client.cleaned_data['email']
            client.address = form_client.cleaned_data['address']
            client.save()
            data['order_changed'] = True
            return render(request, 'Order/StaffOrderForm.html', data)
        return render(request, 'Order/StaffOrderForm.html', {'form_order': form_order, 'form_client': form_client})
    order = Order.objects.get(id=id)
    form_order = ChangeOrderForm(initial={'id': id, 'appointed_time': order.appointed_time.time(),
                                          'appointed_date': order.appointed_time.date(),
                                          'order_type': order.order_type.id,
                                          'cable_number': order.cable_number,
                                          'remark': order.remark})
    client = order.client
    form_client = ClientForm(initial={'first_name': client.first_name,
                                      'last_name': client.last_name,
                                      'surname': client.surname,
                                      'email': client.email,
                                      'phone': client.phone,
                                      'address': client.address})
    data['form_order'] = form_order
    data['form_client'] = form_client
    return render(request, 'Order/StaffOrderForm.html', data)


def user_orders(request):
    user = request.user
    order_list = Order.objects.filter(workers=user)

    return render(request, 'Order/WorkerOrders.html', {'order_list': order_list})
