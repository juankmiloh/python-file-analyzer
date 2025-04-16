import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from utils.errores import ExtractionError


def extraer_texto_pdf(path):
    try:
        with fitz.open(path) as doc:
            return " ".join(page.get_text() for page in doc)
    except Exception as e:
        raise ExtractionError(f"❌ Error leyendo PDF con PyMuPDF: {e}", archivo=path)
    
def extraer_texto_pdf_con_ocr(path):
    try:
        texto = ""
        with fitz.open(path) as doc:
            for page in doc:
                pix = page.get_pixmap(dpi=300)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                texto += pytesseract.image_to_string(img, lang="spa") + "\n"
        return texto
    except Exception as e:
        raise ExtractionError(f"❌ Error en OCR de PDF escaneado: {e}", archivo=path)