from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from triageWeb.models import Person
from triageWeb.models import Structure
from triageWeb.models import TriageArea
from triageWeb.models import TriageCoord

@login_required
def map_view(request):
  casualty_list = Person.objects.all().filter(is_active=True)
  structure_list = Structure.objects.all().filter(is_active=True)
  triage_list = TriageArea.objects.filter(properties__mapText="Triage Area")
  for triage in triage_list:
    coord = TriageCoord.objects.get(geoObj=triage.geometry)
    triage.geometry.coordinates = {'lat':coord.lat, 'lng':coord.lng}
  context = {
    'center_lat':34.738228,
    'center_lon':-86.601791,
    'casualty_list':casualty_list,
    'structure_list':structure_list,
    'triage_list':triage_list
  }
  return render(request, 'map_view.html', context)
