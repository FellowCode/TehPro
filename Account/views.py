from datetime import datetime

from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

from .forms import *
from django.contrib.auth import authenticate, login, logout
from .models import ExtUser
from time import sleep

def registration(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create(username=form.cleaned_data['email'].lower(),
                                       email=form.cleaned_data['email'].lower(),
                                       password=form.cleaned_data['password'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.extuser.surname = form.cleaned_data['surname']
            user.extuser.phone = form.cleaned_data['phone']
            user.extuser.is_worker = form.cleaned_data['is_worker']
            user.save()
            login(request, user)
            return redirect('/')
        return render(request, 'Account/Registration.html', {'form': form})
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'Account/Registration.html')


def auth(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            form = SignInForm(request.POST)
            if form.is_valid():
                user = authenticate(username=form.cleaned_data['email'].lower(), password=form.cleaned_data['password'])
                if user:
                    login(request, user)
                    return redirect('/')
                return render(request, 'Account/Login.html', {'form': form, 'error': 'Неверный логин или пароль'})
            return render(request, 'Account/Login.html', {'form': form, 'error': 'Неверный логин или пароль'})
        return redirect('/')
    data = {'email_confirm': False, 'password_restored': False}
    if 'email_confirm' in request.session:
        data['email_confirm'] = True
        del request.session['email_confirm']
    if 'password_restored' in request.session:
        data['password_restored'] = True
        del request.session['password_restored']
    return render(request, 'Account/Login.html', data)

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')

def create_group(request):
    data = {}
    data['workers'] = ExtUser.objects.filter(is_worker=True)
    if request.method == 'POST':
        print(request.POST)
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            group = Group.objects.create(name=form.cleaned_data['name'])
            group.save()

            for worker in form.cleaned_data['workers']:
                extuser = ExtUser.objects.get(id=worker)
                extuser.group = group
                extuser.save()
            data['created'] = True
            return render(request, 'Account/Create_group.html', data)
        data['form'] = form
        return render(request, 'Account/Create_group.html', data)
    return render(request, 'Account/Create_group.html', data)

def worker_group(request):
    user = request.user
    group = user.extuser.group
    data = {}
    if group:
        if request.method == 'POST':
            form = GroupForm(request.POST, instance=group)
            if form.is_valid():
                form.save()
                return redirect('/')
        data['form'] = GroupForm(instance=group)
        return render(request, 'Account/WorkerGroupForm.html', data)
    raise Http404
