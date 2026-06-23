# Seguimiento de Convocatorias — Gobernación de Sucre

Sistema para el **seguimiento de convocatorias de financiación y de los proyectos**
que se postulan a ellas (indicadores MGA, BPIN, fuentes de financiación, beneficiarios,
vigencias 2024–2027). Está pensado para una entidad pública colombiana: montos en COP,
zona horaria `America/Bogota` y catálogo de indicadores del Plan Indicativo.

El sistema tiene **dos caras**:

1. **Panel de administración** (`/es/admin/`) — registro y parametrización de todos los
   datos, construido sobre el admin de Django con [django-unfold](https://unfoldadmin.com/).
   Acceso con login y permisos por grupos/dependencia.
2. **Capa pública de reportes** (`/`) — consulta de solo lectura, sin login, con filtros
   dinámicos y gráficos. Ver [`docs/REPORTES.md`](docs/REPORTES.md).

---

## Stack

- **Python ≥ 3.13**, **Django 5.2**
- **PostgreSQL** (`dj-database-url` + `psycopg2-binary`)
- **django-unfold** — UI del admin
- **django-import-export** — importar/exportar datos (solo superusuarios)
- **django-guardian** — permisos a nivel de objeto
- **django-money** — campos monetarios (COP por defecto)
- **polars** — carga masiva de indicadores desde Excel
- **WhiteNoise** — servir estáticos; **gunicorn/waitress** — WSGI en producción
- Reportes públicos: **HTMX + Alpine.js** (filtros) y **Chart.js** (gráficos),
  vendorizados en `contenido/static/vendor/`
- Gestor de paquetes: **uv** (`pyproject.toml` + `uv.lock`)

---

## Estructura

```
convocatorias/                       <- raíz del repositorio
├─ pyproject.toml / uv.lock          <- dependencias (uv)
├─ requirements.txt                  <- export pip-compatible
├─ README.md                         <- este archivo
├─ docs/                             <- documentación del proyecto
│  ├─ REPORTES.md                    <- doc de la capa pública de reportes
│  ├─ MEJORAS_ADMIN.md / MEJORAS_CSS_SIDEBAR.md  <- notas de correcciones
│  ├─ GUIA_DISEÑO.md                 <- sistema de diseño institucional
│  └─ GuiaReporte.md                 <- spec original del reporte
└─ convocatorias_seguimiento/        <- proyecto Django (aquí está manage.py)
   ├─ manage.py
   ├─ .env                           <- secretos (NO versionado; ver .env.example)
   ├─ convocatorias_seguimiento/     <- paquete de configuración
   │  ├─ settings.py  urls.py  wsgi.py  asgi.py
   ├─ contenido/                     <- app principal
   │  ├─ models.py                   <- modelo de dominio
   │  ├─ admin.py                    <- todo el panel (django-unfold)
   │  ├─ views.py                    <- vistas públicas de reporte
   │  ├─ urls.py                     <- rutas de la capa pública
   │  ├─ reportes.py                 <- estados derivados + dinero (COP)
   │  ├─ forms.py
   │  ├─ management/commands/cargar_metas.py  <- import de indicadores MGA
   │  └─ static/  (css, logos, vendor)
   ├─ templates/reportes/            <- plantillas de la capa pública
   ├─ staticfiles/                   <- estáticos colectados (generado)
   └─ media/                         <- imágenes subidas (generado)
```

> La app del admin vive **enteramente en `admin.py`**; `views.py`/`urls.py` son la capa
> pública de reportes.

---

## Modelo de dominio (resumen)

- **`Convocatorias`** — entidad central (objetivo, fechas apertura/cierre, monto, sectores,
  ubicaciones, aliados, segmentos, público priorizado).
- **`Proyecto`** — se postula a una convocatoria (FK); lleva BPIN, dependencia, responsable,
  municipios y fechas de trazabilidad (postulación → subsanación → resultados).
- Colgando de cada proyecto: **`FuenteFinanciacion`** (comprometido/pagado por vigencia y
  fuente), **`Beneficiarios`** (por tipo), **`IndicadorMGA`** (meta del proyecto) y
  **`ComentariosProyectos`**.
- Tablas de parametrización: Dependencia, Responsable, Aliados, Segmentos, Sectores,
  Municipios, Ubicación, Vigencias, catálogos MGA y de fuentes.
- **`PerfilUsuario`** vincula cada usuario con una o varias dependencias (los no superadmin
  solo ven las suyas).

> Los **estados no se guardan**: el estado de una convocatoria (Próxima/Abierta/Cerrada/
> Fechas incompletas) y la etapa de un proyecto se **derivan** de las fechas. Esa lógica
> está en `contenido/reportes.py`.

---

## Puesta en marcha (desarrollo)

Requisitos: Python 3.13, una base PostgreSQL accesible y [uv](https://docs.astral.sh/uv/).

```bash
# 1. Dependencias
uv sync                      # o: pip install -r requirements.txt

# 2. Variables de entorno
cd convocatorias_seguimiento
cp .env.example .env         # y completa SECRET_KEY y DATABASE_URL
                             # (en producción, defínelas en el panel de Railway)

# 3. Base de datos
python manage.py migrate
python manage.py createsuperuser

# 4. Estáticos (necesario porque el proyecto corre con DEBUG=False)
python manage.py collectstatic --noinput

# 5. Servir
python manage.py runserver
```

- Reporte público: <http://127.0.0.1:8000/>
- Admin: <http://127.0.0.1:8000/es/admin/>

### ⚠️ Nota importante sobre estáticos

Este proyecto corre con **`DEBUG=False` incluso en local**, así que `runserver` **no**
sirve `/static/` automáticamente: lo hace **WhiteNoise desde `staticfiles/`**. Cada vez que
agregues o cambies un archivo estático (CSS, JS de `vendor/`, logos) **ejecuta de nuevo
`python manage.py collectstatic`** o el navegador recibirá 404 (Tailwind/Chart.js/HTMX no
cargarán). Los cambios en **plantillas** no requieren `collectstatic`.

---

## Variables de entorno

| Variable | Descripción |
|---|---|
| `SECRET_KEY` | Clave secreta de Django. |
| `DEBUG` | `True`/`False`. En este proyecto suele ir en `False`. |
| `DATABASE_URL` | Conexión PostgreSQL (formato `dj-database-url`). |

---

## Tareas frecuentes

```bash
# Cargar el catálogo de indicadores MGA desde un Excel (tabla tblPlanIndicativo_2)
python manage.py cargar_metas <ruta_al_excel.xlsx>

# Comprobaciones del sistema
python manage.py check
```

---

## Despliegue (producción)

- Servir con `gunicorn convocatorias_seguimiento.wsgi` (o `waitress` en Windows) detrás de un
  proxy con HTTPS. El proyecto ya confía en `X-Forwarded-Proto` y tiene `CSRF_TRUSTED_ORIGINS`.
- Ejecutar `collectstatic`; WhiteNoise sirve `staticfiles/`. Las imágenes de `media/`
  requieren servirse aparte (no las cubre WhiteNoise por defecto).
- Mantener `DEBUG=False` y un `SECRET_KEY` real fuera del control de versiones.

---

## Documentos relacionados

- [`docs/REPORTES.md`](docs/REPORTES.md) — capa pública de reportes (vistas, filtros, gráficos).
- [`docs/GUIA_DISEÑO.md`](docs/GUIA_DISEÑO.md) — sistema de diseño institucional (colores, tipografía).
- [`docs/GuiaReporte.md`](docs/GuiaReporte.md) — spec original del reporte.
- [`docs/MEJORAS_ADMIN.md`](docs/MEJORAS_ADMIN.md) y [`docs/MEJORAS_CSS_SIDEBAR.md`](docs/MEJORAS_CSS_SIDEBAR.md)
  — registro de correcciones aplicadas.
