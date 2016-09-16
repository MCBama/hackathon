from django.db import models
from django.conf import settings

from .CenterProperties import *

class HealthCenter(models.Model):
  name = models.CharField(max_length=30)
  created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
  center_type = models.CharField(max_length=30)
  center_id = models.CharField(max_length=6)

  properties = models.OneToOneField(CenterProperties)

  def patient_count(self):
    return self.person_set.filter(is_active=True).count()

  def update_counts(self, queryset):
    self.properties.update_counts(queryset)

  def __str__(self):
    return self.name
