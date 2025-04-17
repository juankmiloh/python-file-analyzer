from utils.configuracion import args, rutaOutput, logger
from utils.comprimidos import descomprimir_recursivo
from procesamiento.analisis import analizar_documentos
from procesamiento.persistencia import cargar_resultados_previos
from procesamiento.salida import export_excel, export_txt, export_resumen_json


def main():
    logger.info(f"🚀 Iniciando análisis de documentos en {args.ruta}")

    # 1. Verificar y descomprimir archivos .zip y .rar
    descomprimir_recursivo(args.ruta)
    
    # 2. Procesar los documentos
    resultados_previos = cargar_resultados_previos()
    resultados_nuevos = analizar_documentos(args.ruta, args.resumen, args.reprocesar)
    resultados_totales = resultados_previos + resultados_nuevos

    # 3. Guardar los resultados
    export_txt(resultados_totales)
    export_excel(resultados_totales)
    if args.resumen:
        export_resumen_json(resultados_totales)

    logger.info("✅ Análisis completo")
    logger.info(f"📂 Archivos de salida generados en {rutaOutput}")
    logger.info("   - analizador.log")
    logger.info("   - informe_documentos.txt")
    logger.info("   - informe_documentos.xlsx")
    logger.info("   - procesados.txt")

if __name__ == "__main__":
    main()
