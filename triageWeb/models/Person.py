from django.db import models
from django.conf import settings

import datetime

from .Reporter import *
from .HealthCenter import *

class Person(models.Model):
  def get_initial(initial_reporter):
    return initial_reporter.id

  # one to one with PatientHistory
  latitude = models.DecimalField(decimal_places=30, max_digits=50, default=0.0)
  longitude = models.DecimalField(decimal_places=30, max_digits=50, default=0.0)
  initial_reporter = models.ForeignKey(Reporter, related_name='reporter')
  updater = models.ForeignKey(Reporter, default=None, null=True)
  report_time = models.DateTimeField(auto_now=False, auto_now_add=True)
  update_time = models.DateTimeField(auto_now=False, auto_now_add=True)
  is_active = models.BooleanField(default=True)
  first_name = models.CharField(max_length=30, default="")
  last_name = models.CharField(max_length=30, default="")
  center = models.ForeignKey(HealthCenter, null=True)

  def update(self, form_data, reporter):
    self.condition.set_status(form_data['status'])
    self.latitude=form_data['latitude']
    self.longitude=form_data['longitude']
    self.updater=reporter
    self.update_time = datetime.datetime.now()
    if form_data['center']:
      previous_center = self.center
      self.center = form_data['center']
      self.latitude = self.center.properties.latitude
      self.longitude = self.center.properties.longitude
    self.save()

    if self.center is not None:
      self.update_center_count()
      if previous_center is not None:
        self.update_center_count(previous_center)

  def status(self):
    return self.condition.status()

  def condition_type(self):
    return self.condition.get_condition()

  status = property(status)
  condition_type = property(condition_type)

  def get_map_image_url(self):
    return self.condition.get_map_image_url()

  def update_center_count(self, center=None):
    if center is None:
      center = self.center
    queryset = Person.objects.all().filter(is_active=True, center=center)
    center.update_counts(queryset)

  def html_output(self):
    string = (
      "<div>"
        "Type: Person<br/>"
        "Patient ID: %s<br/>"
        "Initial Reporter: %s<br/>"
        "Initial Report Time: %s<br/>"
        "Latest Updater: %s<br/>"
        "Last Updated: %s<br/>"
        "Name: %s %s<br/>"
        "Status: %s<br/>"
        "Latitude: %.5f<br/>"
        "Longitude: %.5f<br/>"
      "</div>" % (self.id,
                  self.initial_reporter,
                  self.report_time.strftime("%Y-%m-%d %H:%M:%S"),
                  self.updater,
                  self.update_time.strftime("%Y-%m-%d %H:%M:%S"),
                  self.first_name.capitalize(),
                  self.last_name.capitalize(),
                  self.status.__str__().capitalize(),
                  round(self.latitude,5),
                  round(self.longitude,5))
    )
    return string

  def __str__(self):
    return str(self.id)
