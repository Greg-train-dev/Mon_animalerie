from django import forms
from .models import Animal
from .models import Equipement


class MoveForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ('lieu',)