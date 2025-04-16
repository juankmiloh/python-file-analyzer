import concurrent.futures
import os
import re
from tqdm import tqdm
from utils.configuracion import PALABRAS_CLAVE, rutaOutput, logger
from extractores.pdf import extraer_texto_pdf
from extractores.office import (
    extraer_texto_docx,
    extraer_texto_doc,
    extraer_texto_xlsx,
    extraer_texto_odt,
    extraer_texto_pptx,
)
from extractores.imagenes import extraer_texto_ocr_imagen
from extractores.msg import extraer_texto_de_msg
from extractores.pdf import extraer_texto_pdf_con_ocr
from procesamiento.persistencia import cargar_archivos_procesados, guardar_archivos_procesados
from utils.normalizacion import normalizar
from utils.errores import ExtractionError


def analizar_documentos(ruta, incluir_resumen, forzar_reprocesamiento=False):
    resultados_nuevos = []
    archivos = []
    procesados = set()

    if not forzar_reprocesamiento:
        procesados = cargar_archivos_procesados(rutaOutput)

    for root, dirs, files in os.walk(ruta):
        for file in files:
            path = os.path.abspath(os.path.join(root, file))
            if path not in procesados:
                if not any(ext in os.path.basename(path).lower() for ext in [".ds_store", ".zip", ".rar", ".mpp"]): # Archivos excluidos
                    archivos.append(path)

    logger.info(f"⚙️  {len(archivos)} archivos nuevos por procesar.")
    nuevos_procesados = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futuras = {executor.submit(procesar_archivo, path, incluir_resumen, logger): path for path in archivos}
        for future in tqdm(concurrent.futures.as_completed(futuras), total=len(futuras), desc="Nivel de procesamiento"):
            path = futuras[future]
            try:
                resultado = future.result()
                if resultado:
                    resultados_nuevos.append(resultado)
                    nuevos_procesados.append(path)
                else:
                    logger.error(f"❌ Error procesando archivo: {path}")
            except Exception as e:
                logger.error(f"❌ Error procesando archivo {path}: {e}")

    guardar_archivos_procesados(nuevos_procesados, rutaOutput)

    return resultados_nuevos

def procesar_archivo(path, incluir_resumen, logger):
    tqdm.write(f"🔄 Procesando archivo: {path}")
    nombre = os.path.basename(path)
    extension = os.path.splitext(nombre)[1].lower().lstrip('.')

    # Validar tamaño del archivo (en bytes)
    max_size_mb = 260
    max_size_bytes = max_size_mb * 1024 * 1024
    if os.path.getsize(path) > max_size_bytes:
        logger.warning(f"🚫 Archivo ignorado por exceder los {max_size_mb}MB: {path}")
        return None

    texto = ""
    tipo = extension.upper()

    try:
        if extension == "pdf":
            try:
                texto = extraer_texto_pdf(path)
                if not texto.strip():
                    logger.info(f"📄 PDF vacío o escaneado. Intentando OCR: {path}")
                    texto = extraer_texto_pdf_con_ocr(path)
            except ExtractionError as e:
                logger.warning(f"⚠️ Error leyendo PDF. Intentando OCR: {path}")
                texto = extraer_texto_pdf_con_ocr(path)
        elif extension in ["png", "jpg", "jpeg", "tiff"]:
            texto = extraer_texto_ocr_imagen(path)
        elif extension == "docx":
            texto = extraer_texto_docx(path)
        elif extension == "doc":
            texto = extraer_texto_doc(path)
        elif extension == "xlsx":
            texto = extraer_texto_xlsx(path)
        elif extension in ["txt", "csv"]:
            with open(path, 'r', encoding="utf-8", errors="ignore") as f:
                texto = f.read()
        elif extension == "odt":
            texto = extraer_texto_odt(path)
        elif extension == "pptx":
            texto = extraer_texto_pptx(path)
        elif extension == "msg":
            texto = extraer_texto_de_msg(path)
        else:
            return None
    except ExtractionError as e:
        logger.error(f"⚠️  Archivo no permitido: {path}: {e}")
        return None

    texto_normalizado = normalizar(texto)
    coincidencias = {
        palabra: len(re.findall(rf"\b{re.escape(normalizar(palabra))}\b", texto_normalizado))
        for palabra in PALABRAS_CLAVE
    }
    total = sum(coincidencias.values())

    resultado = {
        "ruta": path,
        "nombre": nombre,
        "tipo": tipo,
        "coincidencias": total,
        "detalle": coincidencias
    }

    if incluir_resumen:
        frases = re.split(r'(?<=[\.\n])\s+', texto)
        resumen_por_palabra = {}

        for palabra in PALABRAS_CLAVE:
            frases_encontradas = []
            palabra_normalizada = normalizar(palabra)

            for frase in frases:
                frase_normalizada = normalizar(frase)
                if re.search(rf"\b{re.escape(palabra_normalizada)}\b", frase_normalizada):
                    frases_encontradas.append(frase.strip())

            if frases_encontradas:
                resumen_por_palabra[palabra] = frases_encontradas

        resultado["resumen"] = resumen_por_palabra or {"sin_resultados": ["No se encontraron frases con palabras clave."]}

    return resultado