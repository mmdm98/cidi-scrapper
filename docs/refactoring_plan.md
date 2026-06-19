# Plan de Refactoring — CIDI Scrapper

Documento de seguimiento del proceso de limpieza, reorganización y refactoring del proyecto. Las fases están ordenadas por prioridad y dependencia.

---

## Etapa 0: Limpieza inicial y documentación (completada 2026-06-18)

### Qué se hizo
- Eliminados 4 archivos basura de la raíz (`pruebasharepoint.py`, `salida.csv`, `output.txt`, `CACs_2025-01-27.csv`)
- Eliminadas 7 carpetas de prueba/backup (`pruebas/`, `7_pruebas_probadas/`, `8_pruebas_probadas/`, `9_pruebas_probadas/`, `72_prueba/`, `porLasDudas/`, `__pycache__/`)
- `DB_CACs_MANUALES_HISTORICO.csv` (45.6 MB) movido a `data/`
- Creada carpeta `docs/` con documentación completa del proyecto
- Configurado repositorio Git con `.gitignore`, `.gitattributes`, archivos `.example`, `.gitkeep` en carpetas de datos

---

## Etapa 1: Refactoring de código

### Fase 0 — Snapshot ✅ (completada 2026-06-19)
- Baseline registrado (commit `29f66c0`)
- Smoke-test checklist definido (ver abajo)

### Fase 1 — Bug fixes ✅ (completada 2026-06-19)
- `file_destructor.py`: botón "No" retornaba "Si" → corregido
- `file_destructor.py`: `os.chdir()` global reemplazado por rutas absolutas en `borrar_archivos`
- `menu.py`: opciones 6 y 7 eran invisibles → agregadas al menú CLI y rama Telegram
- `sharepoint.py`: 160+ líneas de código comentado (legacy shareplum + variante onelake) eliminadas; debug GETs eliminados; constantes de desarrollo sin uso eliminadas
- `csv_stacker.py`: type string `"COMM"` → `"COMMENTS"` para consistencia con onelake
- `onelake.py`: constantes `TYPE_CACS` y `TYPE_COMMENTS` agregadas

### Fase 2 — Eliminación de código muerto ✅ (completada 2026-06-19)
418 líneas eliminadas en 6 archivos:

| Archivo | Antes | Después | Qué se eliminó |
|---------|-------|---------|----------------|
| `csv_parser.py` | 195 | 52 | Versión anterior comentada + experimentos de lectura binaria y conversión txt |
| `tx.py` | 139 | 57 | Duplicado comentado de las 4 funciones + `import time` sin uso |
| `client_info_scrapper.py` | 170 | 82 | Imports comentados, selectores CSS obsoletos, dict de prueba + paths hardcodeados + notas |
| `csv_process.py` | 64 | 28 | Versión original comentada con paths hardcodeados |
| `turnero_scrapper.py` | 167 | 103 | Selectores CSS obsoletos, URLs alternativas comentadas, print de debug |
| `menu.py` | 87 | 75 | Variables sin uso (`black_chars`, `red_chars`), loop colorama comentado, imports `Fore`/`Back` |

### Fase 3 — Centralización de configuración ⬜ (pendiente)

**Objetivo:** Eliminar magic numbers y strings hardcodeados dispersos en múltiples archivos.

**Crear `config.py`** con todas las constantes del sistema:
```python
# Selenium
PAGE_LOAD_TIMEOUT_TURNERO   = 240
PAGE_LOAD_TIMEOUT_COMMENTS  = 120
SLEEP_TAB_OPEN   = 3.5
SLEEP_TAB_CLOSE  = 1.5
SLEEP_LOGIN      = 1.0
PAGE_SIZE_COMMENTS = 10000

# URLs CIDI / Turnero
CIDI_LOGIN_URL = "https://cidi.cba.gov.ar/portal-publico"
TURNERO_LISTADO_URL_TMPL    = "...{id_centro}...{desde}...{hasta}..."
TURNERO_SUPERVISION_URL_TMPL = "...{id_centro}...{desde}...{hasta}..."

# OneLake
ONELAKE_WORKSPACE_NAME     = "Protelem - Premium"
ONELAKE_DATA_PATH_CACS     = "LH_CIDI.Lakehouse/Files/CACs"
ONELAKE_DATA_PATH_COMMENTS = "LH_CIDI.Lakehouse/Files/CACs_Comments"
ONELAKE_TYPE_CACS          = "CACS"
ONELAKE_TYPE_COMMENTS      = "COMMENTS"

# SharePoint
SHAREPOINT_SITE_NAME     = "PROTELEM-INDICADORES"
SHAREPOINT_BASE_PATH     = "https://epeccba.sharepoint.com/"
SHAREPOINT_FOLDER_TURNERO  = "Documentos compartidos/m_actividad_turnero_cidi"
SHAREPOINT_FOLDER_COMMENTS = "Documentos compartidos/m_comentarios_turnero_cidi"
```

**Agregar línea 9 a `paths.txt`** con la ruta de ChromeDriver (actualmente hardcodeada en ambos scrapers). Actualizar `paths.example.txt` y el check `len(paths) == 8` → `== 9` en `cidi_scrapper.py`.

**Externalizar credenciales de Telegram (SEC-01):** Crear `tx_credentials.txt` (mismo formato que `cidi_user_key.txt`). Agregar al `.gitignore`. Modificar `tx.py` para cargarlas con `read_credentials()`.

**Archivos modificados:** `config.py` (nuevo), `onelake.py`, `cidi_scrapper.py`, `tx.py`, `paths.txt`, `paths.example.txt`, `.gitignore`

### Fase 4 — Consolidar scrapers ⬜ (pendiente)

**Objetivo:** Eliminar ~85% de duplicación entre `turnero_scrapper.py` y `client_info_scrapper.py`.

**Crear `scrapper_base.py`** con la lógica común de Selenium:
```python
def _init_driver(chromedriver_path, user_agent=None) -> WebDriver
def _login(driver, cuil, password) -> None
def _open_tab(driver, url) -> None
def _close_extra_tabs(driver, count=2) -> None

def fetch_cac_data(
    cuil, password, centros, folder_path, desde, hasta,
    chromedriver_path, page_timeout,
    build_data_url_fn,   # callable(id_centro, desde, hasta) → str
    build_nav_url_fn,    # callable(id_centro) → str
    build_menu_url_fn,   # callable(id_centro) → str
    file_suffix="",
    use_refresh=False,
    user_agent=None,
) -> None
```

**Reescribir scrapers como wrappers de ~30 líneas** que solo pasan sus diferencias (endpoint, timeout, sufijo de archivo, use_refresh).

**Actualizar 5 call sites en `cidi_scrapper.py`** para pasar `chromedriver_path=chromedriver_path`.

**Archivos modificados:** `scrapper_base.py` (nuevo), `turnero_scrapper.py`, `client_info_scrapper.py`, `cidi_scrapper.py`

> ⚠️ Esta fase requiere verificación con credenciales reales — ejecutar opción `3` con un solo CAC antes de dar por buena.

### Fase 5 — Limpiar `onelake.py` ⬜ (pendiente)

**Objetivo:** Eliminar el triple `if cacs_or_comm == "CACS": ... else: ...` redundante.

Colapsar a un dict de dispatch:
```python
_PATHS = {
    TYPE_CACS:     DATA_PATH_CACs,
    TYPE_COMMENTS: DATA_PATH_COMMENTS,
}
data_path = _PATHS[cacs_or_comm]  # KeyError si el tipo no existe → detección temprana
```

Agregar `local_folder: str` como parámetro para eliminar los paths hardcodeados internos. Actualizar callers en `csv_stacker.py` y `csv_process.py`.

**Archivos modificados:** `onelake.py`, `csv_stacker.py`, `csv_process.py`

### Fase 6 — Sistema de logging ⬜ (pendiente)

**Objetivo:** Reemplazar los ~55 `print()` de feedback del sistema por logging estructurado con archivo persistente.

**Crear `logger.py`:**
```python
def setup_logging(level=logging.INFO) -> None:
    # Console handler
    # RotatingFileHandler → cidi.log (5 MB max, 3 backups)
```

En cada módulo:
```python
import logging
logger = logging.getLogger(__name__)
```

Llamar `setup_logging()` una vez al inicio de `cidi_scrapper.py`. No reemplazar los `print()` del menú (son UI intencional).

**Archivos modificados:** `logger.py` (nuevo) + todos los módulos activos

### Fase 7 — Type hints y docstrings ⬜ (pendiente)

Agregar type hints a todas las funciones públicas y docstring de una línea. Orden de prioridad: `scrapper_base.py` → `onelake.py` → `csv_stacker.py` → resto.

Eliminar definitivamente `cambiar_directorio()` de `file_destructor.py` (marcada `DEPRECATED` en Fase 1, ya sin callers).

### Fase 8 — Actualizar docs/ ⬜ (pendiente)

- Agregar `config.py`, `scrapper_base.py` y `logger.py` a `docs/architecture.md`
- Marcar como resueltos los items de `docs/known_issues.md` corregidos en fases anteriores
- Actualizar `docs/modules/scrapers.md` con el nuevo módulo base
- Documentar la línea 9 de `paths.txt` en `docs/setup.md`
- Actualizar `docs/modules/utilities.md` con el nuevo `logger.py`

---

## Resumen de estado

| Fase | Descripción | Estado | Impacto |
|------|-------------|--------|---------|
| 0 (limpieza inicial) | Archivos/carpetas basura, docs/, Git | ✅ | Organización |
| 1 (bugs) | 5 bugs corregidos, sharepoint limpio | ✅ | Corrección |
| 2 (código muerto) | −418 líneas en 6 archivos | ✅ | Legibilidad |
| 3 (config centralizado) | `config.py`, credenciales Telegram | ⬜ | Mantenibilidad |
| 4 (scrapers unificados) | `scrapper_base.py`, wrappers ~30 líneas | ⬜ | −130 líneas, no duplicación |
| 5 (onelake limpio) | Dict dispatch, `local_folder` param | ⬜ | Robustez |
| 6 (logging) | `logger.py`, reemplazar print() | ⬜ | Observabilidad |
| 7 (types + docs) | Type hints, docstrings | ⬜ | Mantenibilidad |
| 8 (docs actualizada) | architecture, known_issues, modules | ⬜ | Documentación |

**Líneas netas a eliminar en fases restantes (3–5):** ~130 adicionales  
**Total eliminado hasta ahora:** ~580 líneas (Etapa 0 + Fases 1–2)

---

## Smoke-test checklist

Ejecutar después de cada fase para verificar que no se rompió nada:

```bash
# Test 1 — importación limpia de todos los módulos
python -c "import turnero_scrapper, client_info_scrapper, csv_parser, csv_stacker, \
           csv_process, credentials, menu, sharepoint, onelake, file_destructor, tx"

# Test 2 — menú carga y sale limpio
python cidi_scrapper.py   # → ingresar 5 para salir

# Test 3 — borrar todo sin crash
python cidi_scrapper.py   # → ingresar 0 (carpetas pueden estar vacías, no debe tirar error)
```
