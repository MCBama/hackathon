from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils import timezone, dateparse
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static

from urllib.request import urlopen, urlretrieve

from itertools import chain

import codecs
import json
import datetime
import re

from django.utils import six
from django.utils.timezone import get_fixed_timezone, utc

from triageWeb.models import Person
from triageWeb.models import Reporter
from triageWeb.models import Structure
from triageWeb.models import TriageArea
from triageWeb.models import TriageProperties
from triageWeb.models import TriageCoord
from triageWeb.models import TriageGeometry


from triageWeb.forms import ReportForm
from triageWeb.forms import StructureForm
from triageWeb.forms import UpdatePersonForm
from triageWeb.forms import UpdateStructureForm

@login_required
def report(request):
  form = ReportForm(initial={'report_type':'person'});

  if request.GET and request.GET['lng'] and request.GET['lat']:
    form = ReportForm(initial={
        'latitude':request.GET['lat'],
        'longitude':request.GET['lng'],
        'report_type':'person'
      })
  casualty_list = Person.objects.all().filter(is_active=True)
  structure_list = Structure.objects.all().filter(is_active=True)
  context = {
    'form':form,
    'person_statuses':Person.STATUS,
    'structure_statuses':Structure.STATUS,
    'submit_url':"/report_create/",
    'center_lat':34.738228,
    'center_lon':-86.601791,
    'casualty_list':casualty_list,
    'structure_list':structure_list
  }

  return render(request,'report.html',context)

@login_required
def mobile_report(request):
  return render(request, 'mobile_reports.html',{})

def report_create(request):
  if request.method == "POST":
    if(request.POST['report_type'] == "person"):
      form = ReportForm(request.POST)
    else:
      form = StructureForm(request.POST)
    print(request.POST)
    if form.is_valid():
      reporter = Reporter.objects.get(user=request.user)
      if form.cleaned_data['report_type'] == 'person':
        person_report = Person(
          status=form.cleaned_data['status'],
          latitude=form.cleaned_data['latitude'],
          longitude=form.cleaned_data['longitude'],
          initial_reporter=reporter
        )
        person_report.save()
      else:
        structure_report = Structure(
          status=form.cleaned_data['status'],
          latitude=form.cleaned_data['latitude'],
          longitude=form.cleaned_data['longitude'],
          initial_reporter=reporter
        )
        structure_report.save()
        print(form.cleaned_data)
        print("structure made")
    else:
      print("form invalid")
      return render(request, 'report.html', {'form':form})
  return redirect('/map_view/')

def report_person_edit(request, id):
  report = Person.objects.get(pk=id)
  form = UpdatePersonForm(initial={
      'status':report.status,
      'latitude':report.latitude,
      'longitude':report.longitude,
      'triage':report.triage
    })
  queryset = TriageArea.objects.filter(
    properties__mapText__isnull=False).filter(properties__mapText="Triage Area")
  form.fields['triage'].queryset = queryset
  context = {
    'form':form,
    'person_statuses':Person.STATUS,
    'structure_statuses':Structure.STATUS,
    'submit_url':"/report/person/" + str(report.id) + "/update/"
  }
  return render(request,'report.html',context)

def report_structure_edit(request, id):
  report = Structure.objects.get(pk=id)
  form = UpdateStructureForm(initial={
      'status':report.status,
      'latitude':report.latitude,
      'longitude':report.longitude,
    })
  context = {
    'form':form,
    'person_statuses':Person.STATUS,
    'structure_statuses':Structure.STATUS,
    'submit_url':"/report/structure/" + str(report.id) + "/update/"
  }
  return render(request,'report.html',context)

def report_update(request, id, report_type):
  if request.method == "POST":
    if(report_type == "person"):
      form = UpdatePersonForm(request.POST)
    else:
      form = UpdateStructureForm  (request.POST)
    if form.is_valid():
      reporter = Reporter.objects.get(user=request.user)
      if report_type == 'person':
        person_report = Person.objects.get(pk=id)
        person_report.status=form.cleaned_data['status']
        person_report.latitude=form.cleaned_data['latitude']
        person_report.longitude=form.cleaned_data['longitude']
        person_report.updater=reporter
        person_report.update_time = datetime.datetime.now()
        if form.cleaned_data['triage']:
          person_report.triage = form.cleaned_data['triage']
          person_report.latitude = TriageCoord.objects.get(geoObj=person_report.triage.geometry).lat
          person_report.longitude = TriageCoord.objects.get(geoObj=person_report.triage.geometry).lng

        person_report.save()
        if person_report.triage is not None:
          person_report.triage.update_counts()
      else:
        structure_report = Structure.objects.get(pk=id)
        structure_report.status=form.cleaned_data['status']
        structure_report.latitude=format(form.cleaned_data['latitude'],'.13f')
        structure_report.longitude=format(form.cleaned_data['longitude'], '.13f')
        structure_report.updater=reporter
        structure_report.update_time = datetime.datetime.now()

        structure_report.save()
    else:
      print("form invalid")
      return render(request, 'report.html', {'form':form})
  return redirect('/map_view/')

def report_list(request):
  person_list = Person.objects.all().filter(is_active=True)
  structure_list = Structure.objects.all().filter(is_active=True)
  report_list = list(chain(person_list, structure_list))
  print(timezone.localtime(timezone.now()))
  field_list = [
    ('status','Status'),
    ('initial_reporter','Reporter'),
    ('report_time','Reported'),
    ('updater','Updater'),
    ('update_time','Updated'),
  ]

  context = {
    'report_list':report_list,
    'field_list':field_list
  }
  return render(request, 'report_list.html', context)

def report_personnel_view(request, id):
  person_report = Person.objects.get(pk=id)
  return render(request, 'report_view.html',{'report':person_report, 'type':'person'})

def report_personnel_delete(request, id):
  if request.method == "POST":
    report = Person.objects.get(pk=id)
    report.is_active = False
    report.save()
    if report.triage is not None:
      report.triage.update_counts()
    if 'redirect' in request.POST:
      return redirect('/report/list')
    else:
      return redirect('/map_view/')
  return HttpResponse("Delete Get")

def report_structure_view(request, id):
  structure_report = Structure.objects.get(pk=id)
  return render(request, 'report_view.html',{'report':structure_report, 'type':'structure'})

def report_structure_delete(request, id):
  if request.method == "POST":
    report = Structure.objects.get(pk=id)
    report.is_active = False
    report.save()
    if 'redirect' in request.POST:
      return redirect('/report/list')
    else:
      return redirect('/map_view/')
  return HttpResponse("Delete Get")

def mobile_post_report(request, state, lat, lon):
  user = User.objects.get(username='temp')
  reporter = Reporter.objects.get(user = user)
  if not state or state == 'dead':
    state = 'deceased'

  person = Person(status=state,latitude=lat,longitude=lon,initial_reporter=reporter)
  person.save()
  return redirect('/map_view/')