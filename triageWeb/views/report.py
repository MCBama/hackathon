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
from triageWeb.models import Condition
from triageWeb.models import Injury
from triageWeb.models import Disease
from triageWeb.models import Reporter
from triageWeb.models import Structure
from triageWeb.models import HealthCenter
from triageWeb.models import TriageArea
from triageWeb.models import TriageProperties
from triageWeb.models import TriageCoord
from triageWeb.models import TriageGeometry


from triageWeb.forms import InjuryReportForm
from triageWeb.forms import DiseaseReportForm
from triageWeb.forms import StructureForm
from triageWeb.forms import InjuryReportForm
from triageWeb.forms import DiseaseReportForm
from triageWeb.forms import StructureForm

@login_required
def report(request):
  injury_form = InjuryReportForm()
  disease_form = DiseaseReportForm()
  structure_form = StructureForm()
  if request.GET and request.GET['lng'] and request.GET['lat']:
    injury_form = InjuryReportForm(initial={
        'latitude':request.GET['lat'],
        'longitude':request.GET['lng']
      })
    disease_form = DiseaseReportForm(initial={
        'latitude':request.GET['lat'],
        'longitude':request.GET['lng']
      })
    structure_form = StructureForm(initial = {
      'latitude':request.GET['lat'],
      'longitude':request.GET['lng']
      })
  casualty_list = Person.objects.all().filter(is_active=True)
  structure_list = Structure.objects.all().filter(is_active=True)
  context = {
    'new_report':True,
    'injury_form':injury_form,
    'disease_form':disease_form,
    'structure_form':structure_form,
    'disease_statuses':Disease.STATUS,
    'injury_statuses':Injury.STATUS,
    'submit_url':"/report_create/",
    'casualty_list':casualty_list,
    'structure_list':structure_list
  }

  return render(request,'report.html',context)

@login_required
def mobile_report(request):
  return render(request, 'mobile_reports.html',{})

def report_create(request):
  if request.method == "POST":
    print(request.POST['report_type'])
    if request.POST['report_type'] == "disease":
      print("handling disease")
      form = DiseaseReportForm(request.POST)
    elif request.POST['report_type'] == "injury":
      form = InjuryReportForm(request.POST)
    else:
      form = StructureForm(request.POST)
    if form.is_valid():
      reporter = Reporter.objects.get(user=request.user)
      report_type = request.POST['report_type']
      if(report_type == 'injury' or
      report_type == 'disease'):
        person_report = Person(
          latitude=form.cleaned_data['latitude'],
          longitude=form.cleaned_data['longitude'],
          initial_reporter=reporter,
          updater = reporter
        )
        person_report.save()
        condition = Condition(
          person = person_report
        )
        if(report_type == "injury"):
          condition.condition_type = Condition.INJURY
          condition.save()
          injury = Injury(
            condition = condition,
            status = form.cleaned_data['status']
          )
          injury.save()
        else:
          condition.condition_type = Condition.DISEASE
          condition.save()
          disease = Disease(
            condition = condition,
            status = form.cleaned_data['status'],
            disease_name = form.cleaned_data['disease_name']
          )
          disease.save()
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
      print("form invalid here")
      return render(request, 'report.html', {'form':form})
  return redirect('/map_view/')

def report_person_edit(request, id):
  report = Person.objects.get(pk=id)
  injury_form = InjuryReportForm(initial={
      'status':report.status,
      'latitude':report.latitude,
      'longitude':report.longitude,
      'center':report.center
    })
  disease_form = DiseaseReportForm(initial={
      'status':report.status,
      'latitude':report.latitude,
      'longitude':report.longitude,
      'center':report.center
    })
  queryset = HealthCenter.objects.all()
  injury_form.fields['center'].queryset = queryset
  disease_form.fields['center'].queryset = queryset
  context = {
    'current_condition':report.condition.condition_type.lower,
    'is_structure':False,
    'injury_form':injury_form,
    'disease_form':disease_form,
    'structure_statuses':Structure.STATUS,
    'submit_url':"/report/person/" + str(report.id) + "/update/"
  }
  return render(request,'report.html',context)

def report_structure_edit(request, id):
  report = Structure.objects.get(pk=id)
  structure_form = StructureForm(initial={
      'status':report.status,
      'latitude':report.latitude,
      'longitude':report.longitude,
    })
  context = {
    'is_structure':True,
    'structure_form':structure_form,
    'structure_statuses':Structure.STATUS,
    'submit_url':"/report/structure/" + str(report.id) + "/update/"
  }
  return render(request,'report.html',context)

def report_update(request, id, report_type):
  if request.method == "POST":
    if request.POST['report_type'] == "injury":
      form = InjuryReportForm(request.POST)
    elif request.POST['report_type'] == "disease":
      form = DiseaseReportForm(request.POST)
    else:
      form = StructureForm  (request.POST)
    if form.is_valid():
      reporter = Reporter.objects.get(user=request.user)
      if report_type == 'person':
        person_report = Person.objects.get(pk=id)
        person_report.update(form.cleaned_data, reporter)

      else:
        structure_report = Structure.objects.get(pk=id)
        structure_report.update(form.cleaned_data, reporter)

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
    ('condition_type', "Condition"),
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
  report_history = person_report.patienthistory.report_set.all().order_by('report_time')

  report_history = report_history.order_by('-report_time')
  for report in report_history:
    print(report)
  return render(request, 'report_view.html',
  {
    'report':person_report,
    'history':report_history,
    'type':'person'
  })

def report_personnel_delete(request, id):
  if request.method == "POST":
    report = Person.objects.get(pk=id)
    report.is_active = False
    report.save()
    if report.center is not None:
      report.update_center_count()
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
