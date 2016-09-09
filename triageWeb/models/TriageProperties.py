
from django.db import models
from django.conf import settings

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
