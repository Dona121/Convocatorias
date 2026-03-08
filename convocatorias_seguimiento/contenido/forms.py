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


from django import forms
from . import models

class ConvocatoriasForm(forms.ModelForm):
    monto = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ej: 15000000.00',
            'class': 'vTextField' 
        })
    )

    class Meta:
        model = models.Convocatorias
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.monto is not None:
            self.initial['monto'] = f"{self.instance.monto:.2f}"

    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        if monto:
            monto_limpio = str(monto).replace('$', '').replace(',', '').strip()
            return monto_limpio
        return monto


class ProyectoForm(forms.ModelForm):
    valor_proyecto = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'vTextField'})
    )
    monto_contrapartida = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'vTextField'})
    )

    class Meta:
        model = models.Proyecto
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            if self.instance.valor_proyecto is not None:
                self.initial['valor_proyecto'] = f"{self.instance.valor_proyecto:.2f}"
            if self.instance.monto_contrapartida is not None:
                self.initial['monto_contrapartida'] = f"{self.instance.monto_contrapartida:.2f}"

    def clean_valor_proyecto(self):
        valor = self.cleaned_data.get('valor_proyecto')
        if valor:
            return str(valor).replace('$', '').replace(',', '').strip()
        return valor

    def clean_monto_contrapartida(self):
        valor = self.cleaned_data.get('monto_contrapartida')
        if valor:
            return str(valor).replace('$', '').replace(',', '').strip()
        return valor