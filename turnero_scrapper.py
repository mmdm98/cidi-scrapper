from scrapper_base import fetch_cac_data
from config import (
    PAGE_LOAD_TIMEOUT_TURNERO,
    TURNERO_DATA_URL_TMPL,
    TURNERO_NAV_URL,
    TURNERO_USER_AGENT,
)


def fetch_and_save_data(cuil, password, centros_de_atencion, folder_path, desde=None, hasta=None, chromedriver_path=None):
    fetch_cac_data(
        cuil=cuil,
        password=password,
        centros_de_atencion=centros_de_atencion,
        folder_path=folder_path,
        desde=desde,
        hasta=hasta,
        chromedriver_path=chromedriver_path,
        page_load_timeout=PAGE_LOAD_TIMEOUT_TURNERO,
        data_url_fn=lambda id_c, d, h: TURNERO_DATA_URL_TMPL.format(id_centro=id_c, desde=d, hasta=h),
        nav_url=TURNERO_NAV_URL,
        file_suffix="",
        use_refresh=True,
        user_agent=TURNERO_USER_AGENT,
        save_on_error=True,
    )
