import os
import openpyxl
from utils.configuracion import PALABRAS_CLAVE, rutaOutput


def export_txt(resultados, incluir_resumen):
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
            if incluir_resumen:
                f.write("Resumen contextual:\n")
                for palabra, frases in r.get("resumen", {}).items():
                    f.write(f"  - {palabra}:\n")
                    for frase in frases:
                        f.write(f"      * {frase.strip()}\n")
            f.write("\n")

def export_excel(resultados, incluir_resumen):
    wb = openpyxl.Workbook()
    ws = wb.active

    encabezados = ["Ruta", "Nombre", "Tipo", "Total coincidencias"] + PALABRAS_CLAVE
    if incluir_resumen:
        encabezados.append("Resumen")
    ws.append(encabezados)

    for r in resultados:
        ruta_completa = os.path.abspath(r["ruta"])
        ruta_directorio = os.path.dirname(ruta_completa)
        nombre_archivo = r["nombre"]

        fila = [ruta_directorio, nombre_archivo, r["tipo"], r["coincidencias"]]
        fila += [r["detalle"].get(p, 0) for p in PALABRAS_CLAVE]

        if incluir_resumen:
            resumen_concat = "\n".join(
                f"{palabra}: " + " | ".join(frases) for palabra, frases in r.get("resumen", {}).items()
            )
            fila.append(resumen_concat)

        ws.append(fila)

    excel_path = os.path.join(rutaOutput, "informe_documentos.xlsx")
    wb.save(excel_path)