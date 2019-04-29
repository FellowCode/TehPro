from django import forms
from django.contrib.auth.models import User
import string

from django.core.exceptions import ValidationError
from django.forms import ModelForm

class SignInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # if you want to do it to all of them
        for field in self.fields.values():
            field.error_messages = {'required': 'Это обязательное поле', 'invalid': 'Проверьте правильность'}


class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=256)
    last_name = forms.CharField(max_length=256)
    surname = forms.CharField(max_length=256)
    email = forms.EmailField()
    phone = forms.CharField(max_length=16)
    password = forms.CharField()
    password_confirm = forms.CharField()
    is_worker = forms.BooleanField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # if you want to do it to all of them
        for field in self.fields.values():
            field.error_messages = {'required': 'Это обязательное поле', 'invalid': 'Проверьте правильность'}

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

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(username=email).exists():
            self.add_error('email', 'Такой email уже зарегистрирован')
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if len(phone) != 11:
            self.add_error('phone', 'Должно быть 11 цифр')
        for c in phone:
            if c not in string.digits:
                self.add_error('phone', 'Должно быть 11 цифр')
                break
        return phone

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            self.add_error('password', 'В пароле менее 8 символов')
        return password

    def clean_password_confirm(self):
        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data['password_confirm']
        if password != password_confirm:
            self.add_error('password_confirm', 'Пароли не совпадают')

    def forbidden_sym(self, value):
        forb_sym = ';: '
        for char in forb_sym:
            if char in value:
                return True
        return False



