#Install the correct packages first in the same folder as this file. 
#pip install azure-storage-file-datalake azure-identity

from azure.storage.filedatalake import (
    DataLakeServiceClient,
    DataLakeDirectoryClient,
    FileSystemClient
)
from azure.identity import DefaultAzureCredential
from azure.identity import InteractiveBrowserCredential
import os

# Set your account, workspace, and item path here
ACCOUNT_NAME       = "onelake"
WORKSPACE_NAME     = "Protelem - Premium"
DATA_PATH_CACs     = "LH_CIDI.Lakehouse/Files/CACs"
DATA_PATH_COMMENTS = "LH_CIDI.Lakehouse/Files/CACs_Comments"

def upload_file_to_directory(directory_client: DataLakeDirectoryClient, local_path: str, file_name: str):
    file_client = directory_client.get_file_client(file_name)
    # Opción 1: archivos chicos
    with open(os.path.join(local_path, file_name), "rb") as data:
        file_client.upload_data(data.read(), overwrite=True)
    # Opción 2: archivos grandes (más eficiente):
    # file_client.upload_file(os.path.join(local_path, file_name), overwrite=True)

def guardar_en_onelake(cacs_or_comm, file_name):
    #Create a service client using the default Azure credential

    print("Autorización de Credencial...")
    credential = InteractiveBrowserCredential()
    print("Autorización Exitosa...")

    account_url = f"https://{ACCOUNT_NAME}.dfs.fabric.microsoft.com"
    #token_credential = DefaultAzureCredential()
    service_client = DataLakeServiceClient(account_url, credential=credential)

    #Create a file system client for the workspace
    file_system_client = service_client.get_file_system_client(WORKSPACE_NAME)

    if cacs_or_comm == "CACS":
        #List a directory within the filesystem
        paths = file_system_client.get_paths(path=DATA_PATH_CACs)
    else:
        #List a directory within the filesystem
        paths = file_system_client.get_paths(path=DATA_PATH_COMMENTS)

    # Todo lo que trae paths:
    # for path in paths:
    # print(f"Nombre: {path.name}")
    # print(f"Tamaño: {path.content_length}")
    # print(f"Última modificación: {path.last_modified}")
    # print(f"Creado: {path.creation_time}")
    # print("-----")


    print("\n Archivos en el Path de OneLake")
    for path in paths:
        print(f'{path.name} + {path.last_modified}' + '\n')

    if cacs_or_comm == "CACS":
        directory_client = file_system_client.get_directory_client(DATA_PATH_CACs)
    else:
        directory_client = file_system_client.get_directory_client(DATA_PATH_COMMENTS)


    if cacs_or_comm == "CACS":
        # Subir archivo
        upload_file_to_directory(
            directory_client=directory_client,
            local_path = "D:/Usuarios/mdelgadillo/Desktop/xCodes/xSources/cidi/3_filtered_data/",
            file_name  = file_name
        )
    else:
        # Subir archivo
        upload_file_to_directory(
            directory_client=directory_client,
            local_path = "D:/Usuarios/mdelgadillo/Desktop/xCodes/xSources/cidi/6_comments_filtered_data/",
            file_name  = file_name
        )


    print("Archivo subido con éxito!")

# if __name__ == "__main__":
#     main()