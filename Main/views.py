from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

from Main.forms import MaterialForm
from Main.models import Material
from Group.models import Group
from django.db.models import Q

def index(request):
    return render(request, 'Main/Index.html')

def debug(request):
    from TehPro.settings import DEBUG
    return HttpResponse(DEBUG)

def show_materials(request):
    if request.user.is_staff:
        data = {}
        mat = Material.objects.all().first()
        data['form'] = MaterialForm(instance=mat)
        groups = Group.objects.filter(Q(plug__lte=30) | Q(connector__lte=10) | Q(rosette__lte=10) | Q(cable__lte=100))
        data['groups'] = groups
        if request.method == 'POST':
            data['form'] = MaterialForm(request.POST, instance=mat)
            data['form'].save()
            return render(request, 'Main/Materials.html', data)
        return render(request, 'Main/Materials.html', data)
    return Http404
