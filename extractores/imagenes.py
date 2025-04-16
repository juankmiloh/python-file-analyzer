from PIL import Image
import pytesseract
from utils.errores import ExtractionError


def extraer_texto_ocr_imagen(path):
    try:
        imagen = Image.open(path)
        return pytesseract.image_to_string(imagen, lang="spa")
    except Exception as e:
        raise ExtractionError(f"❌ Error leyendo imagen con OCR: {e}", archivo=path)