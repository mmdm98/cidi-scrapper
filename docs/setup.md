# Guía de Instalación y Configuración

## 1. Python

Versión recomendada: **Python 3.13** (probado y en uso).

## 2. Dependencias

```bash
pip install selenium beautifulsoup4 pandas azure-storage-filedatalake azure-identity requests colorama
```

| Paquete | Uso |
|---------|-----|
| `selenium` | Automatización del browser para scrapping CIDI |
| `beautifulsoup4` | Parsing del HTML descargado |
| `pandas` | Manipulación de DataFrames CSV |
| `azure-storage-filedatalake` | Cliente para Azure Data Lake / OneLake |
| `azure-identity` | Autenticación Microsoft (InteractiveBrowserCredential) |
| `requests` | Llamadas HTTP (Graph API, Telegram) |
| `colorama` | Colores en la terminal (menú) |

## 3. ChromeDriver

El scrapper usa Selenium con Google Chrome.

1. Verificar la versión de Chrome instalada: `chrome://settings/help`
2. Descargar ChromeDriver de la misma versión: https://chromedriver.chromium.org/downloads
3. Descomprimir en: `D:/Usuarios/<tu_usuario>/Documents/chromeBrowser/chromedriver-win64/`

> **Nota:** La ruta está hardcodeada en `turnero_scrapper.py` y `client_info_scrapper.py`. Si cambiás la ruta, actualizá ambos archivos.

## 4. Archivo `paths.txt`

El archivo `paths.txt` debe tener **exactamente 8 líneas**, una ruta por línea, en este orden:

```
D:/ruta/a/cidi_user_key.txt
D:/ruta/a/shpt_user_key.txt
D:/ruta/al/proyecto/cidi/1_scrapped_html
D:/ruta/al/proyecto/cidi/2_scrapped_csv
D:/ruta/al/proyecto/cidi/3_filtered_data
D:/ruta/al/proyecto/cidi/4_comments_scrapped_html
D:/ruta/al/proyecto/cidi/5_comments_scrapped_csv
D:/ruta/al/proyecto/cidi/6_comments_filtered_data
```

| Línea | Variable en código | Descripción |
|-------|-------------------|-------------|
| 0 | `cidi_credentials_file` | Credenciales CIDI |
| 1 | `sharepoint_credentials_file` | Credenciales SharePoint |
| 2 | `folder_path` | HTML de turnero (entrada) |
| 3 | `output_folder` | CSV de turnero (intermedio) |
| 4 | `filtered_folder` | CSV filtrado de turnero (salida) |
| 5 | `comment_folder_path` | HTML de comentarios (entrada) |
| 6 | `comment_output_folder` | CSV de comentarios (intermedio) |
| 7 | `comment_filtered_folder` | CSV filtrado de comentarios (salida) |

## 5. Archivos de credenciales

### `cidi_user_key.txt`
Dos líneas: CUIL del empleado (sin guiones) y contraseña CIDI.
```
20123456789
mi_contraseña
```

### `shpt_user_key.txt`
Dos líneas: email corporativo y contraseña SharePoint.
```
usuario@epec.com
mi_contraseña
```

> **Advertencia de seguridad:** Estos archivos contienen credenciales en texto plano. No los subas a ningún repositorio. Agregá sus nombres a `.gitignore` si usás Git.

## 6. Autenticación Microsoft (OneLake / SharePoint)

`onelake.py` y `sharepoint.py` usan `InteractiveBrowserCredential` de Azure Identity. La primera vez que se suba un archivo, se abrirá un browser para autenticación MFA con la cuenta corporativa de Microsoft.

No se necesita configurar nada adicional — el token se cachea automáticamente.

## 7. Token de Telegram (opcional)

`tx.py` envía alertas de error a un bot de Telegram. El token y el chat ID están hardcodeados directamente en el archivo (ver [known_issues.md](known_issues.md) para el detalle del riesgo de seguridad). Si no se usa Telegram, las funciones de `tx.py` solo se llaman en caso de errores durante el scrapping.

## 8. Verificar la instalación

```bash
python cidi_scrapper.py
```

Debe aparecer el menú con el logo EPEC. Seleccionar opción `5` para salir sin hacer nada.
