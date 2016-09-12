from django.db import models
from django.conf import settings

import datetime

from .PatientHistory import *
from .Reporter import *
from .HealthCenter import *

class Report(models.Model):
  patient_history = models.ForeignKey(PatientHistory)

  latitude = models.DecimalField(decimal_places=30, max_digits=50, default=0.0)
  longitude = models.DecimalField(decimal_places=30, max_digits=50, default=0.0)
  reporter = models.ForeignKey(Reporter, default=None, null=True)
  report_time = models.DateTimeField(auto_now=False, auto_now_add=True)
  center = models.ForeignKey(HealthCenter, null=True)

  def __str__(self):
    return str(self.id)
