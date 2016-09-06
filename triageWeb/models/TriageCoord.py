from django.db import models
from django.conf import settings

from .TriageGeometry import *

class TriageCoord(models.Model):
  lat=models.DecimalField(decimal_places=13, max_digits=50, default=0.0)
  lng=models.DecimalField(decimal_places=13, max_digits=50, default=0.0)
  geoObj = models.ForeignKey(TriageGeometry)
