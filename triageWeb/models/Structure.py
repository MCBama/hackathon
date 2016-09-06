from django.db import models
from django.conf import settings

from .Reporter import *

class Structure(models.Model):
  DESTROYED = 'destroyed'
  UNSOUND = 'unsound'
  DAMAGED = 'damaged'
  OK = 'ok'
  STATUS = (
    (DESTROYED, 'Destroyed'),
    (UNSOUND, 'Unsound'),
    (DAMAGED, 'Damaged'),
    (OK, 'Ok'),
  )
  status = models.CharField(choices=STATUS, default=OK, max_length=20)
  latitude = models.DecimalField(decimal_places=15, max_digits=50, default=0.0)
  longitude = models.DecimalField(decimal_places=15, max_digits=50, default=0.0)
  initial_reporter = models.ForeignKey(Reporter, related_name='reporter2')
  updater = models.ForeignKey(Reporter, default=None, null=True)
  report_time = models.DateTimeField(auto_now=False, auto_now_add=True)
  update_time = models.DateTimeField(auto_now=False, auto_now_add=True)
  is_active = models.BooleanField(default=True)

  def html_output(self):
    string = (
      "<div>"
      "Type: Structure<br/>"
      "Initial Reporter: %s<br/>"
      "Initial Report Time: %s<br/>"
      "Latest Updater: %s<br/>"
      "Last Updated: %s<br/>"
      "Status: %s<br/>"
      "Latitude: %f<br/>"
      "Longitude: %f<br/>"
      "</div>" % (self.initial_reporter,
                  self.report_time.strftime("%Y-%m-%d %H:%M:%S"),
                  self.updater,
                  self.update_time.strftime("%Y-%m-%d %H:%M:%S"),
                  self.status,
                  self.latitude,
                  self.longitude)
    )
    return string

  def __str__(self):
    return self.status
