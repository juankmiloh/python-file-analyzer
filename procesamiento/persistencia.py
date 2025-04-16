import os
import openpyxl
from utils.configuracion import PALABRAS_CLAVE, rutaOutput, logger


def cargar_resultados_previos():
    resultados = []
    excel_path = os.path.join(rutaOutput, "informe_documentos.xlsx")
    if not os.path.exists(excel_path):
        logger.info(f"⚙️  No se encontró el archivo informe_documentos.xlsx. Se generará uno nuevo.")
        return resultados
    
    print("Cargando resultados previos de informe_documentos.xlsx...")
    wb = openpyxl.load_workbook(excel_path)
    ws = wb.active

    for row in ws.iter_rows(min_row=2, values_only=True):
        ruta = row[0]
        nombre = row[1]
        tipo = row[2]
        coincidencias = row[3]
        detalle = {PALABRAS_CLAVE[i]: row[4 + i] for i in range(len(PALABRAS_CLAVE))}
        resumen = {}
        if len(row) > 4 + len(PALABRAS_CLAVE) and row[4 + len(PALABRAS_CLAVE)]:
            resumen["resumen"] = [row[4 + len(PALABRAS_CLAVE)]]

        resultados.append({
            "ruta": ruta,
            "nombre": nombre,
            "tipo": tipo,
            "coincidencias": coincidencias,
            "detalle": detalle,
            "resumen": resumen
        })

    return resultados

def cargar_archivos_procesados(rutaOutput):
    procesados = set()
    procesados_path = os.path.join(rutaOutput, "procesados.txt")
    if os.path.exists(procesados_path):
        with open(procesados_path, "r", encoding="utf-8") as f:
            procesados = set(line.strip() for line in f)
    return procesados

def guardar_archivos_procesados(paths, rutaOutput):
    procesados_path = os.path.join(rutaOutput, "procesados.txt")
    with open(procesados_path, "a", encoding="utf-8") as f:
        for path in paths:
            f.write(f"{path}\n")