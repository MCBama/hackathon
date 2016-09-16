from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

import csv
import codecs
from urllib.request import urlopen

from triageWeb.models import Person
from triageWeb.models import Structure
from triageWeb.models import TriageArea
from triageWeb.models import TriageCoord
from triageWeb.models import HealthCenter
from triageWeb.models import CenterProperties

def parse_hospital_data():
  url = "https://docs.google.com/spreadsheets/d/1paoIpHiYo7dy_dnf_luUSfowWDwNAWwS3z4GHL2J7Rc/export?format=csv&id=1paoIpHiYo7dy_dnf_luUSfowWDwNAWwS3z4GHL2J7Rc&gid=2077872077"
  response = urlopen(url)
  # read csv data from url
  cr = csv.DictReader(codecs.iterdecode(response, 'utf-8'))
  data = []
  existingCenters = HealthCenter.objects.all()
  for row in cr:
    # only add "open" hospitals for now
    if "Open" in row["Status"]:
      data.append(dict(row))
  # create centers from data retrived from list
  for center in data:
    healthCenter = HealthCenter(
      name = center["Center"],
      center_type = center["Type"],
      center_id = center["Center ID"],
    )
    # check if center has already been added to the list
    if existingCenters.filter(center_id=center["Center ID"]).count() == 0:
      # clean up some user input errors
      if center["Lat"].endswith(".") or center["Lat"].endswith(","):
        center["Lat"] = center["Lat"][:-1]
      if center["Long"].endswith(".") or center["Long"].endswith(","):
        center["Long"] = center["Long"][:-1]
      properties = CenterProperties(
        status = center["Status"],
        verified = center["Verified"],
        latitude = center["Lat"].replace(",", "."),
        longitude = center["Long"].replace(",", "."),
      )
      properties.save()
      healthCenter.properties = properties;
      healthCenter.save()

def map_view(request):
  casualty_list = Person.objects.all().filter(is_active=True,center=None)
  structure_list = Structure.objects.all().filter(is_active=True)
  triage_list = TriageArea.objects.filter(properties__mapText="Triage Area")
  center_list = HealthCenter.objects.all()

  if(center_list.count() == 0):
    parse_hospital_data()
    center_list = HealthCenter.objects.all()

  for triage in triage_list:
    coord = TriageCoord.objects.get(geoObj=triage.geometry)
    triage.geometry.coordinates = {'lat':coord.lat, 'lng':coord.lng}
  context = {
    'center_lat':10.516667,
    'center_lon':-10.7,
    'casualty_list':casualty_list,
    'structure_list':structure_list,
    'center_list':center_list
  }
  return render(request, 'map_view.html', context)
