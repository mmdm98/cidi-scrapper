# import os
# import requests
# from shareplum import Office365

# def upload_file_to_sharepoint(username, password, site_name, base_path, nested_folder, local_folder):
#     # Function to get the last modified file in a folder
#     def get_last_modified_file(folder_path):
#         files = os.listdir(folder_path)
#         if not files:
#             return None
#         paths = [os.path.join(folder_path, basename) for basename in files]
#         return max(paths, key=os.path.getmtime)

#     # Get the last modified file in the local folder
#     file_path = get_last_modified_file(local_folder)
#     if not file_path:
#         print("No files found in the specified folder.")
#         return False
    
#     print("Last modified file:", file_path)
#     file_name = os.path.basename(file_path)

#     # Agregar acá un redireccionamiento a el one lake

#     # Obtain auth cookie
#     authcookie = Office365(base_path, username=username, password=password).GetCookies()
#     session = requests.Session()
#     session.cookies = authcookie
#     session.headers.update({'user-agent': 'python_bite/v1'})
#     session.headers.update({'accept': 'application/json;odata=verbose'})

#     # Get the X-RequestDigest value
#     response = session.post(url=base_path + "/sites/" + site_name + "/_api/contextinfo")
#     session.headers.update({'X-RequestDigest': response.json()['d']['GetContextWebInformation']['FormDigestValue']})

#     # Upload file
#     with open(file_path, 'rb') as file_input:
#         try:
#             response = session.post(
#                 url=base_path + "/sites/" + site_name + f"/_api/web/GetFolderByServerRelativeUrl('" + nested_folder + "')/Files/add(url='"
#                 + file_name + "',overwrite=true)",
#                 data=file_input)
#             print("Response:", response.status_code)
#             if response.status_code == 200:
#                 print("File uploaded successfully")
#                 return True
#             else:
#                 print("Failed to upload file")
#                 return False
#         except Exception as err:
#             print("Something went wrong: " + str(err))
#             return False




# ##############################################################################################################################################################

# from azure.storage.filedatalake import DataLakeServiceClient, DataLakeDirectoryClient
# from azure.identity import InteractiveBrowserCredential
# import requests
# import os

# # OneLake
# ACCOUNT_NAME = "onelake"
# WORKSPACE_NAME = "myworkspace-1"
# DATA_PATH = "LH_PERFILES.Lakehouse/Files/est"

# # SharePoint
# SITE_NAME = "MiSitio"  # el nombre de tu sitio de SharePoint
# SITE_HOST = "https://tuempresa.sharepoint.com"  # dominio de tu tenant
# DOC_LIB = "Documentos compartidos/Pruebas"     # librería/carpeta destino
# LOCAL_FILE = "D:/Usuarios/mdelgadillo/Desktop/xCodes/xSources/web/consumos.csv"

# def upload_file_to_onelake(directory_client: DataLakeDirectoryClient, local_path: str, file_name: str):
#     file_client = directory_client.get_file_client(file_name)
#     with open(os.path.join(local_path, file_name), "rb") as data:
#         file_client.upload_data(data.read(), overwrite=True)

# #def guardar_en_onelake_y_sharepoint():
# def guardar_en_onelake_y_sharepoint():
#     # 1. Autenticación (con MFA si hace falta)
#     print("Autorización de credencial...")
#     credential = InteractiveBrowserCredential()
#     print("Autorización exitosa...")

#     # # 2. Conexión a OneLake
#     # account_url = f"https://{ACCOUNT_NAME}.dfs.fabric.microsoft.com"
#     # service_client = DataLakeServiceClient(account_url, credential=credential)
#     # file_system_client = service_client.get_file_system_client(WORKSPACE_NAME)
#     # paths = file_system_client.get_paths(path=DATA_PATH)

#     # print("Archivos en el Path de OneLake")
#     # for path in paths:
#     #     print(path.name, path.last_modified)

#     # directory_client = file_system_client.get_directory_client(DATA_PATH)
#     # upload_file_to_onelake(
#     #     directory_client=directory_client,
#     #     local_path=os.path.dirname(LOCAL_FILE),
#     #     file_name=os.path.basename(LOCAL_FILE)
#     # )
#     # print("Archivo subido con éxito a OneLake!")

#     # 3. Subida también a SharePoint con Graph
#     token = credential.get_token("https://graph.microsoft.com/.default").token
#     headers = {
#         "Authorization": f"Bearer {token}",
#         "Content-Type": "application/octet-stream"
#     }

#     file_name = os.path.basename(LOCAL_FILE)
#     with open(LOCAL_FILE, "rb") as f:
#         content = f.read()

#     # URL para cargar directo en la librería
#     upload_url = (
#         f"https://graph.microsoft.com/v1.0/sites/{SITE_HOST.replace('https://','')}:/{SITE_NAME}:/drive/root:/{DOC_LIB}/{file_name}:/content"
#     )

#     resp = requests.put(upload_url, headers=headers, data=content)

#     if resp.status_code in (200, 201):
#         print("Archivo subido con éxito a SharePoint!")
#     else:
#         print("Error subiendo a SharePoint:", resp.status_code, resp.text)


# if __name__ == "__main__":
#     guardar_en_onelake_y_sharepoint()


######################################################################################################################################################

from azure.storage.filedatalake import DataLakeServiceClient, DataLakeDirectoryClient
from azure.identity import InteractiveBrowserCredential
import requests
import os

# SharePoint
SITE_NAME = "MiSitio"  # el nombre de tu sitio de SharePoint
SITE_HOST = "https://tuempresa.sharepoint.com"  # dominio de tu tenant
DOC_LIB = "Documentos compartidos/Pruebas"     # librería/carpeta destino
LOCAL_FILE = "D:/Usuarios/mdelgadillo/Desktop/xCodes/xSources/web/consumos.csv"

def upload_file_to_sharepoint(username, password, site_name, base_path, nested_folder, local_folder):
    # Function to get the last modified file in a folder
    def get_last_modified_file(folder_path):
        files = os.listdir(folder_path)
        if not files:
            return None
        paths = [os.path.join(folder_path, basename) for basename in files]
        return max(paths, key=os.path.getmtime)

    # Get the last modified file in the local folder
    file_path = get_last_modified_file(local_folder)
    if not file_path:
        print("No files found in the specified folder.")
        return False
    
    print("Last modified file:", file_path)
    file_name = os.path.basename(file_path)

    # 1. Autenticación (con MFA si hace falta)
    print("Autorización de credencial...")
    credential = InteractiveBrowserCredential()
    print("Autorización exitosa...")

    # 3. Subida también a SharePoint con Graph
    token = credential.get_token("https://graph.microsoft.com/.default").token
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/octet-stream"
    }

    resp = requests.get(
    "https://graph.microsoft.com/v1.0/sites/epeccba.sharepoint.com/sites/PROTELEM-INDICADORES",
    headers=headers
    )
    print(resp.json())

    resp = requests.get(
    "https://graph.microsoft.com/v1.0/sites?search=PROTELEM", 
    headers=headers
    )
    print(resp.json())

    with open(file_path, "rb") as f:
        content = f.read()

    # URL para cargar directo en la librería
    upload_url = (
        f"https://graph.microsoft.com/v1.0/sites/{base_path.replace('https://','')}:/{site_name}:/drive/root:/{nested_folder}/{file_name}:/content"
    )

    resp = requests.put(upload_url, headers=headers, data=content)

    if resp.status_code in (200, 201):
        print("Archivo subido con éxito a SharePoint!")
    else:
        print("Error subiendo a SharePoint:", resp.status_code, resp.text)





