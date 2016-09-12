from django.db import models
from django.conf import settings

from .Condition import *

class Injury(models.Model):
  DECEASED = 'deceased'
  CRITICAL = 'critical'
  INJURED = 'injured'
  OK = 'ok'
  STATUS = (
      (DECEASED, 'Deceased'),
      (CRITICAL, 'Critical'),
      (INJURED, 'Injured'),
      (OK, 'Ok'),
  )

  image_urls = {
    'deceased': 'images/trans_hatch_black.png',
    'critical': 'images/trans_hatch_red.png',
    'injured': 'images/trans_hatch_yellow.png',
    'ok': 'images/trans_hatch_green.png',
  }

  status = models.CharField(choices = STATUS, default = OK, max_length=20)

  condition = models.OneToOneField(Condition)

  def map_image_url(self):
    return self.image_urls[self.status]

  def __str__(self):
    return self.condition.__str__();
