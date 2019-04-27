from django import forms
from .models import OrderType, Order
import string


class AddOrderForm(forms.Form):
    cable_number = forms.CharField(max_length=32)
    appointed_date = forms.DateField()
    appointed_time = forms.TimeField()

    remark = forms.CharField(max_length=2048, required=False)

    order_type = forms.IntegerField()

    def clean_cable_number(self):
        cable = self.cleaned_data['cable_number']
        for c in cable:
            if c not in string.digits:
                self.add_error('cable_number', 'Должны быть только цифры')
                return cable
        if Order.objects.filter(cable_number=cable).exists():
            self.add_error('cable_number', 'Заявка с таким номером кабеля уже есть')
        return cable

    def clean_order_type(self):
        order_type = self.cleaned_data['order_type']

        if not OrderType.objects.filter(id=order_type).exists():
            self.add_error('order_type', 'Неверный тип заказа')
        return order_type

class ClientForm(forms.Form):
    first_name = forms.CharField(max_length=128)
    last_name = forms.CharField(max_length=128)
    surname = forms.CharField(max_length=128)
    phone = forms.CharField(max_length=11)
    email = forms.EmailField(required=False)
    address = forms.CharField(max_length=2048)

    def clean_first_name(self):
        f_name = self.cleaned_data['first_name']
        if len(f_name) < 2:
            self.add_error('first_name', 'Не менее 2 символов')
        elif self.forbidden_sym(f_name):
            self.add_error('first_name', 'Недопустимый символ в имени')
        return f_name

    def clean_last_name(self):
        l_name = self.cleaned_data['last_name']
        if len(l_name) < 2:
            self.add_error('last_name', 'Не менее 2 символов')
        elif self.forbidden_sym(l_name):
            self.add_error('last_name', 'Недопустимый символ в фамилии')
        return l_name

    def clean_surname(self):
        surname = self.cleaned_data['surname']
        if len(surname) < 2:
            self.add_error('surname', 'Не менее 2 символов')
        elif self.forbidden_sym(surname):
            self.add_error('surname', 'Недопустимый символ в фамилии')
        return surname

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if len(phone) != 11:
            self.add_error('phone', 'Должно быть 11 цифр')
        for c in phone:
            if c not in string.digits:
                self.add_error('phone', 'Должно быть 11 цифр')
                break
        return phone

    def clean_address(self):
        uncorr_sym = '!@#$%^&*():;/|\\+=`~'
        address = self.cleaned_data['address']
        for c in address:
            if c in uncorr_sym:
                self.add_error('address', 'Недопустимый символ')
                break
        return address

    def forbidden_sym(self, value):
        forb_sym = ';: '
        for char in forb_sym:
            if char in value:
                return True
        return False

