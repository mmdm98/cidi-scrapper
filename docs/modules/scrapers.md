# Módulo: Scrapers

Dos scrapers casi idénticos en estructura, uno por tipo de dato.

---

## `turnero_scrapper.py` — Datos de turnero/atenciones

### Función principal

```python
fetch_and_save_data(cidi_cuil, cidi_password, centros_de_atencion, folder_path, date_from, date_until)
```

### Proceso

1. Inicializa ChromeDriver con opciones SSL (`--ignore-certificate-errors`, `--allow-running-insecure-content`)
2. Navega a `https://cidi.cba.gov.ar/portal-publico`
3. Hace login con CUIL + contraseña
4. Para cada CAC en `centros_de_atencion`:
   - Abre la URL del menú del CAC
   - Abre una segunda pestaña con el endpoint de la API de turnero
   - Espera a que cargue el `<pre>` con el JSON (timeout: 240s)
   - Guarda el HTML completo como `{nombre_cac}.html` en `folder_path`
5. Cierra el browser al terminar

### Endpoint consumido

```
https://turnero.cba.gov.ar/api/Reporte/Get_Turnos_Listado
    ?Id_Centro_Atencion={id}
    &FecDesde={YYYY-MM-DD}
    &FecHasta={YYYY-MM-DD}
```

### Output

Archivos HTML en `1_scrapped_html/`. El HTML contiene el JSON de respuesta dentro de un tag `<pre>`.

Ejemplo de nombre de archivo: `EPEC CENTRO DE ATENCION COMERCIAL ESTE.html`

### Parámetros

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `cidi_cuil` | str | CUIL del empleado (leído de `cidi_user_key.txt`) |
| `cidi_password` | str | Contraseña CIDI |
| `centros_de_atencion` | dict | `{id: nombre}` de los CACs a scrapear |
| `folder_path` | str | Ruta donde guardar los HTML |
| `date_from` | str o date | Fecha de inicio (YYYY-MM-DD) |
| `date_until` | str o date | Fecha de fin (YYYY-MM-DD) |

---

## `client_info_scrapper.py` — Datos de comentarios/supervisión

### Función principal

```python
fetch_and_save_comment_data(cidi_cuil, cidi_password, centros_de_atencion, folder_path, date_from, date_until)
```

### Diferencias respecto a `turnero_scrapper.py`

| Aspecto | turnero_scrapper | client_info_scrapper |
|---------|-----------------|---------------------|
| Endpoint | `Get_Turnos_Listado` | `Get_Supervision` |
| Timeout página | 240s | 120s |
| Sufijo en nombres de archivo | (ninguno) | `_CLIENT` |
| Output folder | `1_scrapped_html/` | `4_comments_scrapped_html/` |

### Endpoint consumido

```
https://turnero.cba.gov.ar/api/Turno/Get_Supervision
    ?filtro.fec_Desde={YYYY-MM-DD}
    &filtro.fec_Hasta={YYYY-MM-DD}
    &filtro.Id_Centro_Atencion={id}
    &filtro.Mostrar_Turnos_Con_Comentarios=N
```

### Output

Archivos HTML en `4_comments_scrapped_html/`.

Ejemplo: `EPEC CENTRO DE ATENCION COMERCIAL ESTE_CLIENT.html`

---

## Notas comunes

- Ambos scrapers usan el mismo patrón de login y apertura de pestañas
- El `time.sleep()` entre acciones está hardcodeado para dar tiempo al portal CIDI a responder
- Si el portal CIDI cambia su estructura de login o las URLs de API, ambos scrapers deben actualizarse
- Errores durante el scrapping son reportados vía `tx.py` (Telegram)
- La ruta del ChromeDriver está hardcodeada: `D:/Usuarios/mdelgadillo/Documents/chromeBrowser/chromedriver-win64/chromedriver.exe`
