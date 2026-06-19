import pandas as pd
import os
from glob import glob
from onelake import *

def delete_columns_in_csv(folder_path):
    columns_to_delete = [
        'Estado', 'Tramite', 'Id_Tramite_Relevado', 'Turno', 'Id_Estado',
        'Agente', 'Color', 'Notifica_Usuario', 'Notifica_Agenda', 'Id_Agenda',
        'N_Agenda', 'Id_Modalidad', 'N_Centro_Atencion', 'Id_Centro_Atencion',
        'Sticker_SUAC'
    ]

    csv_files = glob(os.path.join(folder_path, '*.csv'))
    if not csv_files:
        print("No CSV files found in the specified folder.")
        return

    latest_csv_file = max(csv_files, key=os.path.getmtime)
    output_csv_path = latest_csv_file

    df = pd.read_csv(latest_csv_file)
    df.drop(columns=columns_to_delete, inplace=True, errors='ignore')
    df.to_csv(output_csv_path, index=False)

    print(f"CSV file '{output_csv_path}' with specified columns deleted has been created successfully.")
    print("Guardando en Onelake . . .")

    guardar_en_onelake(TYPE_COMMENTS, os.path.basename(output_csv_path), local_folder=folder_path)
