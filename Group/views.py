from django.http import Http404
from django.shortcuts import render, redirect

from .forms import *
from .models import *
from Account.models import *

def create_group(request):
    if request.user.is_staff:
        data = {}
        data['workers'] = ExtUser.objects.filter(is_worker=True)
        if request.method == 'POST':
            form = CreateGroupForm(request.POST)

            if form.is_valid():
                group = Group.objects.create(name=form.cleaned_data['name'])
                group.save()

                for worker in form.cleaned_data['workers']:
                    extuser = ExtUser.objects.get(id=worker)
                    extuser.group = group
                    extuser.save()
                request.session['group_created'] = True
                return redirect('/group/list/')
            data['form'] = form
            return render(request, 'Group/CreateGroup.html', data)
        return render(request, 'Group/CreateGroup.html', data)
    raise Http404

def change_group(request, id):
    if request.user.is_staff:
        group = Group.objects.filter(id=id).first()
        if group:
            data = {}
            data['workers'] = ExtUser.objects.filter(is_worker=True)
            last_workers = group.extuser_set.all()
            data['group_workers'] = last_workers
            data['group'] = group
            if request.method == 'POST':
                form = ChangeGroupForm(request.POST, instance=group)
                if form.is_valid():
                    form.save()
                    for worker in last_workers:
                        worker.group = None
                        worker.save()
                    for worker in form.cleaned_data['workers']:
                        extuser = ExtUser.objects.get(id=worker)
                        extuser.group = group
                        extuser.save()
                    request.session['group_changed'] = True
                    return redirect('/group/{0}/'.format(group.id))
                data['form'] = form
                return render(request, 'Group/ChangeGroup.html', data)
            data['form'] = ChangeGroupForm(instance=group, initial={'id': group.id})
            return render(request, 'Group/ChangeGroup.html', data)
        raise Http404
    raise Http404

def worker_group(request, id=None):
    data = {}
    if id and request.user.is_staff:
        group = Group.objects.filter(id=id).first()
        data['group'] = group
    else:
        user = request.user
        group = user.extuser.group
    if group:
        if request.method == 'POST':
            form = GroupForm(request.POST, instance=group)
            if form.is_valid():
                form.save()
                return redirect('/')
        data['form'] = GroupForm(instance=group)
        return render(request, 'Group/WorkerGroupForm.html', data)
    raise Http404

def group_list(request):
    groups = Group.objects.all()
    return render(request, 'Group/GroupList.html', {'groups': groups})
