import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import (
    CIDI_LOGIN_URL, TURNERO_MENU_URL_TMPL,
    SLEEP_TAB_OPEN, SLEEP_TAB_CLOSE, SLEEP_LOGIN,
    DEFAULT_CHROMEDRIVER_PATH,
)
from tx import alerta_error


def _init_driver(chromedriver_path, page_load_timeout, user_agent=None):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    if user_agent:
        options.add_argument(f"user-agent={user_agent}")
    driver = webdriver.Chrome(
        service=webdriver.chrome.service.Service(executable_path=chromedriver_path),
        options=options,
    )
    driver.set_page_load_timeout(page_load_timeout)
    driver.set_window_position(0, 0)
    return driver


def _login(driver, cuil, password):
    driver.get(CIDI_LOGIN_URL)
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn-ingresar[aria-label="Ingresar"]'))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'cuil'))
        ).send_keys(cuil)

        time.sleep(SLEEP_LOGIN)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'password'))
        ).send_keys(password)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn-access__btn.btn-access__btn--bg-cel'))
        ).click()

        WebDriverWait(driver, 10).until(EC.url_contains('dashboard'))

        if 'dashboard' in driver.current_url:
            print("Login successful!")
        else:
            print("Login failed. Please check your credentials.")

    except Exception as e:
        print(f"An error occurred during login: {str(e)}")


def _open_tab(driver, url):
    driver.execute_script("window.open('about:blank', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(url)


def fetch_cac_data(
    cuil, password, centros_de_atencion, folder_path, desde, hasta,
    chromedriver_path=None,
    page_load_timeout=240,
    data_url_fn=None,
    nav_url=None,
    file_suffix="",
    use_refresh=False,
    user_agent=None,
    save_on_error=False,
):
    driver = _init_driver(chromedriver_path or DEFAULT_CHROMEDRIVER_PATH, page_load_timeout, user_agent)
    _login(driver, cuil, password)

    for id_centro, descripcion in centros_de_atencion.items():
        filename = f"{descripcion}{file_suffix}.html"
        try:
            _open_tab(driver, nav_url)
            if use_refresh:
                driver.refresh()
            time.sleep(SLEEP_TAB_OPEN)

            _open_tab(driver, TURNERO_MENU_URL_TMPL.format(id_centro=id_centro))
            if use_refresh:
                driver.refresh()
            time.sleep(SLEEP_TAB_OPEN)

            _open_tab(driver, data_url_fn(id_centro, desde, hasta))
            if use_refresh:
                driver.refresh()
            time.sleep(SLEEP_TAB_OPEN)

            page_source = driver.page_source
            driver.close()  # cierra pestaña de datos

            # cierra pestañas de menú y navegación
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(SLEEP_TAB_CLOSE)
            driver.close()
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(SLEEP_TAB_CLOSE)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            output_file = os.path.join(folder_path, filename)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(page_source)
            print(f"HTML content for '{descripcion}' saved to {output_file}")

        except Exception as e:
            print(f"An error occurred for '{descripcion}': {str(e)}")
            alerta_error(f"An error occurred for '**{descripcion}**': {str(e)}")
            if save_on_error:
                # Intenta recuperar lo que haya en la pestaña actual y cerrar las extra
                time.sleep(2)
                try:
                    page_source = driver.page_source
                    driver.switch_to.window(driver.window_handles[1])
                    time.sleep(SLEEP_TAB_CLOSE)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[1])
                    time.sleep(SLEEP_TAB_CLOSE)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    output_file = os.path.join(folder_path, filename)
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(page_source)
                    print(f"HTML content for '{descripcion}' saved to {output_file}")
                    alerta_error(f"HTML content for '**{descripcion}**' saved to {output_file}")
                except Exception:
                    pass

    time.sleep(3)
    driver.quit()
    print("Script execution completed.")
