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
from datetime import datetime
import unicodedata
import locale


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

    # Buscar las fechas normalizadas en el texto
    fechas_normalizadas = extraer_fechas(texto_normalizado)

    fechas_coincidencias = {
        fecha: fechas_normalizadas.count(fecha)
        for fecha in fechas_normalizadas
        if fecha in PALABRAS_CLAVE
    }

    # Buscar coincidencias de palabras clave
    coincidencias = {
        palabra: len(re.findall(rf"\b{re.escape(normalizar(palabra))}\b", texto_normalizado))
        for palabra in PALABRAS_CLAVE
        if palabra not in fechas_coincidencias
    }

    print(f"🔍 [texto] Coincidencias encontradas: {coincidencias}")

    print(f"🔍 [fechas] Coincidencias encontradas: {fechas_coincidencias}")

    # Unir coincidencias y fechas_coincidencias
    coincidencias_actualizadas = coincidencias.copy()
    for fecha, count in fechas_coincidencias.items():
        coincidencias_actualizadas[fecha] = coincidencias_actualizadas.get(fecha, 0) + count
    coincidencias = coincidencias_actualizadas

    total = sum(coincidencias.values())

    print(f"🔍 Coincidencias encontradas en {coincidencias}")

    resultado = {
        "ruta": path,
        "nombre": nombre,
        "tipo": tipo,
        "coincidencias": total,
        "detalle": coincidencias,
        "fechas": fechas_normalizadas,  # Guardamos las fechas encontradas
    }

    if incluir_resumen:
        resumen = generar_resumen(texto, PALABRAS_CLAVE)
        resultado["resumen"] = resumen

    return resultado

def generar_resumen(texto, palabras_clave):
    frases = re.split(r'(?<=[\.\n])\s+', texto)
    resumen_por_palabra = {}

    frases_normalizadas = [normalizar(f) for f in frases]

    for palabra in palabras_clave:
        palabra_normalizada = normalizar(palabra)
        frases_encontradas = [
            frases[i].strip()
            for i, frase_norm in enumerate(frases_normalizadas)
            if re.search(rf"\b{re.escape(palabra_normalizada)}\b", frase_norm)
        ]
        if frases_encontradas:
            resumen_por_palabra[palabra] = frases_encontradas

    if not resumen_por_palabra:
        resumen_por_palabra["sin_resultados"] = ["No se encontraron frases con palabras clave."]

    return resumen_por_palabra

# Intentamos establecer el locale a español
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES')
    except locale.Error:
        pass

def remover_tildes(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

def normalizar_fecha(fecha_str):
    original = fecha_str.strip()
    sin_tildes = remover_tildes(original)

    # Reemplazos rápidos si solo es un mes
    meses_es = {
        "enero": "01/01", "febrero": "01/02", "marzo": "01/03", "abril": "01/04",
        "mayo": "01/05", "junio": "01/06", "julio": "01/07", "agosto": "01/08",
        "septiembre": "01/09", "octubre": "01/10", "noviembre": "01/11", "diciembre": "01/12"
    }
    meses_en = {
        "january": "01/01", "february": "01/02", "march": "01/03", "april": "01/04",
        "may": "01/05", "june": "01/06", "july": "01/07", "august": "01/08",
        "september": "01/09", "october": "01/10", "november": "01/11", "december": "01/12"
    }

    sin_tildes_lower = sin_tildes.lower()

    if sin_tildes_lower in meses_es:
        return f"{meses_es[sin_tildes_lower]}/2022"
    if sin_tildes_lower in meses_en:
        return f"{meses_en[sin_tildes_lower]}/2022"

    # Formatos comunes en español e inglés
    formatos = [
        "%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d",
        "%d de %B de %Y", "%d de %b de %Y",
        "%d de %B del %Y",
        "%B %d, %Y", "%b %d, %Y",
        "%d %B %Y", "%d %b %Y",
        "%d/%m/%y", "%d-%m-%y",
    ]

    # Probar primero con el texto original (para casos en inglés con mayúsculas)
    posibles = [original, sin_tildes, sin_tildes.title()]

    for texto in posibles:
        for formato in formatos:
            try:
                fecha = datetime.strptime(texto, formato)
                return fecha.strftime("%d/%m/%Y")
            except ValueError:
                continue

    return None

# Función para extraer todas las fechas del texto y normalizarlas
def extraer_fechas(texto):
    # Expresión regular para detectar fechas en diferentes formatos
    fecha_regex = r"(\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{4}[-/]\d{1,2}[-/]\d{1,2}|\d{1,2} de [a-zA-Z]+ de \d{4}|\d{1,2} de [a-zA-Z]{3} de \d{4})"
    fechas_encontradas = re.findall(fecha_regex, texto)
    print(f"🔍 Buscando fechas en el texto: {fechas_encontradas}")

    # Normalizamos las fechas encontradas
    fechas_normalizadas = [normalizar_fecha(fecha) for fecha in fechas_encontradas]
    
    print(f"🔍 Fechas normalizadas: {fechas_normalizadas}")
    
    # Filtramos las fechas None (si no pudieron ser normalizadas)
    fechas_normalizadas = [fecha for fecha in fechas_normalizadas if fecha is not None]
    
    return fechas_normalizadas