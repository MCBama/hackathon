from django.db import models
from django.conf import settings

from .Person import *

class Condition(models.Model):
  # one to one with Injury
  # one to one with Disease
  person = models.OneToOneField(Person)
  DISEASE = 'disease'
  INJURY = 'injury'
  TYPES = (
      (DISEASE, 'Disease'),
      (INJURY, 'Injury'),
  )

  condition_type = models.CharField(choices = TYPES, default = INJURY, max_length=20)

  def status(self):
    status = "Unknown"
    if self.condition_type == self.INJURY:
      try:
        status = self.injury.status
      except Exception as e:
        status="Unknown"
    elif self.condition_type == self.DISEASE:
      try:
        status = self.disease.status
      except Exception as e:
        status = "Unknown"
    return status

  def set_status(self, status):
    if self.condition_type == self.INJURY:
      if self.injury:
        self.injury.status = status
        self.injury.save()
    elif self.condition_type == self.DISEASE:
      if self.disease:
        self.disease.status = status
        self.disease.save()

  def get_condition(self):
    if self.condition_type == self.INJURY:
      return self.condition_type
    elif self.condition_type == self.DISEASE:
      if self.disease:
        return self.disease.disease_name

  def get_map_image_url(self):
    if self.condition_type == self.INJURY:
      if self.injury:
        return self.injury.map_image_url()
    elif self.condition_type == self.DISEASE:
      if self.disease:
        return self.disease.map_image_url()

  def __str__(self):
    return str(self.person.id)
