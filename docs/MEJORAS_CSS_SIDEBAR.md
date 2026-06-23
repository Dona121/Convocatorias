# Correcciones de CSS — sidebar y `STYLES` de Unfold

**Fecha:** 2026-06-21
**Archivos afectados:**
- `convocatorias_seguimiento/convocatorias_seguimiento/settings.py` (`UNFOLD["STYLES"]`)
- `convocatorias_seguimiento/contenido/static/css/sidebar.css`

**Validación:** `python manage.py check` pasa sin errores nuevos (persiste solo la advertencia
preexistente `staticfiles.W004`, ajena a estos cambios).

---

## Contexto: cómo se cargan estos estilos

Unfold inyecta las hojas de `UNFOLD["STYLES"]` en `unfold/layouts/skeleton.html`:

```django
{% for style in styles %}
    <link href="{{ style }}" rel="stylesheet">
{% endfor %}
...
<link href="{% static 'unfold/css/styles.css' %}" rel="stylesheet">
```

Dos consecuencias importantes:
1. El valor de cada entrada de `STYLES` se usa **tal cual** como `href`. Si no es una URL
   absoluta (p. ej. la que produce `static()`), el navegador la resuelve **relativa a la
   página actual**.
2. Los estilos personalizados se cargan **antes** que `unfold/css/styles.css`. Por eso
   `sidebar.css` necesita `!important` para no ser sobreescrito por Unfold (es esperado, no es bug).

> Verificado además que el selector `#nav-sidebar-inner` de `sidebar.css` corresponde al
> elemento real `<nav id="nav-sidebar-inner">` de `unfold/helpers/navigation.html`. El sidebar
> sí recibe los estilos.

---

## 1. Bug — `convocatorias.css` cargado con URL relativa (404 en todo el admin)

**Severidad:** media (genera un 404 en cada página del admin; ruido en consola).

`settings.py` → `UNFOLD["STYLES"]`:

**Antes:**
```python
"STYLES" : [
    lambda request: static("css/sidebar.css"),
    lambda request: "css/convocatorias.css",   # URL relativa → 404
],
```
La segunda entrada devolvía la cadena literal `"css/convocatorias.css"`. En una página como
`/es/admin/contenido/convocatorias/`, el navegador pedía
`/es/admin/contenido/convocatorias/css/convocatorias.css` → **404**.

**Después:**
```python
"STYLES" : [
    lambda request: static("css/sidebar.css"),
    lambda request: static("css/convocatorias.css"),   # → /static/css/convocatorias.css
],
```

> Nota: la tarjeta de convocatoria (`templates/convocatoria.html`) ya cargaba `convocatorias.css`
> correctamente vía `{% static 'css/convocatorias.css' %}` en su bloque `extrahead`, así que el
> estilo de la tarjeta nunca estuvo roto; lo que fallaba era esta entrada global de `STYLES`.

---

## 2. Bug — Selector `:not()` malformado en `sidebar.css`

**Severidad:** media (la regla podía invalidarse o no hacer lo previsto).

Menú desplegable del footer del sidebar:

**Antes:**
```css
#nav-sidebar-inner nav.absolute button:not([type="submit"]#logout-form button),
```
El argumento de `:not()` (`[type="submit"]#logout-form button`) incluía un combinador
descendiente. En navegadores antiguos invalida toda la regla; en los modernos nunca coincide,
por lo que la exclusión no funcionaba como se esperaba (la intención era "todos los botones
excepto el de cerrar sesión").

**Después:**
```css
#nav-sidebar-inner nav.absolute button:not(#logout-form button),
```

---

## 3. Limpieza — `#nav-sidebar-inner h2` definido 3 veces con valores contradictorios

**Severidad:** baja (reglas muertas; el resultado visual no cambia, pero confundía el mantenimiento).

`h2` del sidebar estaba definido en tres lugares y, por orden de cascada, solo ganaba el último.
Las dos primeras definiciones eran código muerto:

- Bloque "SECTION HEADERS": pedía MAYÚSCULAS, `0.7rem`, color oscuro → **anulado**.
- Bloque "Restaurar semibold" (`font-weight: 700`) → **anulado** por el `font-weight: 600` final.

**Acción:** se eliminaron las dos reglas muertas y se dejó una **única** definición consolidada
(la del bloque "SEPARADORES DE SECCIÓN"), que es la que realmente aplica:

```css
#nav-sidebar-inner h2 {
    color: oklch(96% 0.015 260) !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.01em !important;
    text-transform: none !important;
    padding: 8px 12px !important;
    margin: 0 !important;
}
```
En el lugar de la regla eliminada se dejó un comentario apuntando a esta definición consolidada.

---

## Pendiente / observaciones (no corregidas)

- **`sidebar.css` contiene CSS global** (reglas `*`, `body`, `input`, `td`, `thead th`, etc.)
  que afectan a todo el admin, no solo al sidebar. Funciona, pero el nombre del archivo es
  engañoso. Si se quiere ordenar, ese CSS global podría moverse a `custom_admin.css`.
- **`collectstatic`:** en producción WhiteNoise sirve desde `STATIC_ROOT` (`staticfiles/`), que
  contiene copias *previas* de estos CSS. Tras estos cambios conviene ejecutar
  `python manage.py collectstatic` para regenerarlas. En desarrollo (`runserver`) no hace falta:
  los finders leen directamente de `contenido/static/`.

---

## Resumen

| # | Tipo | Ubicación | Estado |
|---|------|-----------|--------|
| 1 | URL relativa → 404 (`static()`) | `settings.py` → `UNFOLD["STYLES"]` | ✅ Corregido |
| 2 | Selector `:not()` malformado | `sidebar.css` (menú footer) | ✅ Corregido |
| 3 | `h2` triplicado con reglas muertas | `sidebar.css` | ✅ Consolidado |
