from azure.storage.filedatalake import DataLakeServiceClient, DataLakeDirectoryClient
from azure.identity import InteractiveBrowserCredential
import requests
import os

def upload_file_to_sharepoint(username, password, site_name, base_path, nested_folder, local_folder):
    def get_last_modified_file(folder_path):
        files = os.listdir(folder_path)
        if not files:
            return None
        paths = [os.path.join(folder_path, basename) for basename in files]
        return max(paths, key=os.path.getmtime)

    file_path = get_last_modified_file(local_folder)
    if not file_path:
        print("No files found in the specified folder.")
        return False

    print("Last modified file:", file_path)
    file_name = os.path.basename(file_path)

    print("Autorización de credencial...")
    credential = InteractiveBrowserCredential()
    print("Autorización exitosa...")

    token = credential.get_token("https://graph.microsoft.com/.default").token
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/octet-stream"
    }

    with open(file_path, "rb") as f:
        content = f.read()

    upload_url = (
        f"https://graph.microsoft.com/v1.0/sites/{base_path.replace('https://','')}:/{site_name}:/drive/root:/{nested_folder}/{file_name}:/content"
    )

    resp = requests.put(upload_url, headers=headers, data=content)

    if resp.status_code in (200, 201):
        print("Archivo subido con éxito a SharePoint!")
        return True
    else:
        print("Error subiendo a SharePoint:", resp.status_code, resp.text)
        return False
