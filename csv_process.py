# import pandas as pd

# def delete_columns_in_csv(input_csv_path, output_csv_path):
#     columns_to_delete = ['Estado', 'Tramite', 'Id_Tramite_Relevado', 'Turno', 'Id_Estado', 'Agente', 'Color', 'Notifica_Usuario', 'Notifica_Agenda', 'Id_Agenda', 'N_Agenda', 'Id_Modalidad', 'N_Centro_Atencion', 'Id_Centro_Atencion', 'Sticker_SUAC']
#     # Load CSV file into a DataFrame
#     df = pd.read_csv(input_csv_path)

#     # Delete specified columns
#     df.drop(columns=columns_to_delete, inplace=True, errors='ignore')

#     # Save modified DataFrame to a new CSV file
#     df.to_csv(output_csv_path, index=False)

#     print(f"CSV file '{output_csv_path}' with specified columns deleted has been created successfully.")

# Example usage
# input_csv_path    = 'D:/Usuarios/MDELGADILLO/Desktop/xCodes/xSources/cidi/6_comments_filtered_data/CACs_Comments_2024-07-24.csv'
# output_csv_path   = 'D:/Usuarios/MDELGADILLO/Desktop/xCodes/xSources/cidi/6_comments_filtered_data/CACs_Comments_2024-07-24.csv'
# columns_to_keep = ['Interesado', 'Cuil_Interesado', 'Id_Turno', 'Fec_Solicitado', 'Datos_Particulares', 'Comentarios']
# columns_to_delete = ['Estado', 'Tramite', 'Id_Tramite_Relevado', 'Turno', 'Id_Estado', 'Agente', 'Color', 'Notifica_Usuario', 'Notifica_Agenda', 'Id_Agenda', 'N_Agenda', 'Id_Modalidad', 'N_Centro_Atencion', 'Id_Centro_Atencion', 'Sticker_SUAC']

#delete_columns_in_csv(input_csv_path, output_csv_path, columns_to_delete)

import pandas as pd
import os
from glob import glob
from onelake import *

def delete_columns_in_csv(folder_path):
    # Define the columns to delete
    columns_to_delete = ['Estado', 'Tramite', 'Id_Tramite_Relevado', 'Turno', 'Id_Estado', 'Agente', 'Color', 'Notifica_Usuario', 'Notifica_Agenda', 'Id_Agenda', 'N_Agenda', 'Id_Modalidad', 'N_Centro_Atencion', 'Id_Centro_Atencion', 'Sticker_SUAC']
    
    # Get a list of all CSV files in the folder
    csv_files = glob(os.path.join(folder_path, '*.csv'))

    if not csv_files:
        print("No CSV files found in the specified folder.")
        return

    # Sort files by modification time and get the latest one
    latest_csv_file = max(csv_files, key=os.path.getmtime)
    
    # Define the output file path (overwrite the original file)
    output_csv_path = latest_csv_file

    # Load CSV file into a DataFrame
    df = pd.read_csv(latest_csv_file)

    # Delete specified columns
    df.drop(columns=columns_to_delete, inplace=True, errors='ignore')

    # Save modified DataFrame to the same CSV file
    df.to_csv(output_csv_path, index=False)

    print(f"CSV file '{output_csv_path}' with specified columns deleted has been created successfully.")

    print("Guardando en Onelake . . .")

    guardar_en_onelake("COMMENTS", os.path.basename(output_csv_path))

# # Example usage
# folder_path = 'D:/Usuarios/MDELGADILLO/Desktop/xCodes/xSources/cidi/6_comments_filtered_data'
# delete_columns_in_csv(folder_path)
