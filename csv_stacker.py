import os
import glob
import re
import logging
import pandas as pd
from onelake import *

logger = logging.getLogger(__name__)

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
def clasificar_regex(comentario):
    if pd.isna(comentario):
        return "SIN COMENTARIO"

    comentario = comentario.lower()
    for categoria, patron in categorias_regex.items():
        if re.search(patron, comentario, re.IGNORECASE):
            return categoria
    return "NO CLASIFICADO"

def merge_csv_files(csv_directory, output_folder, date, turnero_or_client):
    os.makedirs(output_folder, exist_ok=True)

    csv_files = glob.glob(os.path.join(csv_directory, '*.csv'))

    all_data = []
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        all_data.append(df)

    merged_df = pd.concat(all_data, ignore_index=True)

    if turnero_or_client == 'COMENTARIOS':
        merged_df['Datos_Particulares'] = merged_df['Comentarios'].apply(clasificar_regex)
        output_file = os.path.join(output_folder, f'CACs_Comments_{date}.csv')
        cacs_or_comments = TYPE_COMMENTS
    elif turnero_or_client == 'TURNERO':
        output_file = os.path.join(output_folder, f'CACs_{date}.csv')
        cacs_or_comments = TYPE_CACS

    merged_df.to_csv(output_file, index=False)
    logger.info('Merged CSV file "%s" has been created successfully.', output_file)

    if cacs_or_comments == TYPE_CACS:
        logger.info('Uploading "%s" to OneLake...', output_file)
        guardar_en_onelake(cacs_or_comments, f'CACs_{date}.csv', local_folder=output_folder)
