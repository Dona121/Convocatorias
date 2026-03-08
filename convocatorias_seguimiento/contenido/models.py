from django.db import models
from django.core.exceptions import ValidationError

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
    
class Aliados(models.Model):
    aliado = models.CharField(max_length=100)
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


class Estado(models.Model):
    estado = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"

    def __str__(self):
        return f"{self.estado}" 


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
    segmento = models.ManyToManyField(
        Segmentos
    )
    # 
    fecha_apertura = models.DateTimeField()
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    estado = models.ForeignKey(
        Estado,
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )
    monto = models.DecimalField(decimal_places=10, max_digits=30)
    sectores = models.ManyToManyField(
        Sectores
    )
    ubicacion = models.ManyToManyField(
        Ubicacion
    )
    # 
    contacto = models.CharField(max_length=100)
    que_ofrece = models.TextField(null=True,blank=True)
    quienes_pueden_participar = models.TextField(null=True,blank=True)
    publico_priorizado = models.TextField(null=True,blank=True)
    
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
    nombre_proyecto = models.TextField()
    valor_proyecto = models.DecimalField(max_digits=30, decimal_places=10)
    bpin = models.CharField(max_length=20)
    monto_contrapartida = models.DecimalField(max_digits=30, decimal_places=10,null=True,blank=True)
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
    # 
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