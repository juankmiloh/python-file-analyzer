import os
import shutil
import patoolib
from utils.configuracion import logger


def descomprimir_recursivo(carpeta):
    for root, dirs, files in os.walk(carpeta):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith(".zip"):
                try:
                    destino = os.path.join(root, os.path.splitext(file)[0])
                    shutil.unpack_archive(file_path, destino)
                    logger.info(f"📦 Archivo .zip descomprimido: {file_path}")
                    descomprimir_recursivo(destino)  # Llamada recursiva
                except Exception as e:
                    logger.error(f"❌ Error descomprimiendo archivo .zip {file_path}: {e}")
            elif file.lower().endswith(".rar"):
                try:
                    destino = os.path.join(root, os.path.splitext(file)[0])
                    patoolib.extract_archive(file_path, outdir=destino)
                    logger.info(f"📦 Archivo .rar descomprimido: {file_path}")
                    descomprimir_recursivo(destino)  # Llamada recursiva
                except Exception as e:
                    logger.error(f"❌ Error descomprimiendo archivo .rar {file_path}: {e}")