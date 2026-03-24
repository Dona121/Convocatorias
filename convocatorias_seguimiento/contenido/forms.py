from django import forms
from contenido import models


class BeneficiariosForm(forms.ModelForm):
    class Meta:
        model = models.Beneficiarios
        fields = '__all__'

class IndicadoresForm(forms.ModelForm):
    class Meta:
        model = models.IndicadorMGA
        fields = '__all__'

class FuentesForm(forms.ModelForm):
    class Meta:
        model = models.FuenteFinanciacion
        fields = "__all__"