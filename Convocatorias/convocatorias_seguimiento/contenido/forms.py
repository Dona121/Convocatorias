from django import forms
from contenido import models
from django.forms import Textarea


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
        fields = ["vigencia","fuente","valor_comprometido","valor_pagado",]

class ComentariosDelProyecto(forms.ModelForm):

    class Meta:
        model = models.ComentariosProyectos
        fields = ["comentario"]

        widgets = {
            "comentario": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": """
                        w-full min-w-[500px]
                        rounded-xl
                        border border-gray-300
                        dark:border-gray-700
                        shadow-sm
                    """,
                }
            )
        }