from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils import timezone, dateparse
from django.contrib.auth.models import User

from triageWeb.models import HealthCenter
from triageWeb.models import Person

def view(request, id):
  center = HealthCenter.objects.get(pk=id)
  patients = Person.objects.all().filter(center=center, is_active=True)
  context = {
    'center':center,
    'patient_list':patients
  }
  return render(request,'center/view.html',context)

def list(request):
  center_list = HealthCenter.objects.all()
  context = {
    'center_list':center_list
  }
  return render(request, 'center/list.html', context)
