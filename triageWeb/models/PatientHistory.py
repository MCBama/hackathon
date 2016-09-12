from django.db import models
from django.conf import settings

import datetime

from .Person import Person

class PatientHistory(models.Model):
  # one to many with Report
  patient = models.OneToOneField(Person)

  def add_report(self):
    patient = self.patient
    self.report_set.create(latitude=patient.latitude, longitude=patient.longitude,
    reporter=patient.updater, center=patient.center)

  def __str__(self):
    return "History for Patient {}".format(self.patient.id)
