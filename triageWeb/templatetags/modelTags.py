from django import template
from django.template.defaultfilters import stringfilter
from django.utils import timezone

from django.db import models

import datetime

register = template.Library()

@register.filter(name='getattribute')
def getattribute(object, str):
  attr = getattr(object, str)
  if type(attr) == datetime.datetime:
    string = timezone.localtime(attr).strftime("%Y-%m-%d %H:%M:%S")
  else:
    string = attr.__str__()
  return string.capitalize()

@register.filter(name='class_name')
def class_name(object):
  return object.__class__.__name__

@register.filter(name='class_name_lower')
def class_name_lower(object):
  return object.__class__.__name__.lower()

@register.filter(name="dict_get_key")
def dict_get_key(dictionary, key):
  return dictionary[key]
