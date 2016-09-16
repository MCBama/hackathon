from django.db.models.signals import post_save
from django.dispatch import receiver

from triageWeb.models.PatientHistory import PatientHistory
from triageWeb.models.Person import Person

from triageWeb.models.Injury import Injury
from triageWeb.models.Disease import Disease

@receiver(post_save, sender=Person)
def create_report(sender, instance, created, raw, using, **kwargs):
  print("creating report")
  try:
    instance.patienthistory.add_report()
    instance.patienthistory.save()
  except Exception as e:
    instance.patienthistory = PatientHistory(patient=instance)
    instance.patienthistory.save()
    instance.patienthistory.add_report()

@receiver(post_save, sender=Injury)
@receiver(post_save, sender=Disease)
def update_report(sender, instance, created, raw, using, **kwargs):
  report = instance.condition.person.patienthistory.report_set.latest('report_time')
  report.patient_status = instance.status
  report.save()
