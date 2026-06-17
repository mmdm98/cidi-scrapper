#--------------------------------------------------------------------------------------------------------------------
# CIDI_SCRAPPER.PY
#--------------------------------------------------------------------------------------------------------------------
import warnings

from csv_stacker            import *
from csv_parser             import *
from csv_process            import *
from turnero_scrapper       import *
from menu                   import *
from credentials            import *
from sharepoint             import *
from client_info_scrapper   import *
from file_destructor        import *
from tx                     import *
from datetime import datetime, timedelta

# MAIN
warnings.filterwarnings("ignore")

# Specify the path to the paths text file
paths_file = 'D:/Usuarios/mdelgadillo/Desktop/xCodes/xSources/cidi/paths.txt'

# Read paths from the text file
paths = read_paths_from_file(paths_file)

if len(paths) == 8:
    cidi_credentials_file       = paths[0]
    sharepoint_credentials_file = paths[1]
    folder_path                 = paths[2]
    output_folder               = paths[3]
    filtered_folder             = paths[4]
    comment_folder_path         = paths[5]
    comment_output_folder       = paths[6]
    comment_filtered_folder     = paths[7]
else:
    print("Incorrect number of paths read from file. Check the content.")

#opcion_seleccionada = mostrar_popup('IMPORTANT WARNING', '¿Borrar todo?')
#print(f'Usted ha seleccionado borrar todo: {opcion_seleccionada}')

deleting_paths_csv  = [2,5]
deleting_paths_html = [3,6]

extensiones = {
    'html': deleting_paths_csv,
    'csv': deleting_paths_html
}

for extension, indices in extensiones.items():
    for index in indices:
        if index < len(paths):
            borrar_archivos(extension, paths[index])
        else:
            print(f'Índice fuera de rango para archivos {extension.upper()}: {index}')

# Read CUIL and SHAREPOINT and password from the text file
cidi_cuil, cidi_password = read_credentials(cidi_credentials_file)
sharepoint_username, sharepoint_password = read_credentials(sharepoint_credentials_file)

sharepoint_site_name              = 'PROTELEM-INDICADORES'
sharepoint_base_path              = 'https://epeccba.sharepoint.com/'
sharepoint_nested_folder          = 'Documentos compartidos/m_actividad_turnero_cidi'
sharepoint_nested_folder_comments = 'Documentos compartidos/m_comentarios_turnero_cidi'

# Locking a el dia de la fecha
current_date = datetime.today().date() - timedelta(days=1)

# Dictionary of Centro de Atención IDs and descriptions
# centros_de_atencion = {
#     1825: 'EPEC CENTRO DE ATENCION COMERCIAL ESTE',
#     1824: 'EPEC CENTRO DE ATENCION COMERCIAL NORTE',
#     1823: 'EPEC CENTRO DE ATENCION COMERCIAL SUR',
#     1766: 'EPEC CENTRO DE ATENCION COMERCIAL TERMINAL DE ÓMNIBUS',
#     1826: 'EPEC CPC ARGUELLO - LOCAL 3'
# }

# centros_de_atencion = {
#     1823: 'EPEC CENTRO DE ATENCION COMERCIAL SUR'
# }

centros_de_atencion = {
    # 1766: 'EPEC CENTRO DE ATENCION COMERCIAL TERMINAL DE ÓMNIBUS'
    1825: 'EPEC CENTRO DE ATENCION COMERCIAL ESTE', #A
    1824: 'EPEC CENTRO DE ATENCION COMERCIAL NORTE',#A
    1823: 'EPEC CENTRO DE ATENCION COMERCIAL SUR',#A
    1766: 'EPEC CENTRO DE ATENCION COMERCIAL TERMINAL DE ÓMNIBUS',#A
    1826: 'EPEC CPC ARGUELLO - LOCAL 3',#A # NUEVOS 20 CAC
    1789: 'EPEC CENTRO DE ATENCION COMERCIAL LA CUMBRE', #de este no hay nada
    1782: 'EPEC CENTRO DE ATENCION COMERCIAL ALEJANDRO',
    1785: 'EPEC CENTRO DE ATENCION COMERCIAL ALEJO LEDESMA',
    1818: 'EPEC CENTRO DE ATENCION COMERCIAL ALTA GRACIA',
    1783: 'EPEC CENTRO DE ATENCION COMERCIAL ARIAS',
    1793: 'EPEC CENTRO DE ATENCION COMERCIAL BALLESTEROS',#C
    1802: 'EPEC CENTRO DE ATENCION COMERCIAL BALNEARIA',
    1805: 'EPEC CENTRO DE ATENCION COMERCIAL BELL VILLE',
    1784: 'EPEC CENTRO DE ATENCION COMERCIAL BUCHARDO',
    1790: 'EPEC CENTRO DE ATENCION COMERCIAL CAPILLA DEL MONTE', #B
    1810: 'EPEC CENTRO DE ATENCION COMERCIAL CORRAL DE BUSTOS',
    1791: 'EPEC CENTRO DE ATENCION COMERCIAL COSQUIN', #B
    1809: 'EPEC CENTRO DE ATENCION COMERCIAL CRUZ ALTA',
    1786: 'EPEC CENTRO DE ATENCION COMERCIAL CRUZ DEL EJE',#B
    1776: 'EPEC CENTRO DE ATENCION COMERCIAL JAMES CRAIK',
    1817: 'EPEC CENTRO DE ATENCION COMERCIAL LA CALERA',
    1822: 'EPEC CENTRO DE ATENCION COMERCIAL LA CARLOTA',
    1788: 'EPEC CENTRO DE ATENCION COMERCIAL LA FALDA',#B
    1806: 'EPEC CENTRO DE ATENCION COMERCIAL MARCOS JUAREZ',
    1811: 'EPEC CENTRO DE ATENCION COMERCIAL MONTE MAIZ', #NUEVOS 19 CACS
    1801: 'EPEC CENTRO DE ATENCION COMERCIAL DEVOTO', #si
    1813: 'EPEC CENTRO DE ATENCION COMERCIAL ISLA VERDE', #SI
    1794: 'EPEC CENTRO DE ATENCION COMERCIAL LABORDE', #si
    1807: 'EPEC CENTRO DE ATENCION COMERCIAL LEONES', #SI
    1808: 'EPEC CENTRO DE ATENCION COMERCIAL LOS SURGENTES', #SI
    1812: 'EPEC CENTRO DE ATENCION COMERCIAL NOETINGER', #SI
    1815: 'EPEC CENTRO DE ATENCION COMERCIAL RIO CEBALLOS',#si
    1821: 'EPEC CENTRO DE ATENCION COMERCIAL RIO CUARTO', #SI
    1819: 'EPEC CENTRO DE ATENCION COMERCIAL RIO SEGUNDO',#si
    1800: 'EPEC CENTRO DE ATENCION COMERCIAL SAN FRANCISCO',#si
    1777: 'EPEC CENTRO DE ATENCION COMERCIAL SAN FRANCISCO DEL CHAÑAR',
    1778: 'EPEC CENTRO DE ATENCION COMERCIAL SANTIAGO TEMPLE',#si
    1796: 'EPEC CENTRO DE ATENCION COMERCIAL TANCACHA',#si
    1797: 'EPEC CENTRO DE ATENCION COMERCIAL UCACHA',#si
    1816: 'EPEC CENTRO DE ATENCION COMERCIAL VILLA ALLENDE',
    1803: 'EPEC CENTRO DE ATENCION COMERCIAL VILLA CARLOS PAZ',
    1780: 'EPEC CENTRO DE ATENCION COMERCIAL VILLA DE MARIA', #si
    1787: 'EPEC CENTRO DE ATENCION COMERCIAL VILLA DEL TOTORAL',#si
    1798: 'EPEC CENTRO DE ATENCION COMERCIAL VILLA MARIA',
    1814: 'EPEC CENTRO DE ATENCION COMERCIAL MORRISON' #SI
}

#agregar GENERAL CABRERA, PASCANAS
# log
# 12/8/25 - no estan en el cidi

menu_locker = 1

while menu_locker == 1:
    menu(0)
    mes_actual = datetime.now().strftime('%B')  # Nombre del mes en inglés
    anio_actual = datetime.now().strftime('%Y')
    print(f'\n ESTAMOS EN EL MES DE {mes_actual.upper()}{anio_actual.upper()} \n')
    lake_or_local = input()
    if lake_or_local == '2':
        print("Attepting to connect ...")
        fetch_and_save_data(cidi_cuil, cidi_password, centros_de_atencion, folder_path, current_date, current_date)
        print("Downloaded data ...")
        convert_html_files_to_csv(folder_path, output_folder, 0)
        print("Filtering data...")
        merge_csv_files(output_folder, filtered_folder, current_date, 'TURNERO')
        download_comment = input("Download Comment Data? [Y] or [N]: ").upper()
        if download_comment == 'Y':
            fetch_and_save_comment_data(cidi_cuil, cidi_password, centros_de_atencion, comment_folder_path, current_date, current_date)
            print("Downloaded data ...")
            convert_html_files_to_csv(comment_folder_path, comment_output_folder, 1)
            print("Filtering data...")
            merge_csv_files(comment_output_folder, comment_filtered_folder, current_date, 'COMENTARIOS')
            delete_columns_in_csv(comment_filtered_folder)
            upload_or_not = input("Upload Comment Data to SharePoint? [Y] or [N]: ").upper()
            if upload_or_not == 'Y':
                print("Uploading...")
                upload_success = upload_file_to_sharepoint(sharepoint_username, sharepoint_password, sharepoint_site_name, sharepoint_base_path, sharepoint_nested_folder_comments, comment_filtered_folder)
            else:
                print("No subimos nada...")
        else:
            print("No descargado ...")

    elif lake_or_local == '1':
        print("Uploading...")
        upload_success = upload_file_to_sharepoint(sharepoint_username, sharepoint_password, sharepoint_site_name, sharepoint_base_path, sharepoint_nested_folder, filtered_folder)
    elif lake_or_local == '3':
        print("Type the day you want to download (YYYY-MM-DD): ")
        current_date = input()
        print("Attepting to connect ...")
        fetch_and_save_data(cidi_cuil, cidi_password, centros_de_atencion, folder_path, current_date, current_date)
        print("Downloaded data ...")
        convert_html_files_to_csv(folder_path, output_folder, 0)
        print("Filtering data...")
        merge_csv_files(output_folder, filtered_folder, current_date, 'TURNERO')
    elif lake_or_local == '4':
        print("Type the day you want to download (YYYY-MM-DD): ")
        current_date = input()
        print("Attepting to connect ...")
        fetch_and_save_comment_data(cidi_cuil, cidi_password, centros_de_atencion, comment_folder_path, current_date, current_date)
        print("Downloaded data ...")
        convert_html_files_to_csv(comment_folder_path, comment_output_folder, 1)
        print("Filtering data...")
        merge_csv_files(comment_output_folder, comment_filtered_folder, current_date, 'COMENTARIOS')
        delete_columns_in_csv(comment_filtered_folder)
        upload_or_not = input("Upload Comment Data to SharePoint? [Y] or [N]: ").upper()
        if upload_or_not == 'Y':
            print("Uploading...")
            upload_success = upload_file_to_sharepoint(sharepoint_username, sharepoint_password, sharepoint_site_name, sharepoint_base_path, sharepoint_nested_folder_comments, comment_filtered_folder)
        else:
            print("No subimos nada...")
    elif lake_or_local == '5':
        print("Exiting...")
        menu_locker = 0
    elif lake_or_local == '6':
        print("CUSTOM DEV MODE")
        cantidad_de_fechas = input("Ingrese la cantidad de fechas: ")
        cantidad_de_fechas = int(cantidad_de_fechas)
        array_de_fechas = []
        for i in range(cantidad_de_fechas):
            fecha = input(f"Enter date {i + 1} (YYYY-MM-DD): ")
            array_de_fechas.append(fecha)
        
        for fecha in array_de_fechas:
            current_date = fecha
            print(" ################################ FECHA " + fecha + " ################################")
            print("Attepting to connect ...")
            fetch_and_save_data(cidi_cuil, cidi_password, centros_de_atencion, folder_path, current_date, current_date)
            print("Downloaded data ...")
            convert_html_files_to_csv(folder_path, output_folder, 0)
            print("Filtering data...")
            merge_csv_files(output_folder, filtered_folder, current_date, 'TURNERO')

            print("Uploading...")
            upload_success = upload_file_to_sharepoint(sharepoint_username, sharepoint_password, sharepoint_site_name, sharepoint_base_path, sharepoint_nested_folder, filtered_folder)

            print(" ################################################################ ")
        print("Exiting...")
        menu_locker = 0
    elif lake_or_local == '7':
        print("DEVS 2nd desde hasta 1 archivo")
        comment_or_general = 0
        comment_or_general = input(f"Enter 1 for data, 2 for comments: ")
        desde  = input(f"Enter date (YYYY-MM-DD): ")
        hasta  = input(f"Enter date (YYYY-MM-DD): ")
        period = desde + "-" + hasta 
        print(" ################### DESDE " + desde + " HASTA " + hasta + "#####################")
        print("Attepting to connect ...")
        if comment_or_general == "1":
            fetch_and_save_data(cidi_cuil, cidi_password, centros_de_atencion, folder_path, desde, hasta)
            print("Downloaded data ...")
            convert_html_files_to_csv(folder_path, output_folder, 0)
            print("Filtering data...")
            merge_csv_files(output_folder, filtered_folder, period, 'TURNERO')

            print("Uploading...")
            upload_success = upload_file_to_sharepoint(sharepoint_username, sharepoint_password, sharepoint_site_name, sharepoint_base_path, sharepoint_nested_folder, filtered_folder)

        if comment_or_general == "2":
            fetch_and_save_comment_data(cidi_cuil, cidi_password, centros_de_atencion, comment_folder_path, desde, hasta)
            print("Downloaded data ...")
            convert_html_files_to_csv(comment_folder_path, comment_output_folder, 1)
            print("Filtering data...")
            merge_csv_files(comment_output_folder, comment_filtered_folder, period, 'COMENTARIOS')
            delete_columns_in_csv(comment_filtered_folder)

            print("Uploading...")
            upload_success = upload_file_to_sharepoint(sharepoint_username, sharepoint_password, sharepoint_site_name, sharepoint_base_path, sharepoint_nested_folder, filtered_folder)

        else: 
            print(" o p c i o n  i n c o r r e c t a  h e r m a n o")
        print(" ################################################################ ")
        print("Exiting...")
        menu_locker = 0
    elif lake_or_local == '0':
        print("BORRAR TODO")
        for extension, indices in extensiones.items():
            for index in indices:
                if index < len(paths):
                    borrar_archivos(extension, paths[index])
                else:
                    print(f'Índice fuera de rango para archivos {extension.upper()}: {index}')
    else:
        print("Try again, wrong option ...")

# Notas:
# todavia se puede mejorar mucho en la parte de descargar fechas del historial
# hay que abusar del termino "desde" "hasta" para evitar escribir fechas
# el seleccionador de fechas puede servir para algo muuy puntual