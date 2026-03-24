from django import forms
from contenido import models


class BeneficariosForm(forms.ModelForm):
    class Meta:
        model = models.Beneficiarios
        fields = '__all__'

class IndicadoresForm(forms.ModelForm):
    class Meta:
        model = models.IndicadorMGA
        fields = '__all__'