# Documentación de usuario YUBUS

Repositorio autónomo de documentación de usuario construido con MkDocs Material.
Las guías publicadas están en `docs/`, la navegación en `mkdocs.yml` y el
inventario de cobertura en `documentation/inventory.yml`.

## Levantar localmente

### 1. Verificar Python

```bash
python3 --version
```

### 2. Crear y activar el entorno virtual

```bash
python3 -m venv .venv && source .venv/bin/activate
```

### 3. Instalar dependencias fijadas

```bash
pip install -r requirements.txt
```

### 4. Ejecutar MkDocs

```bash
mkdocs serve --dev-addr 127.0.0.1:8000
```

Abrí <http://127.0.0.1:8000/>. El servidor queda limitado a este equipo. La
ruta pública se aplica solo durante el build de producción.

## Validación local

```bash
.venv/bin/python scripts/check_inventory.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/mkdocs build --strict --clean
```

## Evidencia de la aplicación

Para investigar una guía respaldada por código, definí un checkout local de
solo lectura sin cargarlo desde la shell:

```bash
cp .env.example .env
# Editá YUBUS_SOURCE_DIR con una ruta absoluta local.
```

La variable de entorno tiene prioridad sobre `.env`. El helper
`scripts/source_config.py` lee `.env` como datos, nunca lo ejecuta, y acepta solo
`YUBUS_SOURCE_DIR` cuando indica un directorio absoluto existente. El archivo
`.env` no se versiona y nunca debe contener secretos. Los criterios de evidencia
y captura están en `AGENTS.md` y `documentation/`.

El contrato del inventario está en `documentation/inventory.schema.json`.
`scripts/check_inventory.py` aplica sus campos requeridos y restricciones de
tipos, unicidad y rutas; no implementa JSON Schema Draft 2020-12 completo.

## Publicación

El workflow de producción se activa por `push` a `main` o manualmente desde
GitHub Actions. Publica solamente en la URL fija
`https://yubus.puyu.pe/manual/` y requiere los secrets del Environment
`production` y, opcionalmente, `DEPLOY_PORT`. Antes de publicarlo, un release de
la aplicación debe crear `shared/manual` y `public/manual -> shared/manual`.
No modifica Laravel ni la configuración del servidor. Consultá
`documentation/production-runbook.md` antes de activarlo.

# Referencias

- [Instalación mkdocs](https://www.mkdocs.org/user-guide/installation/) 
- [Documentación Material Theme](https://squidfunk.github.io/mkdocs-material/creating-your-site/)
