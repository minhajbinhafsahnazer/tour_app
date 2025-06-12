# C:\api\tourproject\tourapp\forms.py

from django import forms
from .models import Destination, DestinationImage

class DestinationForm(forms.ModelForm):

    class Meta:
        model = Destination
        fields = ['place_name', 'weather', 'state', 'district', 'map_link', 'description']


