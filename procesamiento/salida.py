import os
import openpyxl
import json
from utils.configuracion import PALABRAS_CLAVE, rutaOutput


def export_txt(resultados):
    txt_path = os.path.join(rutaOutput, "informe_documentos.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        for r in resultados:
            ruta_completa = os.path.abspath(r["ruta"])
            ruta_directorio = os.path.dirname(ruta_completa)
            nombre_archivo = r["nombre"]
            f.write(f"Ruta: {ruta_directorio}\n")
            f.write(f"Archivo: {nombre_archivo} ({r['tipo']})\n")
            f.write(f"Total coincidencias: {r['coincidencias']}\n")
            for palabra, cantidad in r['detalle'].items():
                f.write(f"   {palabra}: {cantidad}\n")

def export_excel(resultados):
    wb = openpyxl.Workbook()
    ws = wb.active

    encabezados = ["Ruta", "Nombre", "Tipo", "Total coincidencias"] + PALABRAS_CLAVE

    ws.append(encabezados)

    for r in resultados:
        ruta_completa = os.path.abspath(r["ruta"])
        ruta_directorio = os.path.dirname(ruta_completa)
        nombre_archivo = r["nombre"]

        fila = [ruta_directorio, nombre_archivo, r["tipo"], r["coincidencias"]]
        fila += [r["detalle"].get(p, 0) for p in PALABRAS_CLAVE]

        ws.append(fila)

    excel_path = os.path.join(rutaOutput, "informe_documentos.xlsx")
    wb.save(excel_path)

def export_resumen_json(resultados):
    resumen = [
        {"archivo": os.path.join(os.path.dirname(os.path.abspath(r["ruta"])), r["nombre"]), "resumen": r["resumen"]}
        for r in resultados if "resumen" in r
    ]
    json_path = os.path.join(rutaOutput, "resumen.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(resumen, f, ensure_ascii=False, indent=2)
