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

class DiseaseNewReportForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(DiseaseNewReportForm, self).__init__(*args, **kwargs)
    self.fields['status'] = forms.ChoiceField(Disease.STATUS, initial="cleared")
    self.fields['disease_name'] = forms.ChoiceField(Disease.DISEASES, initial="ebola")
  class Meta:
    model = Person
    fields=[
      'latitude',
      'longitude'
    ]

class DiseaseReportForm(DiseaseNewReportForm):
  def __init__(self, *args, **kwargs):
    super(DiseaseReportForm, self).__init__(*args, **kwargs)
    self.fields['center'].required = False

  class Meta(DiseaseNewReportForm.Meta):
    DiseaseNewReportForm.Meta.fields.append('center')

class InjuryNewReportForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(InjuryNewReportForm, self).__init__(*args, **kwargs)
    self.fields['status'] = forms.ChoiceField(Injury.STATUS, initial="ok")

  class Meta:
    model = Person
    fields=[
      'latitude',
      'longitude'
    ]

class InjuryReportForm(InjuryNewReportForm):
  def __init__(self, *args, **kwargs):
    super(InjuryReportForm, self).__init__(*args, **kwargs)
    self.fields['center'].required = False

  class Meta(InjuryNewReportForm.Meta):
    model = Person
    InjuryNewReportForm.Meta.fields.append('center')
