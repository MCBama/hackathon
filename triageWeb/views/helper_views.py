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
