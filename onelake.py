from azure.storage.filedatalake import DataLakeServiceClient, DataLakeDirectoryClient
from azure.identity import InteractiveBrowserCredential
import os

ACCOUNT_NAME       = "onelake"
WORKSPACE_NAME     = "Protelem - Premium"
DATA_PATH_CACs     = "LH_CIDI.Lakehouse/Files/CACs"
DATA_PATH_COMMENTS = "LH_CIDI.Lakehouse/Files/CACs_Comments"

TYPE_CACS     = "CACS"
TYPE_COMMENTS = "COMMENTS"

_DATA_PATHS = {
    TYPE_CACS:     DATA_PATH_CACs,
    TYPE_COMMENTS: DATA_PATH_COMMENTS,
}


def upload_file_to_directory(directory_client: DataLakeDirectoryClient, local_path: str, file_name: str):
    file_client = directory_client.get_file_client(file_name)
    with open(os.path.join(local_path, file_name), "rb") as data:
        file_client.upload_data(data.read(), overwrite=True)


def guardar_en_onelake(cacs_or_comm: str, file_name: str, local_folder: str):
    data_path = _DATA_PATHS[cacs_or_comm]  # KeyError si se pasa un tipo inválido

    print("Autorización de Credencial...")
    credential = InteractiveBrowserCredential()
    print("Autorización Exitosa...")

    account_url = f"https://{ACCOUNT_NAME}.dfs.fabric.microsoft.com"
    service_client = DataLakeServiceClient(account_url, credential=credential)
    file_system_client = service_client.get_file_system_client(WORKSPACE_NAME)

    print("\n Archivos en el Path de OneLake")
    for path in file_system_client.get_paths(path=data_path):
        print(f'{path.name} + {path.last_modified}\n')

    directory_client = file_system_client.get_directory_client(data_path)
    upload_file_to_directory(
        directory_client=directory_client,
        local_path=local_folder,
        file_name=file_name,
    )

    print("Archivo subido con éxito!")
