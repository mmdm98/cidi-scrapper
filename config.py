# Selenium — timeouts y delays
PAGE_LOAD_TIMEOUT_TURNERO  = 240
PAGE_LOAD_TIMEOUT_COMMENTS = 120
SLEEP_TAB_OPEN   = 3.5
SLEEP_TAB_CLOSE  = 1.5
SLEEP_LOGIN      = 1.0
PAGE_SIZE_COMMENTS = 10000
TURNERO_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
)

# ChromeDriver — configurable via línea 9 de paths.txt (ver paths.example.txt)
DEFAULT_CHROMEDRIVER_PATH = "D:/Usuarios/mdelgadillo/Documents/chromeBrowser/chromedriver-win64/chromedriver.exe"

# URLs CIDI / Turnero
CIDI_LOGIN_URL  = "https://cidi.cba.gov.ar/portal-publico"
TURNERO_NAV_URL = "https://turnero.cba.gov.ar/turnos"
CLIENT_NAV_URL  = "https://turnero.cba.gov.ar/asistencia/turnos"
TURNERO_MENU_URL_TMPL = "https://turnero.cba.gov.ar/api/Menu?id_centro_atencion={id_centro}"
TURNERO_DATA_URL_TMPL = (
    "https://turnero.cba.gov.ar/api/Reporte/Get_Turnos_Listado"
    "?Id_Centro_Atencion={id_centro}&FecDesde={desde}T00:00:00&FecHasta={hasta}T23:59:59"
)
SUPERVISION_DATA_URL_TMPL = (
    "https://turnero.cba.gov.ar/api/Turno/Get_Supervision"
    "?filtro.fec_Desde={desde}T00:00:00&filtro.fec_Hasta={hasta}T23:59:59"
    "&filtro.nro_Pagina=1&filtro.tam_Pagina={size}"
    "&filtro.Mostrar_Turnos_Con_Comentarios=N&filtro.id_Centro_Atencion={id_centro}"
)

# SharePoint
SHAREPOINT_SITE_NAME       = "PROTELEM-INDICADORES"
SHAREPOINT_BASE_PATH       = "https://epeccba.sharepoint.com/"
SHAREPOINT_FOLDER_TURNERO  = "Documentos compartidos/m_actividad_turnero_cidi"
SHAREPOINT_FOLDER_COMMENTS = "Documentos compartidos/m_comentarios_turnero_cidi"
