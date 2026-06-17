import time
from datetime import datetime
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tx import *
# from csv_parser         import *
# from csv_stacker        import *

def fetch_and_save_comment_data(cuil, password, centros_de_atencion, folder_path, desde=None, hasta=None):
    # Chrome options to ignore certificate errors
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')

    # Replace with the path to your chromedriver executable
    executable_path_usr = "D:/Usuarios/mdelgadillo/Documents/chromeBrowser/chromedriver-win64/chromedriver.exe"

    # Initialize Chrome driver
    driver = webdriver.Chrome(service=webdriver.chrome.service.Service(executable_path=executable_path_usr), options=options)


    # Set the window size (for example, iPhone 6/7/8 dimensions)
    #driver.set_window_size(375, 667)

    # Set the window position (top-left corner)
    driver.set_window_position(0, 0)


    # Function to login with Selenium
    def login_with_selenium(cuil, password):
        url = 'https://cidi.cba.gov.ar/portal-publico'  # Replace with the actual login URL
        driver.get(url)

        try:
            # # Find and click the "INGRESAR" button using CSS selector
            # ingresar_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.mat-focus-indicator.btn--primario.mat-raised-button.mat-button-base.ng-star-inserted')))
            # ingresar_button.click()
            # Find and click the "INGRESAR" button using updated CSS selector
            ingresar_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn-ingresar[aria-label="Ingresar"]')))
            ingresar_button.click()
            
            # Find the CUIL input field and enter the CUIL number
            cuil_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'cuil')))
            cuil_input.send_keys(cuil)

            time.sleep(1)

            # Find the password input field and enter the password
            password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
            password_input.send_keys(password)

            # Find and click the "Ingresar" button using CSS selector
            ingresar_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn-access__btn.btn-access__btn--bg-cel')))
            ingresar_button.click()

            # Find and click the "Ingresar" button using CSS selector este quedó viejo
            # ingresar_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.mat-raised-button.mat-button-base')))
            # ingresar_button.click()

            # ingresar_button = driver.find_element(By.XPATH, "//button[contains(., 'INGRESAR')]") este no funciono
            # ingresar_button.click()

            # Wait for the login process to complete and check if logged in successfully
            WebDriverWait(driver, 10).until(EC.url_contains('dashboard'))

            if 'dashboard' in driver.current_url:
                print("Login successful!")
            else:
                print("Login failed. Please check your credentials.")

        except Exception as e:
            print(f"An error occurred: {str(e)}")

    # Function to open a new tab in the same browser session and load a specific URL
    def open_new_tab_with_url(url):
        # Execute JavaScript to open a new tab
        driver.execute_script("window.open('about:blank', '_blank');")

        # Switch to the newly opened tab
        driver.switch_to.window(driver.window_handles[-1])

        # Navigate to the specified URL in the new tab
        driver.get(url)

    # Log in
    login_with_selenium(cuil, password)
    size = 10000
    # Main function to iterate through each Centro de Atención
    # Hacer un description anterior y un description actual
    for id_centro, descripcion in centros_de_atencion.items():
        try:
            # Construct the URL for data with current Centro de Atención ID and date range
            url_data = f'https://turnero.cba.gov.ar/api/Turno/Get_Supervision?filtro.fec_Desde={desde}T00:00:00&filtro.fec_Hasta={hasta}T23:59:59&filtro.nro_Pagina=1&filtro.tam_Pagina={size}&filtro.Mostrar_Turnos_Con_Comentarios=N&filtro.id_Centro_Atencion={id_centro}'
            url_turnos = 'https://turnero.cba.gov.ar/asistencia/turnos'

            open_new_tab_with_url(url_turnos)
            time.sleep(3.5)

            # Open Centro de Atención page and wait
            open_new_tab_with_url(f'https://turnero.cba.gov.ar/api/Menu?id_centro_atencion={id_centro}')
            time.sleep(3.5)

            # Open data page and wait
            open_new_tab_with_url(url_data)
            driver.set_page_load_timeout(120)  # Wait up to 60 seconds

            # Get page source (HTML content)
            page_source = driver.page_source

            # Close the current tab
            driver.close()

            # Switch back to the main tab
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(1.5)
            driver.close()
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(1.5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            # Save HTML content to a file named after the Centro de Atención description
            output_file = os.path.join(folder_path, f'{descripcion}_CLIENT.html')
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(page_source)

            print(f"HTML content for '{descripcion}' saved to {output_file}")

        except Exception as e:
            print(f"An error occurred for '{descripcion}': {str(e)}")
            alerta_error(f"An error occurred for '{descripcion}': {str(e)}")

    # Wait for 3 seconds before quitting
    time.sleep(3)

    # Close the browser window
    driver.quit()

    print("Script execution completed.")


# centros_de_atencion = {
#     1825: 'EPEC CENTRO DE ATENCION COMERCIAL ESTE',
#     1824: 'EPEC CENTRO DE ATENCION COMERCIAL NORTE',
#     1823: 'EPEC CENTRO DE ATENCION COMERCIAL SUR',
#     1766: 'EPEC CENTRO DE ATENCION COMERCIAL TERMINAL DE ÓMNIBUS',
#     1826: 'EPEC CPC ARGUELLO - LOCAL 3'
# }

# path_1 = 'D:/Usuarios/MDELGADILLO/Desktop/xCodes/xSources/cidi/4_pruebas_probadas'
# path_2 = 'D:/Usuarios/MDELGADILLO/Desktop/xCodes/xSources/cidi/5_pruebas_probadas'
# path_3 = 'D:/Usuarios/MDELGADILLO/Desktop/xCodes/xSources/cidi/6_pruebas_probadas'

#fetch_and_save_data('20-35894360-9', 'Qknibpg5', centros_de_atencion, path_1, '2024-07-01', '2024-07-23')

# convert_html_files_to_csv(path_1, path_2, True)

# Locking a el dia de la fecha
# current_date = datetime.today().date() - timedelta(days=1)

# merge_csv_files(path_2, path_3, current_date, 'COMENTARIOS')

# necesito un pre data curing para sacar algunas columnas, las que quedan son
# Interesado,Cuil_Interesado,Turno,Id_Turno,Fec_Solicitado,Datos_Particulares,Comentarios
# csv-> pandas -> csv -> al sharepoint (en el sharepoint hacer otra carpeta para subir las cosas)
# ver si todos los id son realmente unicos o se repiten entre cacs (ver si son unicos por cac o unicos globales)
# ver si el agendado ese fue un dedaso mio o un dedaso de los del cidi
# 