from django.db import models
from django.conf import settings

class TriageGeometry(models.Model):
  geo_type = models.CharField(max_length=20, default="")
