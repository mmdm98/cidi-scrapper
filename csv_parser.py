import os
import json
import csv
from bs4 import BeautifulSoup
import glob

# def convert_html_to_csv(html_content):
#     soup = BeautifulSoup(html_content, 'html.parser')
#     pre_tag = soup.find('pre')
#     if pre_tag:
#         json_data = pre_tag.text.strip()
#         data = json.loads(json_data)
#         records = data['Data']
#         csv_headers = records[0].keys()
#         return records, csv_headers
#     else:
#         return None, None

def convert_html_to_csv(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    pre_tag = soup.find('pre')
    if pre_tag:
        json_data = pre_tag.text.strip()
        try:
            data = json.loads(json_data)
            records = data['Data']
            if records:
                csv_headers = records[0].keys()
                return records, csv_headers
            else:
                return [], []  # Return empty lists if no records
        except json.JSONDecodeError:
            return None, None  # Handle JSON parsing errors
    else:
        return None, None

# def convert_html_files_to_csv(html_directory, output_folder):
#     # Ensure output folder exists, create if it doesn't
#     os.makedirs(output_folder, exist_ok=True)

#     # Process each HTML file in the directory
#     for html_file in glob.glob(os.path.join(html_directory, '*.html')):
#         with open(html_file, 'r', encoding='utf-8') as file:
#             html_content = file.read()

#         # Convert HTML to CSV
#         records, csv_headers = convert_html_to_csv(html_content)

#         if records and csv_headers:
#             # Extract the filename without extension
#             filename = os.path.splitext(os.path.basename(html_file))[0]

#             # Define CSV output file path in the output folder
#             csv_file = os.path.join(output_folder, f'{filename}.csv')

#             # Write data to CSV file
#             with open(csv_file, mode='w', newline='', encoding='utf-8') as csv_file:
#                 writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
#                 writer.writeheader()
#                 writer.writerows(records)

#             print(f'CSV file "{csv_file}" has been created successfully.')
#         else:
#             print(f'No <pre> tag containing JSON data found in {html_file}. Skipping...')


def convert_html_files_to_csv(html_directory, output_folder, Ns):
    # Ensure output folder exists, create if it doesn't
    os.makedirs(output_folder, exist_ok=True)

    # Process each HTML file in the directory
    for html_file in glob.glob(os.path.join(html_directory, '*.html')):
        with open(html_file, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Hay enes? Si hay reemplazarlo con espacio en blanco
        if Ns == 1:
            # newline_count = html_content.count('\\n')
            # print("HAY UN TOTAL DE Ns : ", newline_count)
            html_content = html_content.replace('\\n', ' ')

        # Convert HTML to CSV
        records, csv_headers = convert_html_to_csv(html_content)

        if records and csv_headers:
            # Extract the filename without extension
            filename = os.path.splitext(os.path.basename(html_file))[0]

            # Define CSV output file path in the output folder
            csv_file = os.path.join(output_folder, f'{filename}.csv')

            # Write data to CSV file
            with open(csv_file, mode='w', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
                writer.writeheader()
                writer.writerows(records)

            print(f'CSV file "{csv_file}" has been created successfully.')
        else:
            print(f'No valid JSON data found in {html_file}. Skipping...')


# html_directory="D:/Usuarios/MDELGADILLO/Desktop/xCodes/xSources/cidi/72_prueba"
# output_folder="D:/Usuarios/MDELGADILLO/Desktop/xCodes/xSources/cidi/72_prueba"
# convert_html_files_to_csv(html_directory, output_folder, 1)

# # Nombre del archivo
# html_file = 'D:/Usuarios/MDELGADILLO/Desktop/xCodes/xSources/cidi/72_prueba/EPEC CENTRO DE ATENCION COMERCIAL ESTE_CLIENT.html'

# # Abrir el archivo en modo binario
# with open(html_file, 'rb') as file:
#     # Leer el contenido del archivo como bytes
#     html_content = file.read()

# # Convertir el valor binario de '\n' (0x0A) y el espacio (0x20) a bytes
# newline_byte = b'\x0A'
# space_byte = b'\x20'

# # Si Ns es 1, reemplazar los caracteres
# if 1 == 1:
#     print("SI SE IMPRIME ESTE MENSAJE ES QUE ENTRA ACA")
#     # Reemplazar '\n' con espacio en blanco
#     html_content = html_content.replace(newline_byte, space_byte)

# # Guardar el contenido modificado en un nuevo archivo (opcional)
# output_file = 'D:/Usuarios/MDELGADILLO/Desktop/xCodes/xSources/cidi/72_prueba/EPEC CENTRO DE ATENCION COMERCIAL ESTE_CLIENTxx.html'
# with open(output_file, 'wb') as file:
#     file.write(html_content)
    
# print(f'Archivo modificado guardado como "{output_file}".')


# from bs4 import BeautifulSoup

# def html_to_text(html_file, text_file):
#     try:
#         # Leer el contenido del archivo HTML
#         with open(html_file, 'r', encoding='utf-8') as file:
#             html_content = file.read()

#         # Parsear el contenido HTML usando BeautifulSoup
#         soup = BeautifulSoup(html_content, 'lxml')

#         # Extraer el texto del contenido HTML
#         text_content = soup.get_text(separator='\n')

#         # Guardar el texto extraído en un archivo .txt
#         with open(text_file, 'w', encoding='utf-8') as file:
#             file.write(text_content)

#         print(f"El archivo '{text_file}' ha sido creado exitosamente.")
    
#     except FileNotFoundError:
#         print(f"El archivo '{html_file}' no se encontró.")
#     except IOError:
#         print(f"Hubo un error al intentar leer o escribir el archivo.")

# def replace_newlines_in_txt(input_file, output_file, replacement=' '):
#     """
#     Abre un archivo .txt, reemplaza los saltos de línea '\n' con el carácter especificado,
#     y guarda el resultado en un nuevo archivo.
    
#     :param input_file: Ruta al archivo de entrada .txt
#     :param output_file: Ruta al archivo de salida .txt
#     :param replacement: Carácter para reemplazar los saltos de línea. Por defecto es un espacio en blanco.
#     """
#     try:
#         # Abrir el archivo de entrada en modo lectura
#         with open(input_file, 'r', encoding='utf-8') as file:
#             content = file.read()

#         # Reemplazar los saltos de línea con el carácter especificado
#         modified_content = content.replace('\n', replacement)

#         # Guardar el contenido modificado en el archivo de salida
#         with open(output_file, 'w', encoding='utf-8') as file:
#             file.write(modified_content)

#         print(f"El archivo '{output_file}' ha sido creado exitosamente con los saltos de línea reemplazados.")
    
#     except FileNotFoundError:
#         print(f"El archivo '{input_file}' no se encontró.")
#     except IOError:
#         print(f"Hubo un error al intentar leer o escribir el archivo.")


# # Usar la función
# html_file = 'D:/Usuarios/MDELGADILLO/Desktop/xCodes/xSources/cidi/72_prueba/EPEC CENTRO DE ATENCION COMERCIAL ESTE_CLIENT.html'
# text_file = 'D:/Usuarios/MDELGADILLO/Desktop/xCodes/xSources/cidi/72_prueba/EPEC CENTRO DE ATENCION COMERCIAL ESTE_CLIENT.txt'
# text_out = 'D:/Usuarios/MDELGADILLO/Desktop/xCodes/xSources/cidi/72_prueba/EPEC CENTRO DE ATENCION COMERCIAL ESTE_CLIENTxxx.txt'

# # html_to_text(html_file, text_file)
# # replace_newlines_in_txt(text_file, text_out, replacement=' ')

# print("a \\n a")