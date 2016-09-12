from django.db.models.signals import post_save
from django.dispatch import receiver

from triageWeb.models.PatientHistory import PatientHistory
from triageWeb.models.Person import Person

@receiver(post_save, sender=Person)
def create_report(sender, instance, created, raw, using, **kwargs):
  try:
    print(instance.id)
    instance.patienthistory.add_report()
    instance.patienthistory.save()
  except Exception as e:
    print(e)
    print("[Person] Error: Missing Patient History");
    instance.patienthistory = PatientHistory(patient=instance)
    instance.patienthistory.save()
    instance.patienthistory.add_report()
