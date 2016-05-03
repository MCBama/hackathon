from django.db import models
from django.conf import settings

# Create your models here.

class TriageProperties(models.Model):
  status=models.CharField(max_length=20, default="")
  mapText=models.CharField(max_length=20, default="")
  created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
  green = models.IntegerField(default=0)
  yellow = models.IntegerField(default=0)
  red = models.IntegerField(default=0)
  casualties = models.IntegerField(default=0)

  def __str__(self):
    return str(self.id)  
  
class TriageGeometry(models.Model):
  geo_type = models.CharField(max_length=20, default="")
  
class TriageCoord(models.Model):
  lat=models.DecimalField(decimal_places=13, max_digits=50, default=0.0)
  lng=models.DecimalField(decimal_places=13, max_digits=50, default=0.0)
  geoObj = models.ForeignKey(TriageGeometry)
  
class TriageArea(models.Model):
  properties=models.ForeignKey(TriageProperties)
  geometry = models.ForeignKey(TriageGeometry)
  
  def update_counts(self):
    queryset = Person.objects.all().filter(is_active=True, triage=self)
    self.properties.green = queryset.filter(status="ok").count()
    self.properties.yellow = queryset.filter(status="injured").count()
    self.properties.red = queryset.filter(status="critical").count()
    self.properties.casualties = queryset.filter(status="deceased").count()
    self.properties.save()
    
  def __str__(self):
    return self.properties.__str__()
    
class Reporter(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

  def __str__(self):
    return self.user.username

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

class Person(models.Model):
    def get_initial(initial_reporter):
      return initial_reporter.id

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
    status = models.CharField(choices=STATUS, default=OK, max_length=20)
    latitude = models.DecimalField(decimal_places=30, max_digits=50, default=0.0)
    longitude = models.DecimalField(decimal_places=30, max_digits=50, default=0.0)
    initial_reporter = models.ForeignKey(Reporter, related_name='reporter')
    updater = models.ForeignKey(Reporter, default=None, null=True)
    report_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    update_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=30, default="")
    last_name = models.CharField(max_length=30, default="")
    triage = models.ForeignKey(TriageArea, null=True)
    
    def html_output(self):
      string = (
        "<div>"
          "Type: Person<br/>"
          "Initial Reporter: %s<br/>"
          "Initial Report Time: %s<br/>"
          "Latest Updater: %s<br/>"
          "Last Updated: %s<br/>"
          "Name: %s %s<br/>"
          "Status: %s<br/>"
          "Latitude: %.13f<br/>"
          "Longitude: %.13f<br/>"
        "</div>" % (self.initial_reporter,
                    self.report_time.strftime("%Y-%m-%d %H:%M:%S"),
                    self.updater,
                    self.update_time.strftime("%Y-%m-%d %H:%M:%S"),
                    self.first_name.capitalize(),
                    self.last_name.capitalize(),
                    self.status.__str__().capitalize(),
                    self.latitude,
                    self.longitude)
      )
      return string

