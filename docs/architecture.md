# Arquitectura del Sistema

## Visión general

El proyecto es un **pipeline ETL automatizado** que extrae datos del portal CIDI, los transforma y los carga en Microsoft Fabric. Se ejecuta manualmente desde la línea de comandos.

---

## Diagrama de flujo — Turnero (datos de atenciones)

```
┌─────────────────────────────────────────────────────────┐
│  cidi_scrapper.py  (orquestador principal)              │
└───────────────────────┬─────────────────────────────────┘
                        │
          ┌─────────────▼──────────────┐
          │   turnero_scrapper.py       │
          │   (Selenium + Chrome)       │
          │                            │
          │  1. Login en CIDI          │
          │  2. Por cada CAC:          │
          │     GET /api/Reporte/      │
          │     Get_Turnos_Listado     │
          │  3. Guarda HTML bruto      │
          └─────────────┬──────────────┘
                        │ HTML (1 por CAC)
                        ▼
              1_scrapped_html/
                        │
          ┌─────────────▼──────────────┐
          │   csv_parser.py             │
          │                            │
          │  Extrae JSON del <pre>     │
          │  Convierte a CSV           │
          └─────────────┬──────────────┘
                        │ CSV (1 por CAC)
                        ▼
              2_scrapped_csv/
                        │
          ┌─────────────▼──────────────┐
          │   csv_stacker.py            │
          │                            │
          │  Fusiona todos los CSVs    │
          │  en un único DataFrame     │
          │  Genera: CACs_{fecha}.csv  │
          └─────────────┬──────────────┘
                        │ CSV unificado
                        ▼
              3_filtered_data/
                        │
          ┌─────────────▼──────────────┐
          │   onelake.py                │
          │                            │
          │  Sube a Fabric OneLake     │
          │  LH_CIDI.Lakehouse/Files/  │
          │  CACs/                     │
          └────────────────────────────┘
```

---

## Diagrama de flujo — Comentarios

```
┌─────────────────────────────────────────────────────────┐
│  cidi_scrapper.py  (orquestador)                        │
└───────────────────────┬─────────────────────────────────┘
                        │
          ┌─────────────▼──────────────┐
          │ client_info_scrapper.py     │
          │   (Selenium + Chrome)       │
          │                            │
          │  GET /api/Turno/           │
          │  Get_Supervision           │
          └─────────────┬──────────────┘
                        │ HTML (1 por CAC)
                        ▼
           4_comments_scrapped_html/
                        │
          ┌─────────────▼──────────────┐
          │   csv_parser.py (Ns=1)      │
          │   (reemplaza \n en texto)   │
          └─────────────┬──────────────┘
                        │ CSV (1 por CAC)
                        ▼
           5_comments_scrapped_csv/
                        │
          ┌─────────────▼──────────────┐
          │   csv_stacker.py            │
          │   Clasifica comentarios    │
          │   en 14 categorías         │
          │   Genera:                  │
          │   CACs_Comments_{fecha}.csv│
          └─────────────┬──────────────┘
                        │
          ┌─────────────▼──────────────┐
          │   csv_process.py            │
          │   Elimina 15 columnas      │
          │   innecesarias             │
          └─────────────┬──────────────┘
                        │ CSV limpio
                        ▼
           6_comments_filtered_data/
                        │
          ┌─────────────▼──────────────┐
          │ sharepoint.py / onelake.py  │
          │ Upload a SharePoint o      │
          │ OneLake (según opción)     │
          └────────────────────────────┘
```

---

## Módulos y responsabilidades

| Módulo | Responsabilidad | Dependencias externas |
|--------|----------------|----------------------|
| `cidi_scrapper.py` | Orquestación del pipeline completo, menú interactivo | Todos los módulos |
| `turnero_scrapper.py` | Scraping de datos de turnero vía Selenium | Chrome, ChromeDriver, CIDI portal |
| `client_info_scrapper.py` | Scraping de comentarios/supervisión vía Selenium | Chrome, ChromeDriver, CIDI portal |
| `csv_parser.py` | Parsing HTML → JSON → CSV | BeautifulSoup |
| `csv_stacker.py` | Fusión de CSVs + clasificación por regex | pandas, onelake |
| `csv_process.py` | Limpieza de columnas de comentarios | pandas, onelake |
| `credentials.py` | Lectura de credenciales y rutas desde .txt | — |
| `menu.py` | Interfaz CLI con logo EPEC | colorama |
| `sharepoint.py` | Upload a SharePoint vía Microsoft Graph API | azure-identity, requests |
| `onelake.py` | Upload a Azure OneLake (Fabric) | azure-storage-filedatalake, azure-identity |
| `file_destructor.py` | Limpieza de archivos temporales entre ejecuciones | tkinter (popup) |
| `tx.py` | Alertas de error vía Telegram Bot API | requests |

---

## Endpoints de la API de CIDI

| Tipo de datos | Endpoint |
|---------------|----------|
| Turnero (listado de atenciones) | `https://turnero.cba.gov.ar/api/Reporte/Get_Turnos_Listado?Id_Centro_Atencion={id}&FecDesde={fecha}&FecHasta={fecha}` |
| Comentarios/Supervisión | `https://turnero.cba.gov.ar/api/Turno/Get_Supervision?filtro.fec_Desde={fecha}&filtro.fec_Hasta={fecha}&filtro.Id_Centro_Atencion={id}&filtro.Mostrar_Turnos_Con_Comentarios=N` |

La autenticación se realiza mediante login web en `https://cidi.cba.gov.ar/portal-publico` y las cookies de sesión son usadas por Selenium para las requests posteriores.

---

## Categorías de clasificación de comentarios

El módulo `csv_stacker.py` clasifica los comentarios libres de clientes en 14 categorías mediante expresiones regulares:

1. ALTA SERVICIO
2. BAJA DE SERVICIO
3. RECLAMO POR FACTURACION
4. RECLAMO POR CORTE
5. TRAMITES VARIOS
6. INFORMACION
7. PAGO
8. CONEXION
9. CAMBIO DE TITULAR
10. CONVENIO DE PAGO
11. MEDIDOR
12. SUBSIDIO
13. ATENCION COMERCIAL
14. OTRO (categoría residual)

---

## Destinos cloud

| Destino | Credenciales | Ruta |
|---------|-------------|------|
| OneLake (turnero) | InteractiveBrowserCredential (MFA) | `Protelem - Premium / LH_CIDI.Lakehouse/Files/CACs/` |
| OneLake (comentarios) | InteractiveBrowserCredential (MFA) | `Protelem - Premium / LH_CIDI.Lakehouse/Files/CACs_Comments/` |
| SharePoint | InteractiveBrowserCredential (MFA) | `PROTELEM-INDICADORES / Documentos compartidos/m_actividad_turnero_cidi` |
| SharePoint (comentarios) | InteractiveBrowserCredential (MFA) | `PROTELEM-INDICADORES / Documentos compartidos/m_comentarios_turnero_cidi` |
