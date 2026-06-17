import time
from datetime import datetime
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tx import *

def fetch_and_save_data(cuil, password, centros_de_atencion, folder_path, desde=None, hasta=None):
    # Chrome options to ignore certificate errors
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")

    # Replace with the path to your chromedriver executable
    executable_path_usr = "D:/Usuarios/mdelgadillo/Documents/chromeBrowser/chromedriver-win64/chromedriver.exe"

    # Initialize Chrome driver
    driver = webdriver.Chrome(service=webdriver.chrome.service.Service(executable_path=executable_path_usr), options=options)

    # Este es el timer global, 4 minutos (no sirve y lo ignora)
    driver.set_page_load_timeout(240) 

    # Set the window size (for example, iPhone 6/7/8 dimensions)
    #driver.set_window_size(375, 667)

    # Set the window position (top-left corner)
    driver.set_window_position(0, 0)

    # Function to login with Selenium
    def login_with_selenium(cuil, password):
        url = 'https://cidi.cba.gov.ar/portal-publico'  # Replace with the actual login URL
        driver.get(url)

        try:
            # Find and click the "INGRESAR" button using CSS selector
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

            # # Find and click the "Ingresar" button using CSS selector
            # ingresar_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.mat-raised-button.mat-button-base')))
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
    # Main function to iterate through each Centro de Atención
    for id_centro, descripcion in centros_de_atencion.items():
        try:
            # Construct the URL for data with current Centro de Atención ID and date range
            url_data = f'https://turnero.cba.gov.ar/api/Reporte/Get_Turnos_Listado?Id_Centro_Atencion={id_centro}&FecDesde={desde}T00:00:00&FecHasta={hasta}T23:59:59'
            url_turnos = 'https://turnero.cba.gov.ar/turnos'
            # url_reportes = 'https://turnero.cba.gov.ar/reportes'
            open_new_tab_with_url(url_turnos)
            driver.refresh()
            time.sleep(3.5)

            # open_new_tab_with_url(url_reportes)
            # time.sleep(3.5)

            # Open Centro de Atención page and wait
            open_new_tab_with_url(f'https://turnero.cba.gov.ar/api/Menu?id_centro_atencion={id_centro}')
            driver.refresh()
            time.sleep(3.5)

            # open_new_tab_with_url(f'https://turnero.cba.gov.ar/api/Reporte/Get_Turnos_Listado?Id_Centro_Atencion=1766&FecDesde=2025-01-27T00:00:00&FecHasta=2025-01-27T23:59:59')
            # time.sleep(3.5)

            # Open data page and wait
            open_new_tab_with_url(url_data)
            driver.refresh()
            time.sleep(3.5)

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
            output_file = os.path.join(folder_path, f'{descripcion}.html')
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(page_source)

            print(f"HTML content for '{descripcion}' saved to {output_file}")

        except Exception as e:
            print(f"An error occurred for '{descripcion}': {str(e)}")
            alerta_error(f"An error occurred for '**{descripcion}**': {str(e)}")
            time.sleep(2)
            page_source = driver.page_source
            # print(page_source)

            # Switch back to the main tab
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

    # Wait for 3 seconds before quitting
    time.sleep(3)

    # Close the browser window
    driver.quit()

    print("Script execution completed.")

