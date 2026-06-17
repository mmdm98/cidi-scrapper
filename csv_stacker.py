import os
import glob
import re
import pandas as pd
from datetime import datetime, timedelta
from onelake import *
#########################################################################################
# Diccionario de categorías con sus patrones asociados
categorias_regex = {
    "ALTA SERVICIO": r"\balta\b|\bsolicitud.*servicio\b",
    "BAJA DE SERVICIO": r"\bbaja\b.*\bservicio\b",
    "CAMBIO TITULARIDAD": r"cambio.*titular",
    "CONSULTA-TRAMITE WEB": r"\bweb\b|\btrámite\b",
    "CONSULTA-CONSUMO": r"\bconsumo\b",
    "CONSULTA-DEUDA": r"\bdeuda\b|\bsaldo\b",
    "CONSULTA-RETIRO/CORTE": r"\bretiro\b|\bcorte\b",
    "CONSULTA-SEGMENTACION ENERGETICA": r"\bsegmentaci[oó]n\b|\bsubsidio\b",
    "CUMPLIMIENTO DE REQUISITOS": r"\brequisito\b|\bcumplimiento\b",
    "RECLAMO POR FACTURACION": r"\bfactura\b|\bfacturaci[oó]n\b|\berror.*importe\b",
    "FINANCIACION": r"\bfinanciaci[oó]n\b|\bcuotas\b",
    "ILICITO": r"\bil[ií]cito\b|\bil[ií]citos\b|\bfraude\b",
    "RECLAMO ARTEFACTOS QUEMADOS": r"\bquemado\b|\bartefacto\b|\bdan[oñ]ado\b",
    "REGISTRO EN LA PAGINA WEB / ALTA CIDI": r"\bregistro\b|\bcidi\b|\balta.*web\b",
}
#########################################################################################
# Función para clasificar usando regex
def clasificar_regex(comentario):
    if pd.isna(comentario):
        return "SIN COMENTARIO"
    
    comentario = comentario.lower()
    for categoria, patron in categorias_regex.items():
        if re.search(patron, comentario, re.IGNORECASE):
            return categoria
    return "NO CLASIFICADO"

def merge_csv_files(csv_directory, output_folder, date, turnero_or_client):
    # Ensure the output folder exists, create it if necessary
    os.makedirs(output_folder, exist_ok=True)

    # List all CSV files in the directory
    csv_files = glob.glob(os.path.join(csv_directory, '*.csv'))

    # Initialize an empty list to store all dataframes
    all_data = []

    # Read each CSV file and append to the list
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        all_data.append(df)

    # Concatenate all dataframes into one
    merged_df = pd.concat(all_data, ignore_index=True)

    # Generate a timestamp
    # timestamp = datetime.now().strftime('%Y-%m-%d')

    # timestamp = datetime.today().date() - timedelta(days=1)

    # Define the output file path
    if   turnero_or_client == 'COMENTARIOS':
    # Aplicar la clasificación
        merged_df['Datos_Particulares'] = merged_df['Comentarios'].apply(clasificar_regex)
        output_file = os.path.join(output_folder, f'CACs_Comments_{date}.csv')
        cacs_or_comments = "COMM"
    elif turnero_or_client == 'TURNERO':
        output_file = os.path.join(output_folder, f'CACs_{date}.csv')
        cacs_or_comments = "CACS"

    # Write merged dataframe to CSV
    merged_df.to_csv(output_file, index=False)

    print(f'Merged CSV file "{output_file}" has been created successfully.')

    if cacs_or_comments == "CACS":
        print(F'Uploading "{output_file}" to onelake . . .')
        guardar_en_onelake(cacs_or_comments, f'CACs_{date}.csv')

