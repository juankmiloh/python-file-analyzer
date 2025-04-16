import os
from utils.cli_args import obtener_argumentos
from utils.limpieza import cleanup
from utils.logger import setup_logger
from utils.palabras_clave import cargar_palabras_clave


# -- Configuración de la aplicación -- Obtener argumentos de la línea de comandos
args = obtener_argumentos()

# -- Configuración de palabras clave -- Cargar las palabras clave una vez al inicio - Definir la ruta de palabras clave global
RUTA_PALABRAS_CLAVE = os.path.join("config", "palabras_clave.txt")
PALABRAS_CLAVE = cargar_palabras_clave(RUTA_PALABRAS_CLAVE)

# -- Configuración de rutas y carpetas --
OUT_DIR = "out_docs" # Carpeta de salida para los resultados
folder = os.path.basename(os.path.normpath(args.ruta)) # Nombre de la carpeta del análisis
rutaOutput = os.path.join(OUT_DIR, folder) # Crear ruta de carpeta de salida específica para cada análisis

# -- Configuración de limpieza -- Limpiar archivos generados previamente en la ruta de salida
if args.reprocesar:
    cleanup(args.reprocesar, rutaOutput)

# -- Crear la carpeta de salida si no existe --
if not os.path.exists(rutaOutput):
    os.makedirs(rutaOutput)

# -- Configuración del logger -- Configurar el logger para registrar la actividad de la aplicación
logger = setup_logger(rutaOutput)