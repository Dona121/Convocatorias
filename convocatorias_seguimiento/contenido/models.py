from django.db import models
from django.core.exceptions import ValidationError
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User

# Create your models here.


class Dependencia(models.Model):
    dependencia = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Dependencia"
        verbose_name_plural = "Dependencias"

    def __str__(self):
        return f"{self.dependencia}"
    
class Responsable(models.Model):
    responsable = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Responsable"
        verbose_name_plural = "Responsables"

    def __str__(self):
        return f"{self.responsable}"
    
class ClasificacionAliados(models.Model):
    clasificacion_aliado = models.CharField(max_length=150)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Clasificacion Aliado"
        verbose_name_plural = "Clasificacion Aliados"

    def __str__(self):
        return f"{self.clasificacion_aliado}"
    
class Aliados(models.Model):
    clasificacion = models.ForeignKey(
        ClasificacionAliados,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    aliado = models.CharField(max_length=200)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Aliado"
        verbose_name_plural = "Aliados"

    def __str__(self):
        return f"{self.aliado}"

class Segmentos(models.Model):
    segmento = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Segmento"
        verbose_name_plural = "Segmentos"

    def __str__(self):
        return f"{self.segmento}"


class Sectores(models.Model):
    codigo_sector = models.CharField(max_length=2)
    sector = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sector"
        verbose_name_plural = "Sectores"

    def __str__(self):
        return f"{self.codigo_sector} - {self.sector}"


class Municipios(models.Model):
    municipio = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Municipio"
        verbose_name_plural = "Municipios"

    def __str__(self):
        return f"{self.municipio}"

    
class Ubicacion(models.Model):
    ubicacion = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ubicacion"
        verbose_name_plural = "Ubicaciones"

    def __str__(self):
        return f"{self.ubicacion}"

class Convocatorias(models.Model):
    nombre_convocatoria = models.TextField()
    dependencia = models.ManyToManyField(
        Dependencia
    )
    aliados = models.ManyToManyField(
        Aliados,
        blank=True
    )
    objetivo = models.TextField(null=True)
    segmento = models.ManyToManyField(
        Segmentos
    ) 
    fecha_apertura = models.DateTimeField()
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    estado_monto = models.CharField(max_length=2,choices=[("ES","Especifica"),("NE","No especifica")],null=True)
    monto = MoneyField(decimal_places=4, max_digits=19,null=True,default_currency='COP',blank=True)
    sectores = models.ManyToManyField(
        Sectores
    )
    ubicacion = models.ManyToManyField(
        Ubicacion
    )
    enlace_convocatoria = models.CharField(max_length=250,null=True)
    enlace_del_actor = models.CharField(max_length=250,null=True)
    contacto = models.EmailField(max_length=100,null=True,blank=True)
    que_ofrece = models.TextField(null=True,blank=True)
    quienes_pueden_participar = models.TextField(null=True,blank=True)
    publico_priorizado = models.TextField(null=True,blank=True)
    imagen_convocatoria = models.ImageField(null=True,blank=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Convocatoria"
        verbose_name_plural = "Convocatorias"

    def __str__(self):
        return f"{self.nombre_convocatoria}" 

class Proyecto(models.Model):
    convocatoria = models.ForeignKey(
        Convocatorias,
        on_delete=models.CASCADE,
        null=True,
        blank=False
    )
    municipios = models.ManyToManyField(
        Municipios
    )
    aliados = models.ManyToManyField(
        Aliados,
        blank=True
    )
    nombre_proyecto = models.TextField()
    bpin = models.CharField(max_length=20)
    dependencia = models.ForeignKey(
        Dependencia,
        on_delete=models.CASCADE,
        null=True,
        blank=False
    )
    responsable = models.ForeignKey(
        Responsable,
        on_delete=models.CASCADE,
        null=True,
        blank=False
    )

    fecha_envio_postulacion_proyecto = models.DateTimeField(null=True,blank=True)
    fecha_solicitud_subsanacion_proyecto = models.DateTimeField(null=True,blank=True)
    fecha_envio_subsanciones_proyecto = models.DateTimeField(null=True,blank=True)
    fecha_publicacion_resultados_proyecto = models.DateTimeField(null=True,blank=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"

    def __str__(self):
        return f"{self.nombre_proyecto}" 
    

class ClasificacionBeneficiario(models.Model):
    tipo_beneficiario = models.CharField(max_length=40)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Beneficiario"
        verbose_name_plural = "Beneficiarios"

    def __str__(self):
        return f"{self.tipo_beneficiario}"


class Beneficiarios(models.Model):
    beneficiario = models.ForeignKey(
        ClasificacionBeneficiario,
        # 
        on_delete=models.CASCADE,
        null=True,
        blank=False
    )
    proyecto = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE,
        null=True,
        blank=False
    )
    numero_beneficiarios = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Beneficiario"
        verbose_name_plural = "Beneficiarios"


    def __str__(self):
        return f"{self.beneficiario}"
    
class ClasificacionIndicadorMGA(models.Model):
    codigo_meta = models.CharField(max_length=5,null=True,blank=False)
    codigo_indicador = models.CharField(max_length=9)
    nombre_indicador = models.TextField()
    decripcion = models.TextField(null=True,blank=True)
    medido_a_atraves_de = models.CharField(max_length=150,null=True,blank=True)
    meta_cuatrienio = models.DecimalField(max_digits=30, decimal_places=10)
    tipo_acumulacion = models.CharField(max_length=30,null=True,blank=True)
    responsable = models.CharField(max_length=200,null=True,blank=True)
    meta_fisica_esperada_2024 = models.DecimalField(max_digits=30, decimal_places=10,null=True,blank=True)
    meta_fisica_esperada_2025 = models.DecimalField(max_digits=30, decimal_places=10,null=True,blank=True)
    meta_fisica_esperada_2026 = models.DecimalField(max_digits=30, decimal_places=10,null=True,blank=True)
    meta_fisica_esperada_2027 = models.DecimalField(max_digits=30, decimal_places=10,null=True,blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Indicador"
        verbose_name_plural = "Indicadores"

    def __str__(self):
        return f"{self.codigo_meta} - {self.codigo_indicador} - {self.nombre_indicador}"
    
class ClasificacionVigencia(models.Model):
    vigencia = models.IntegerField(null=True,blank=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Vigencia"
        verbose_name_plural = "Vigencias"

    def __str__(self):
        return f"{self.vigencia}"
    
class IndicadorMGA(models.Model):
    vigencia = models.ForeignKey(
        ClasificacionVigencia,
        on_delete=models.CASCADE,
        null=True,
        blank=False
    )
    indicadores = models.ForeignKey(
        ClasificacionIndicadorMGA,
        on_delete=models.CASCADE,
        null=True,
        blank=False
    )
    proyecto = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE,
        null=True,
        blank=False
    )
    meta_proyecto = models.DecimalField(null=True,blank=False,decimal_places=5,max_digits=15)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Indicador"
        verbose_name_plural = "Indicadores"

    def __str__(self):
        return f"{self.indicadores}"
    
class ClasificacionFuenteFinanciacion(models.Model):
    class TipoFuente(models.TextChoices):
        NACIONAL = "NAC", "Nacional"
        INTERNACIONAL = "INT", "Internacional"

    class SubtipoFuente(models.TextChoices):
        RECURSOS_PROPIOS = "RP", "Recursos Propios"
        PGN = "PGN", "Presupuesto General de la Nación"
        REGALIAS = "SGR", "Sistema General de Regalías"
        CREDITO = "CRE", "Crédito"
        COOPERACION = "COO", "Cooperación Internacional"
        DONACION = "DON", "Donación"
        OTRO = "OTR", "Otro"

    tipo_de_fuente = models.CharField(
        max_length=3,
        choices=TipoFuente.choices,
        verbose_name="Tipo de Fuente"
    )
    subtipo = models.CharField(
        max_length=3,
        choices=SubtipoFuente.choices,
        null=True,
        blank=True,
        verbose_name="Subtipo de Fuente"
    )
    fuente = models.CharField(max_length=250,verbose_name="Fuente de Financiacion")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Clasificación Fuente de Financiación"
        verbose_name_plural = "Clasificación Fuentes de Financiación"

    def __str__(self):
        return f"{self.fuente}"
    
class FuenteFinanciacion(models.Model):
    vigencia = models.ForeignKey(
        ClasificacionVigencia,
        on_delete=models.CASCADE
    )
    fuente = models.ForeignKey(
        ClasificacionFuenteFinanciacion,
        on_delete=models.CASCADE,
        verbose_name="Fuente de Financiación"
    )
    proyecto = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE,
    )
    valor_comprometido = MoneyField(max_digits=19,decimal_places=4,verbose_name="Valor Comprometido",blank=True,null=True,default_currency="COP")
    valor_pagado = MoneyField(max_digits=19,decimal_places=4,verbose_name="Valor Pagado",blank=True,null=True,default_currency="COP")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Fuente de Financiación"
        verbose_name_plural = "Fuentes de Financiación"
        unique_together = [("vigencia","fuente","proyecto")]

    def __str__(self):
        return f"{self.fuente}"