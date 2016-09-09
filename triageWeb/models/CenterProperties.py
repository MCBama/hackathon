
from django.db import models
from django.conf import settings

class CenterProperties(models.Model):
  status=models.CharField(max_length=20, default="")
  mapText=models.CharField(max_length=20, default="")
  verified = models.CharField(max_length=10)
  latitude = models.DecimalField(decimal_places=13, max_digits=50, default=0.0)
  longitude = models.DecimalField(decimal_places=13, max_digits=50, default=0.0)
  created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
  green = models.IntegerField(default=0)
  yellow = models.IntegerField(default=0)
  red = models.IntegerField(default=0)
  casualties = models.IntegerField(default=0)

  def update_counts(self, queryset):
    injury_ok = queryset.filter(condition__injury__status="ok").count()
    injury_injured = queryset.filter(condition__injury__status="injured").count()
    injury_critical = queryset.filter(condition__injury__status="critical").count()
    injury_dead = queryset.filter(condition__injury__status="deceased").count()

    disease_cleared = queryset.filter(condition__disease__status="cleared").count()
    disease_stable = queryset.filter(condition__disease__status="stable").count()
    disease_critical = queryset.filter(condition__disease__status="critical").count()
    disease_dead = queryset.filter(condition__disease__status="deceased").count()

    self.green = injury_ok + disease_cleared
    self.yellow = injury_injured + disease_stable
    self.red = injury_critical + disease_critical
    self.casualties = injury_dead + disease_dead
    self.save()

  def __str__(self):
    return str(self.id)
