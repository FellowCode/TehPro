from django.shortcuts import render, redirect
from .forms import *
from . models import *
from datetime import datetime

def add(request):
    data = {}
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
            return render(request, 'Order/Add.html', data)
        return render(request, 'Order/Add.html', {'form_order': form_order, 'form_client': form_client})
    return render(request, 'Order/Add.html', data)

def user_orders(request):
    user = request.user
    order_list = Order.objects.filter(workers=user)

    return render(request, 'Order/User_orders.html', {'order_list': order_list})
