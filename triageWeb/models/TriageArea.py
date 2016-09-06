from django.db import models
from django.conf import settings

from .TriageProperties import *
from .TriageGeometry import *

class TriageArea(models.Model):
  properties=models.ForeignKey(TriageProperties)
  geometry = models.ForeignKey(TriageGeometry)

  def update_counts(self):
    queryset = Person.objects.all().filter(is_active=True, triage=self)
    self.properties.green = queryset.filter(status="ok").count()
    self.properties.yellow = queryset.filter(status="injured").count()
    self.properties.red = queryset.filter(status="critical").count()
    self.properties.casualties = queryset.filter(status="deceased").count()
    self.properties.save()

  def __str__(self):
    return self.properties.__str__()
