import requests
import re

TOKEN = "7587271823:AAH0IPahMLq7SZMhHg6UMpHDw2Z97iSiS8I"  # Reemplaza con tu token
CHAT_ID = "1762109746"  # Reemplaza con tu chat ID (ver paso 3)
URL_BASE = f"https://api.telegram.org/bot{TOKEN}"
ultimo_update_id = 0

def alerta_error(mensaje, parse_mode="Markdown"):
    """
    Envía un mensaje a un bot de Telegram.

    :param mensaje: Texto del mensaje a enviar
    :param parse_mode: Formato del mensaje (Markdown, HTML o None)
    :return: Respuesta de la API de Telegram
    """
    url = f"{URL_BASE}/sendMessage"
    params = {
        "chat_id": CHAT_ID,
        "text": mensaje,
        "parse_mode": parse_mode
    }
    response = requests.get(url, params=params)
    return response.json()

def recibir_mensajes():
    global ultimo_update_id
    url = f"{URL_BASE}/getUpdates?offset={ultimo_update_id + 1}"
    response = requests.get(url)
    datos = response.json()

    if "result" in datos:
        for mensaje in datos["result"]:
            update_id = mensaje["update_id"]
            if update_id > ultimo_update_id:
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
            output = coincidencia.group(1)
        else:
            if mensaje and mensaje[0].isdigit():
                output = mensaje[0]
            else:
                output = '5'
    else:
        output = 0
    return output
