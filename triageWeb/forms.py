from django import forms

from .models import Person
from .models import Structure
from .models import Injury
from .models import Disease

class StructureForm(forms.ModelForm):
  class Meta:
    model = Structure
    fields=[
      'latitude',
      'longitude',
      'status'
    ]

class DiseaseReportForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(DiseaseReportForm, self).__init__(*args, **kwargs)
    self.fields['center'].required = False
    self.fields['status'] = forms.ChoiceField(Disease.STATUS, initial="cleared")
    self.fields['disease_name'] = forms.ChoiceField(Disease.DISEASES, initial="ebola")
  class Meta:
    model = Person
    fields=[
      'latitude',
      'longitude',
      'center'
    ]

class InjuryReportForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(InjuryReportForm, self).__init__(*args, **kwargs)
    self.fields['center'].required = False
    self.fields['status'] = forms.ChoiceField(Injury.STATUS, initial="ok")

  class Meta:
    model = Person
    fields=[
      'latitude',
      'longitude',
      'center'
    ]
