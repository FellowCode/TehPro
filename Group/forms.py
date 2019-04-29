from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import *
from Account.models import ExtUser


class MultipleValueWidget(forms.TextInput):
    def value_from_datadict(self, data, files, name):
        return data.getlist(name)


class MultipleValueField(forms.Field):
    widget = MultipleValueWidget


def clean_int(x):
    try:
        return int(x)
    except ValueError:
        raise ValidationError("Cannot convert to integer: {}".format(repr(x)))


class MultipleIntField(MultipleValueField):
    def clean(self, value):
        values = []
        for x in value:
            try:
                values.append(int(x))
            except:
                print("'{0}' convert to int error".format(x))
        return values

class CreateGroupForm(forms.Form):
    name = forms.CharField(max_length=256)

    workers = MultipleIntField()

    def clean_name(self):
        name = self.cleaned_data['name']

        if Group.objects.filter(name=name).exists():
            self.add_error('name', 'такое название уже используется')

        return name

    def clean_workers(self):
        workers = self.cleaned_data['workers']
        for worker in workers:
            extuser = ExtUser.objects.filter(id=worker).first()
            if not extuser:
                self.add_error('workers', 'пользователя не существует')
                break
            if not extuser.is_worker:
                self.add_error('workers', extuser.user.last_name + ' не является исполнителем')
                break
        set_workers = set(workers)
        if len(set_workers) != len(workers):
            self.add_error('workers', 'Исполнители совпадают')
        return workers

class ChangeGroupForm(ModelForm):
    workers = MultipleIntField()

    id = forms.IntegerField()

    class Meta:
        model = Group
        fields = ['name']

    def clean_workers(self):
        workers = self.cleaned_data['workers']
        for worker in workers:
            extuser = ExtUser.objects.filter(id=worker).first()
            if not extuser:
                self.add_error('workers', 'пользователя не существует')
                break
            if not extuser.is_worker:
                self.add_error('workers', extuser.user.last_name + ' не является исполнителем')
                break
        set_workers = set(workers)
        if len(set_workers) != len(workers):
            self.add_error('workers', 'Исполнители совпадают')
        return workers

    def clean(self):
        cleaned_data = super(ChangeGroupForm, self).clean()
        name = cleaned_data['name']
        group = Group.objects.filter(name=name).first()
        if group and group.id != cleaned_data['id']:
            self.add_error('name', 'такое название уже используется')
        return cleaned_data

class GroupForm(ModelForm):
    class Meta:
        model = Group
        exclude = ['name', 'id']
