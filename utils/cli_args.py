import argparse


# Este script define una función para manejar argumentos de línea de comandos
def obtener_argumentos():
    parser = argparse.ArgumentParser(description="Analiza documentos y busca palabras clave.")
    parser.add_argument("--ruta", required=True, help="Ruta de la carpeta que contiene los documentos")
    parser.add_argument("--resumen", action="store_true", help="Incluir resumen contextual")
    parser.add_argument("--reprocesar", action="store_true", help="Limpiar archivos generados previamente")
    print(f"⚙️  Configuración CLI: {parser.parse_args()}")
    return parser.parse_args()