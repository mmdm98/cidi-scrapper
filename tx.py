import requests
import re
import logging
from credentials import read_credentials

logger = logging.getLogger(__name__)

_token, _chat_id = read_credentials('tx_credentials.txt')
TOKEN    = _token   or ""
CHAT_ID  = _chat_id or ""
URL_BASE = f"https://api.telegram.org/bot{TOKEN}"
ultimo_update_id = 0


def alerta_error(mensaje, parse_mode="Markdown"):
    if not TOKEN:
        logger.warning("Telegram no configurado — mensaje suprimido: %s", mensaje)
        return None
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
                logger.info("Mensaje recibido: %s", texto)
                var = text_analysis(texto)
                logger.info("Análisis: %s", var)
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
