import logging
import os


def setup_logger(rutaOutput):
    print(f"⚙️  Configurando logger para la ruta de salida: {rutaOutput}")
    # Ruta completa al archivo de log
    log_file = os.path.join(rutaOutput, "analizador.log")

    # Configuración del logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logging.getLogger("extract_msg").setLevel(logging.WARNING) # Ocultar mensajes de información de extract_msg