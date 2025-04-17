from datetime import datetime
import unicodedata
import locale
import re
from utils.configuracion import logger


# Intentamos establecer el locale a español
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except locale.Error:
    try:
        print("No se pudo establecer el locale a español. Intentando con 'es_ES'.")
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
def extraer_fechas(texto, path):
    # Expresión regular para detectar fechas en diferentes formatos
    fecha_regex = r"""
        \d{1,2}[-/]\d{1,2}[-/]\d{2,4}                               |  # 15/04/2025 o 15-04-2025
        \d{4}[-/]\d{1,2}[-/]\d{1,2}                                 |  # 2025-04-15
        \d{1,2} \s+ de \s+ [a-zA-ZáéíóúÁÉÍÓÚñÑ]+ \s+ de \s+ \d{4}   |  # 15 de abril de 2025
        \d{1,2} \s+ de \s+ [a-zA-ZáéíóúÁÉÍÓÚñÑ]{3} \s+ de \s+ \d{4} |  # 15 de abr de 2025
        [A-Z][a-z]+ \s+ \d{1,2}, \s+ \d{4}                          |  # May 7, 2021 o Aug 3, 2022
        \d{1,2} \s+ [a-zA-Z]{3} \s+ \d{4}                              # 18 mar 2025
    """

    fechas_encontradas = re.findall(fecha_regex, texto, re.VERBOSE)
    logger.info(f"🔍 [Fechas encontradas][Archivo]: {path} | {fechas_encontradas}")

    # Normalizamos las fechas encontradas
    fechas_normalizadas = [normalizar_fecha(fecha) for fecha in fechas_encontradas]
    
    # Filtramos las fechas None (si no pudieron ser normalizadas)
    fechas_normalizadas = [fecha for fecha in fechas_normalizadas if fecha is not None]
    
    return fechas_normalizadas