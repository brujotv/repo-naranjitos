# Cómo añadir addons al repositorio

## Estructura que usa tu repo

- **addons.xml** y **addons.xml.md5** se generan con `repo_prep.py`.
- Cada addon es una **carpeta** cuyo nombre es el **id del addon** (ej: `plugin.video.miaddon`).
- Dentro de cada carpeta debe haber un **addon.xml** y el resto de archivos del addon.
- El script genera también el **ZIP** de cada addon: `addon.id-version.zip`.

## Pasos para añadir un addon nuevo

### 1. Crear la carpeta del addon

Dentro de **Repositorio**, crea una carpeta con el **id exacto** del addon (el mismo que pongas en `id="..."` del addon.xml).

Ejemplo: para un addon con `id="plugin.video.ejemplo"`:

```
Repositorio/
  plugin.video.ejemplo/   ← carpeta nueva
    addon.xml
    default.py
    icon.png
    fanart.jpg
    ...
```

### 2. Poner los archivos del addon

- **addon.xml** es obligatorio (con `id`, `version`, `name`, `provider-name`, extension points, etc.).
- Incluye también icon.png, fanart, código Python, etc.
- Opcional: **changelog.txt** (el script lo renombrará a `changelog-x.y.z.txt`).

### 3. Regenerar addons.xml y los ZIP

Abre una terminal en la carpeta **Repositorio** (donde está `repo_prep.py`) y ejecuta:

```bash
cd c:\Users\carlos\Documents\GitHub\repo-naranjitos\Repositorio
python repo_prep.py
```

O si usas Python 3 y el script da errores (el script está en Python 2), puedes usar:

```bash
python2 repo_prep.py
```

El script:

- Recorre todas las carpetas que tengan `addon.xml`.
- Actualiza **addons.xml** con la información de cada addon.
- Genera **addons.xml.md5**.
- Si `compress_addons = True`, crea **addon.id-version.zip** en cada carpeta y deja en la carpeta solo: addon.xml, icon, fanart, changelog y el zip.

### 4. Subir los cambios a GitHub

Haz commit y push de:

- La carpeta nueva del addon (con addon.xml y el .zip generado).
- Los archivos **addons.xml** y **addons.xml.md5** actualizados.

Así Kodi podrá ver el addon en el repo y descargar `datadir/addon.id/addon.id-version.zip`.

## Resumen rápido

| Paso | Acción |
|------|--------|
| 1 | Crear carpeta `Repositorio/mi.addon.id/` |
| 2 | Copiar ahí addon.xml y todos los archivos del addon |
| 3 | Ejecutar `python repo_prep.py` desde `Repositorio` |
| 4 | Subir a GitHub la carpeta del addon + addons.xml + addons.xml.md5 |

## Nota sobre repo_prep.py

El script está escrito para **Python 2** (usa `print` sin paréntesis y el módulo `md5`). Si no tienes Python 2, puede que tengas que adaptar el script a Python 3 o usar un entorno con Python 2 solo para generar el repo.
