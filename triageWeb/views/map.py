from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from triageWeb.models import Person
from triageWeb.models import Structure
from triageWeb.models import TriageArea
from triageWeb.models import TriageCoord
from triageWeb.models import HealthCenter

def map_view(request):
  casualty_list = Person.objects.all().filter(is_active=True)
  print(casualty_list)
  structure_list = Structure.objects.all().filter(is_active=True)
  triage_list = TriageArea.objects.filter(properties__mapText="Triage Area")
  center_list = HealthCenter.objects.all()
  #for center in center_list:
  #  center.update_counts(casualty_list.filter(center=center))
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
