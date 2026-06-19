import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tx import *

def fetch_and_save_data(cuil, password, centros_de_atencion, folder_path, desde=None, hasta=None):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")

    executable_path_usr = "D:/Usuarios/mdelgadillo/Documents/chromeBrowser/chromedriver-win64/chromedriver.exe"

    driver = webdriver.Chrome(service=webdriver.chrome.service.Service(executable_path=executable_path_usr), options=options)
    driver.set_page_load_timeout(240)
    driver.set_window_position(0, 0)

    def login_with_selenium(cuil, password):
        url = 'https://cidi.cba.gov.ar/portal-publico'
        driver.get(url)

        try:
            ingresar_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn-ingresar[aria-label="Ingresar"]')))
            ingresar_button.click()

            cuil_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'cuil')))
            cuil_input.send_keys(cuil)

            time.sleep(1)

            password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
            password_input.send_keys(password)

            ingresar_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn-access__btn.btn-access__btn--bg-cel')))
            ingresar_button.click()

            WebDriverWait(driver, 10).until(EC.url_contains('dashboard'))

            if 'dashboard' in driver.current_url:
                print("Login successful!")
            else:
                print("Login failed. Please check your credentials.")

        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def open_new_tab_with_url(url):
        driver.execute_script("window.open('about:blank', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(url)

    login_with_selenium(cuil, password)

    for id_centro, descripcion in centros_de_atencion.items():
        try:
            url_data = f'https://turnero.cba.gov.ar/api/Reporte/Get_Turnos_Listado?Id_Centro_Atencion={id_centro}&FecDesde={desde}T00:00:00&FecHasta={hasta}T23:59:59'
            url_turnos = 'https://turnero.cba.gov.ar/turnos'

            open_new_tab_with_url(url_turnos)
            driver.refresh()
            time.sleep(3.5)

            open_new_tab_with_url(f'https://turnero.cba.gov.ar/api/Menu?id_centro_atencion={id_centro}')
            driver.refresh()
            time.sleep(3.5)

            open_new_tab_with_url(url_data)
            driver.refresh()
            time.sleep(3.5)

            page_source = driver.page_source

            driver.close()

            driver.switch_to.window(driver.window_handles[1])
            time.sleep(1.5)
            driver.close()
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(1.5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            output_file = os.path.join(folder_path, f'{descripcion}.html')
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(page_source)

            print(f"HTML content for '{descripcion}' saved to {output_file}")

        except Exception as e:
            print(f"An error occurred for '{descripcion}': {str(e)}")
            alerta_error(f"An error occurred for '**{descripcion}**': {str(e)}")
            time.sleep(2)
            page_source = driver.page_source

            driver.switch_to.window(driver.window_handles[1])
            time.sleep(1.5)
            driver.close()
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(1.5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            output_file = os.path.join(folder_path, f'{descripcion}.html')
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(page_source)

            print(f"HTML content for '{descripcion}' saved to {output_file}")
            alerta_error(f"HTML content for '**{descripcion}**' saved to {output_file}")

    time.sleep(3)
    driver.quit()
    print("Script execution completed.")
