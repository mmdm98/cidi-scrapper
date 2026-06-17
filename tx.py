import requests
import time
import re

TOKEN = "7587271823:AAH0IPahMLq7SZMhHg6UMpHDw2Z97iSiS8I"  # Reemplaza con tu token
CHAT_ID = "1762109746"  # Reemplaza con tu chat ID (ver paso 3)
URL_BASE = f"https://api.telegram.org/bot{TOKEN}"
ultimo_update_id = 0

def alerta_error(mensaje, parse_mode="Markdown"):
    """
    Envía un mensaje a un bot de Telegram.

    :param token: Token del bot de Telegram
    :param chat_id: ID del chat o grupo
    :param mensaje: Texto del mensaje a enviar
    :param parse_mode: Formato del mensaje (Markdown, HTML o None)
    :return: Respuesta de la API de Telegram
    """
    
    url = f"{URL_BASE}/sendMessage"
    params = {
        "chat_id": CHAT_ID,
        "text": mensaje,
        "parse_mode": parse_mode  # Markdown, HTML o None
    }

    response = requests.get(url, params=params)
    return response.json()  # Devuelve la respuesta de la API

def recibir_mensajes():
    global ultimo_update_id
    url = f"{URL_BASE}/getUpdates?offset={ultimo_update_id + 1}"
    response = requests.get(url)
    datos = response.json()

    if "result" in datos:
        for mensaje in datos["result"]:
            update_id = mensaje["update_id"]
            if update_id > ultimo_update_id:  # Solo mensajes nuevos
                ultimo_update_id = update_id
                chat_id = mensaje["message"]["chat"]["id"]
                texto = mensaje["message"]["text"]
                print(f"Mensaje recibido: {texto}")
                var = text_analysis(texto)
                print(var)
                responder_mensaje(chat_id, texto)

def responder_mensaje(chat_id, mensaje):
    url = f"{URL_BASE}/sendMessage"
    params = {"chat_id": chat_id, "text": f"Entendido! {mensaje}"}
    requests.get(url, params=params)

def text_analysis(mensaje):
    date_pattern = r"Fecha:\s*(\d{4}-\d{2}-\d{2})"

    coincidencia = re.search(date_pattern, mensaje)
    if mensaje:
        if coincidencia:
            output = coincidencia.group(1)  # Captura solo la fecha
            #print(f"Fecha encontrada: {fecha}")
        else:
            if mensaje and mensaje[0].isdigit(): #Verificamos si no esta vacio y que sea un numero
                output = mensaje[0]
            else:
                output = '5'
    else:
        output = 0
    return output


# # Bucle para revisar mensajes cada 5 segundos
# while True:
#     recibir_mensajes()
#     time.sleep(5)


# import requests
# import time
# import re
# from menu import *

# TOKEN = "7587271823:AAH0IPahMLq7SZMhHg6UMpHDw2Z97iSiS8I"  # Reemplaza con tu token
# CHAT_ID = "1762109746"  # Reemplaza con tu chat ID (ver paso 3)
# URL_BASE = f"https://api.telegram.org/bot{TOKEN}"
# ultimo_update_id = 0  # Variable para guardar el último update_id procesado

# def alerta_error(mensaje, parse_mode="Markdown"):
#     url = f"{URL_BASE}/sendMessage"
#     params = {
#         "chat_id": CHAT_ID,
#         "text": mensaje,
#         "parse_mode": parse_mode  # Markdown, HTML o None
#     }
#     response = requests.get(url, params=params)
#     return response.json()

# def recibir_mensajes():
#     global ultimo_update_id
#     url = f"{URL_BASE}/getUpdates?offset={ultimo_update_id + 1}"  # Añadido el offset
#     response = requests.get(url)
#     datos = response.json()

#     if "result" in datos:
#         for mensaje in datos["result"]:
#             update_id = mensaje["update_id"]
#             if update_id > ultimo_update_id:  # Solo procesar mensajes con update_id mayores al último
#                 ultimo_update_id = update_id  # Actualiza el último update_id procesado
#                 chat_id = mensaje["message"]["chat"]["id"]
#                 texto = mensaje["message"]["text"]
#                 print(f"Mensaje recibido: {texto}")
#                 var = text_analysis(texto)
#                 responder_mensaje(chat_id, texto)

#     # Esto deberia retornar var, que se puede usar en el menu

# def responder_mensaje(chat_id, mensaje):
#     url = f"{URL_BASE}/sendMessage"
#     params = {"chat_id": chat_id, "text": f"{mensaje}"}
#     requests.get(url, params=params)

# def text_analysis(mensaje):
#     date_pattern = r"Fecha:\s*(\d{4}-\d{2}-\d{2})"
#     coincidencia = re.search(date_pattern, mensaje)
#     if coincidencia:
#         output = coincidencia.group(1)  # Captura solo la fecha
#     else:
#         if mensaje and mensaje[0].isdigit():  # Verificamos si no está vacío y es un número
#             output = mensaje[0]
#         else:
#             output = '5'
#     return output

# # Bucle para revisar mensajes cada 5 segundos
# responder_mensaje(CHAT_ID, menu(1))
# while True:
#     recibir_mensajes()
#     time.sleep(5)
