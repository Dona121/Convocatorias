# Correcciones y mejoras de calidad — `contenido/admin.py`

**Fecha:** 2026-06-21
**Archivo afectado:** `convocatorias_seguimiento/contenido/admin.py`
**Validación:** `python manage.py check` pasa sin errores nuevos (solo persiste la advertencia preexistente `staticfiles.W004` por la carpeta `static/` inexistente, ajena a estos cambios).

---

## 1. Bug — Etiqueta HTML mal cerrada (`</p>` en un `<span>`)

**Severidad:** baja (el navegador autocorrige, pero es HTML inválido).

En los badges de "Proyecto no postulado" se abría un `<span>` y se cerraba con `</p>`.
Aparecía **dos veces**:

- `SeccionProyectos.proyecto_postulado`
- `ProyectoAdmin.proyecto_postulado`

**Antes:**
```python
return format_html("<span style='{}...;'>{}</p>", base, no_postulado)
```

**Después:**
```python
return format_html("<span style='{}...;'>{}</span>", base, no_postulado)
```

---

## 2. Calidad — Métodos de permisos devolvían un `QuerySet` en lugar de un `bool`

**Severidad:** media (funcionaba por *truthiness*, pero ejecutaba una consulta extra a la BD y no era idiomático).

Afecta a los `has_view_permission` / `has_change_permission` / `has_add_permission` de los inlines
`BeneficiariosInline`, `ComentariosInline`, `FuentesInline` e `IndicadoresInline`.

**Antes:**
```python
return (
    request.user.is_superuser
    or request.user.groups.filter(name="Seguimiento de Proyectos")   # QuerySet
    or request.user.groups.filter(name="Administrador")              # QuerySet
)
```

**Después:**
```python
return (
    request.user.is_superuser
    or request.user.groups.filter(name="Seguimiento de Proyectos").exists()
    or request.user.groups.filter(name="Administrador").exists()
)
```

`.exists()` devuelve un `bool` real y genera una consulta `SELECT ... LIMIT 1` más barata.

---

## 3. Calidad — `list_display_links` con campos que no existían en `list_display`

**Severidad:** baja (configuración muerta/engañosa; no rompía porque Unfold sobreescribe
`get_list_display`, lo que omite el check `admin.E111` de Django).

### `ConvocatoriasAdmin`
**Antes:**
```python
list_display_links = ("id", "nombre_convocatoria", "nombre_convocatoria_recortada")
```
`"id"` y `"nombre_convocatoria"` no están en `list_display`, así que no hacían nada.

**Después:**
```python
list_display_links = ("nombre_convocatoria_recortada",)
```

### `ProyectoAdmin`
**Antes:**
```python
list_display_links = ("id", "nombre_proyecto")   # la columna real es "nombre_proyecto_recortado"
```

**Después:**
```python
list_display_links = ("id", "nombre_proyecto_recortado")
```

---

## 4. Rendimiento — N+1 de consultas en `numero_proyectos`

**Severidad:** media (una consulta `COUNT` por cada fila del listado de convocatorias).

`numero_proyectos` usaba `obj.proyecto_set.all().count()`. El `.count()` **ignora la caché de
`prefetch_related`** y lanza una consulta por fila. Además, la rama de superusuario en
`get_queryset` no precargaba la relación.

**Cambios:**

1. En `get_queryset`, la rama de superusuario ahora precarga la relación:
```python
if request.user.is_superuser:
    return qs.prefetch_related("proyecto_set")
```
(La rama de usuarios no superadmin ya usaba un `Prefetch` filtrado por dependencia.)

2. `numero_proyectos` usa `len()` sobre la relación ya precargada:
```python
def numero_proyectos(self, obj):
    # len() sobre la relación ya precargada con prefetch_related evita el N+1
    # (un .count() ignora la caché del prefetch y lanza una consulta por fila).
    proyectos = obj.proyecto_set.all()
    numero_proyectos = len(proyectos)
    ...
```

**Nota de comportamiento:** se mantiene la semántica previa. Para usuarios no superadmin el
conteo sigue reflejando únicamente los proyectos de sus dependencias (porque el `Prefetch` está
filtrado), y para superusuarios refleja todos. Se descartó deliberadamente la alternativa de
`annotate(Count("proyecto"))` porque, combinada con el `filter()` sobre la relación M2M
`dependencia` y el `.distinct()`, podía inflar el conteo por multiplicación de joins.

---

## Resumen

| # | Tipo | Ubicación | Estado |
|---|------|-----------|--------|
| 1 | Bug HTML (`</p>` → `</span>`) | `SeccionProyectos`, `ProyectoAdmin` | ✅ Corregido |
| 2 | `QuerySet` → `bool` (`.exists()`) | 4 inlines × 3 métodos de permiso | ✅ Corregido |
| 3 | `list_display_links` inválido | `ConvocatoriasAdmin`, `ProyectoAdmin` | ✅ Corregido |
| 4 | N+1 en `numero_proyectos` | `ConvocatoriasAdmin` | ✅ Corregido |
