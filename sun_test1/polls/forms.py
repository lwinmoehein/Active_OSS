from django import forms
from django.forms import ModelForm
from .models import TestModel

class PersonForm(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = TestModel
        fields = ['name','nrc','occupation','father_name','father_nrc','dob','spouse_name','spouse_nrc','labour_id','marital_status','race','religion']

class UpdatePerson(ModelForm):
  required_css_class = 'required'
  class Meta:
        fields = ['nrc','attribute','value']
# model = TestModel
       