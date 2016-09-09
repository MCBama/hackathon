from django.contrib import admin
from triageWeb.models import Reporter
from triageWeb.models import HealthCenter
from triageWeb.models import CenterProperties
from triageWeb.models import Person
from triageWeb.models import Structure
from triageWeb.models import Condition
from triageWeb.models import Disease
from triageWeb.models import Injury
# Register your models here.
admin.site.register(Reporter)
admin.site.register(HealthCenter)
admin.site.register(CenterProperties)
admin.site.register(Person)
admin.site.register(Structure)
admin.site.register(Condition)
admin.site.register(Disease)
admin.site.register(Injury)
