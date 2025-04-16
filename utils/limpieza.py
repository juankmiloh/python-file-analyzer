import os
import shutil


def cleanup(reprocesar, rutaOutput):
    if reprocesar:
        if os.path.exists(rutaOutput):
            print(f"🗑️  Limpiando archivos generados previamente...")
            for root, dirs, files in os.walk(rutaOutput):
                for file in files:
                    os.remove(os.path.join(root, file))
                for dir in dirs:
                    shutil.rmtree(os.path.join(root, dir))
            print(f"🗑️  Directorio '{rutaOutput}' limpiado correctamente.")
        else:
            print(f"⚙️  El directorio '{rutaOutput}' no existe.")