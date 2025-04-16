import extract_msg
from utils.errores import ExtractionError


def extraer_texto_de_msg(path):
    try:
        msg = extract_msg.Message(path)
        msg_message = msg.date + "\n" + msg.subject + "\n" + msg.body
        return msg_message
    except Exception as e:
        raise ExtractionError(f"❌ Error extrayendo texto de archivo MSG: {e}", archivo=path)