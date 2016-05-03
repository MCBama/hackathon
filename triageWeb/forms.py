from django import forms

from .models import Person
from .models import Structure

class StructureForm(forms.ModelForm):
  report_type = forms.ChoiceField(choices=[('structure','Structure'),('person','Person')])
  class Meta:
    model = Structure
    fields=[
      'status',
      'latitude',
      'longitude'
    ]

class ReportForm(forms.ModelForm):
  report_type = forms.ChoiceField(choices=[('structure','Structure'),('person','Person')])
  class Meta:
    model = Person
    fields=[
      'status',
      'latitude',
      'longitude'
    ]
  
class UpdatePersonForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(UpdatePersonForm, self).__init__(*args, **kwargs)
    self.fields['triage'].required = False
  class Meta:
    model = Person
    fields=[
      'status',
      'latitude',
      'longitude',
      'triage'
    ]
    
        
class UpdateStructureForm(forms.ModelForm):
  class Meta:
    model = Structure
    fields=[
      'status',
      'latitude',
      'longitude'
    ]