import csv
import codecs

from urllib.request import urlopen
from django.http import HttpResponse, HttpResponseNotFound

from triageWeb.models import HealthCenter
from triageWeb.models import CenterProperties

def parse_json(request):
  response = urlopen("https://geo-q.com/geoq/api/jobs/182.geojson")
  data = json.loads(response.read().decode("utf-8"))

  for feature in data['features']:
    if TriageProperties.objects.filter(pk=feature['properties']['id']).count()==0:
      properties = TriageProperties(
      status = feature['properties']['status'],
      created_at = dateparse.parse_time(feature['properties']['created_at']),
      updated_at = dateparse.parse_time(feature['properties']['updated_at']),
      id = feature['properties']['id']
      )
      if 'mapText' in feature['properties']:
        properties.mapText = feature['properties']['mapText']
        geometry = TriageGeometry(
        geo_type = feature['geometry']['type']
        )
        geometry.save()
        coords = feature['geometry']['coordinates']
        if geometry.geo_type == "Point":
          coord = TriageCoord(
          lat = coords[1],
          lng = coords[0],
          geoObj = geometry
          )
          coord.save()
          area = TriageArea(
          properties = properties,
          geometry = geometry
          )
          properties.save()
          area.save()
  return HttpResponse("parsed")

def view_hospital_data(request):
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
  return HttpResponse("Hospital Data Read")
