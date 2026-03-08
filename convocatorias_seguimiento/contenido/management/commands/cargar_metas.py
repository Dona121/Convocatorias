import polars as pl
from contenido.models import ClasificacionIndicadorMGA
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Migrar datos de excel a indicadores MGA"

    def add_arguments(self, parser):
        parser.add_argument(
            "ruta_excel",
            type=str,
            help="Ruta al archivo Excel con los indicadores MGA"
        )

    def handle(self, *args, **options):
        ruta = options["ruta_excel"]
        self.stdout.write(f"Leyendo archivo: {ruta}")

        try:
            df = pl.read_excel(ruta, table_name="tblPlanIndicativo_2")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error al leer el archivo Excel: {e}"))
            return

        lista = []
        errores = 0

        for row in df.iter_rows(named=True):
            instancia = ClasificacionIndicadorMGA(
                codigo_meta=row["codigo meta"],
                codigo_indicador=row["codigo indicador"],
                nombre_indicador=row["nombre indicador"],
                decripcion=row["descripcion"], 
                medido_a_atraves_de=row["medido a traves de"],
                meta_cuatrienio=row["meta de cuatrienio"],
                tipo_acumulacion=row["tipo acumulacion"],
                responsable=row["responsable"],
                meta_fisica_esperada_2024=row["meta 2024"],
                meta_fisica_esperada_2025=row["meta 2025"],
                meta_fisica_esperada_2026=row["meta 2026"],
                meta_fisica_esperada_2027=row["meta 2027"],
            )
            try:
                instancia.clean()
                lista.append(instancia)
            except ValidationError as e:
                errores += 1
                self.stdout.write(
                    self.style.ERROR(f"Error de validación en fila {row.get('codigo indicador', '?')}: {e}")
                )

        if not lista:
            self.stdout.write(self.style.WARNING("No hay registros válidos para insertar."))
            return

        try:
            ClasificacionIndicadorMGA.objects.bulk_create(lista)
            self.stdout.write(
                self.style.SUCCESS(f"Se crearon {len(lista)} indicadores correctamente.")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error al insertar en base de datos: {e}"))
            return

        if errores:
            self.stdout.write(
                self.style.WARNING(f"{errores} filas fueron omitidas por errores de validación.")
            )