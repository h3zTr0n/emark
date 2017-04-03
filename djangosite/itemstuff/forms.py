# -*- coding: UTF-8 -*-
# __author__: Alison Mukoma

from __future__ import absolute_import

from django import forms

from .models import Electronics
from .models import BoutiquesFashion
from .models import Motor
from .models import Event

from .models import Job
from .models import Service
from .models import Education
from .models import HomeGarden

class JobModelForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ['created_by']

class ServiceModelForm(forms.ModelForm):
    class Meta:
        model = Service
        exclude = ['created_by']

class EducationModelForm(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ['created_by']

class HomeGardenModelForm(forms.ModelForm):
    class Meta:
        model = HomeGarden
        exclude = ['created_by']

# Model form for Electronics table
class ElectronicsModelForm(forms.ModelForm):
    class Meta:
        model = Electronics
        exclude = ["created_by"]


class BoutiquesFashionModelForm(forms.ModelForm):
    class Meta:
        model = BoutiquesFashion
        exclude = ["created_by"]

class MotorModelForm(forms.ModelForm):
    class Meta:
        model = Motor
        exclude = ["created_by"]

class EventModelForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ["created_by"]
