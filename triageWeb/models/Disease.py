from django.db import models
from django.conf import settings

from .Condition import *

class Disease(models.Model):
  DECEASED = 'deceased'
  CRITICAL = 'critical'
  STABLE = 'stable'
  CLEARED = 'cleared'
  STATUS = (
      (DECEASED, 'Deceased'),
      (CRITICAL, 'Critical'),
      (STABLE, 'Stable'),
      (CLEARED, 'Cleared'),
  )

  EBOLA = 'ebola'
  DISEASES = (
    (EBOLA, 'Ebola'),
  )

  image_urls = {
    'deceased': 'images/black_person.png',
    'critical': 'images/red_person.png',
    'stable': 'images/yellow_person.png',
    'cleared': 'images/green_person.png'
  }

  disease_name = models.CharField(choices = DISEASES, default=EBOLA, max_length=20)
  status = models.CharField(choices = STATUS, default = CLEARED, max_length=20)

  condition = models.OneToOneField(Condition)

  def map_image_url(self):
    return self.image_urls[self.status]
