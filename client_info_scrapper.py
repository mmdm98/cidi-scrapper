from scrapper_base import fetch_cac_data
from config import (
    PAGE_LOAD_TIMEOUT_COMMENTS,
    SUPERVISION_DATA_URL_TMPL,
    CLIENT_NAV_URL,
    PAGE_SIZE_COMMENTS,
)


def fetch_and_save_comment_data(cuil, password, centros_de_atencion, folder_path, desde=None, hasta=None, chromedriver_path=None):
    fetch_cac_data(
        cuil=cuil,
        password=password,
        centros_de_atencion=centros_de_atencion,
        folder_path=folder_path,
        desde=desde,
        hasta=hasta,
        chromedriver_path=chromedriver_path,
        page_load_timeout=PAGE_LOAD_TIMEOUT_COMMENTS,
        data_url_fn=lambda id_c, d, h: SUPERVISION_DATA_URL_TMPL.format(
            id_centro=id_c, desde=d, hasta=h, size=PAGE_SIZE_COMMENTS
        ),
        nav_url=CLIENT_NAV_URL,
        file_suffix="_CLIENT",
        use_refresh=False,
        user_agent=None,
        save_on_error=False,
    )
