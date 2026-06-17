# CIDI Scrapper — Documentación General

## ¿Qué hace este proyecto?

Automatiza la descarga diaria de datos del **portal CIDI** (Córdoba Digital) para los Centros de Atención Comercial (CACs) de EPEC. El flujo completo:

1. Autenticación en el portal CIDI con credenciales de empleado
2. Descarga de datos de **turnero** (citas/atenciones) y/o **comentarios** de clientes por CAC
3. Conversión de HTML a CSV
4. Clasificación y filtrado de datos
5. Subida automática a **Microsoft Fabric OneLake** y/o **SharePoint**

Cubre ~45 CACs distribuidos en toda la provincia de Córdoba.

---

## Prerrequisitos

- **Python 3.x** (probado con 3.13)
- **Google Chrome** + **ChromeDriver** compatible con la versión instalada
  - Ruta actual hardcodeada: `D:/Usuarios/mdelgadillo/Documents/chromeBrowser/chromedriver-win64/chromedriver.exe`
  - Ver [setup.md](setup.md) para instrucciones de instalación
- Cuenta **Microsoft** con acceso a Fabric OneLake (autenticación interactiva via browser)

### Paquetes Python

```
pip install selenium beautifulsoup4 pandas azure-storage-filedatalake azure-identity requests colorama
```

---

## Configuración inicial

Ver [setup.md](setup.md) para la guía completa. Resumen:

1. Crear `paths.txt` con 8 rutas (ver setup.md)
2. Crear `cidi_user_key.txt` con CUIL y contraseña CIDI
3. Crear `shpt_user_key.txt` con usuario y contraseña SharePoint
4. Verificar que ChromeDriver esté en la ruta correcta

---

## Cómo ejecutar

```bash
python cidi_scrapper.py
```

Se despliega un menú interactivo con las siguientes opciones:

| Opción | Descripción |
|--------|-------------|
| `0` | Borrar todos los archivos temporales (HTML y CSV intermedios) |
| `1` | Subir el archivo filtrado existente a SharePoint |
| `2` | Descargar datos de **ayer** (turnero + opcionalmente comentarios) y subir a OneLake |
| `3` | Descargar datos de una **fecha específica** (solo turnero) |
| `4` | Descargar datos de comentarios de una **fecha específica** |
| `5` | Salir |
| `6` | Modo dev: múltiples fechas individuales, sube cada una a OneLake |
| `7` | Modo dev: rango de fechas (desde/hasta), sube a OneLake |

---

## Flujo de datos

```
Portal CIDI (turnero API)
    │
    ├─ [turnero_scrapper.py] ──► 1_scrapped_html/     (HTML bruto por CAC)
    │
    ├─ [csv_parser.py]       ──► 2_scrapped_csv/      (CSV por CAC)
    │
    └─ [csv_stacker.py]      ──► 3_filtered_data/     (un CSV con todos los CACs)
                                      │
                                      └─ [onelake.py] ──► Microsoft Fabric

Portal CIDI (comentarios API)
    │
    ├─ [client_info_scrapper.py] ──► 4_comments_scrapped_html/
    │
    ├─ [csv_parser.py]           ──► 5_comments_scrapped_csv/
    │
    ├─ [csv_stacker.py]          ──► 6_comments_filtered_data/
    │
    ├─ [csv_process.py]          (limpia columnas innecesarias)
    │
    └─ [sharepoint.py / onelake.py] ──► SharePoint / Microsoft Fabric
```

---

## Estructura de archivos del proyecto

```
cidi/
├── cidi_scrapper.py          ← PUNTO DE ENTRADA principal
├── turnero_scrapper.py       ← Scrapper de datos de turnero (Selenium)
├── client_info_scrapper.py   ← Scrapper de comentarios (Selenium)
├── csv_parser.py             ← Convierte HTML → CSV
├── csv_stacker.py            ← Fusiona y clasifica CSVs
├── csv_process.py            ← Limpia columnas de comentarios
├── credentials.py            ← Lee credenciales y rutas desde archivos .txt
├── menu.py                   ← Interfaz de menú CLI
├── sharepoint.py             ← Upload a SharePoint vía Graph API
├── onelake.py                ← Upload a Azure OneLake
├── file_destructor.py        ← Limpieza de archivos temporales
├── tx.py                     ← Notificaciones por Telegram
├── paths.txt                 ← Configuración de rutas (no subir al repo)
├── cidi_user_key.txt         ← Credenciales CIDI (no subir al repo)
├── shpt_user_key.txt         ← Credenciales SharePoint (no subir al repo)
├── data/                     ← Datos de referencia históricos
├── docs/                     ← Esta documentación
├── 1_scrapped_html/          ← HTML temporal (se limpia en cada ejecución)
├── 2_scrapped_csv/           ← CSV temporal (se limpia en cada ejecución)
├── 3_filtered_data/          ← OUTPUT: datos de turnero por fecha
├── 4_comments_scrapped_html/ ← HTML temporal de comentarios
├── 5_comments_scrapped_csv/  ← CSV temporal de comentarios
└── 6_comments_filtered_data/ ← OUTPUT: comentarios clasificados por fecha
```

---

## Módulos — documentación detallada

- [Scrapers (turnero + comentarios)](modules/scrapers.md)
- [Procesamiento CSV](modules/processing.md)
- [Integración cloud (SharePoint + OneLake)](modules/integration.md)
- [Utilidades (credenciales, menú, limpieza, Telegram)](modules/utilities.md)

## Referencias

- [Centros de Atención Comercial (CACs)](centros_de_atencion.md)
- [Guía de instalación](setup.md)
- [Problemas conocidos y TODOs](known_issues.md)
