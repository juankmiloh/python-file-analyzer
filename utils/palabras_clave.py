

def cargar_palabras_clave(ruta_archivo):
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            palabras = [linea.strip().lower() for linea in f if linea.strip()]
        return palabras
    except FileNotFoundError:
        raise SystemExit(f"❌ El archivo {ruta_archivo} no fue encontrado.")