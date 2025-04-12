# Este script analiza documentos en una carpeta especificada, busca palabras clave y genera un informe.

# Se pueden incluir resúmenes contextuales de las palabras clave encontradas.

# Para ejecutar el script, usa el siguiente comando en la terminal:

# python analizador_documentos.py --ruta /ruta/a/tu/carpeta --resumen

🚀 Cómo ejecutarlo

1. Crear un entorno virtual de Python:
   python3 -m venv venv
   source venv/bin/activate
   python -m pip install --upgrade pip
   pip install -r requirements.txt
2. python analizador_documentos.py --ruta "/ruta/a/tu/carpeta" --resumen

O si no quieres resumen:
python analizador_documentos.py --ruta "/ruta/a/tu/carpeta"

🧪 Ejemplo de uso

python analizador_documentos.py --ruta "/Users/bitsamericas/Downloads/doc_pdf" --resumen

O sin resumen:
python analizador_documentos.py --ruta "/Users/bitsamericas/Downloads/doc_pdf"
python analizador_documentos.py --ruta "/Users/bitsamericas/Downloads/orf"
python analizador_documentos.py --ruta "/Users/bitsamericas/Downloads/INCUMPLIMIENTO"
python analizador_documentos.py --ruta "/Users/bitsamericas/Downloads/ACTA"

O si se quiere reprocesar todo:
python analizador_documentos.py --ruta "/Users/bitsamericas/Downloads/INCUMPLIMIENTO" --reprocesar

# Downgrade de pip (recomendado para instalar textract)

brew install antiword
pip install "pip<24.1"
pip install textract

# Comando para contar cantidad de archivos de una carpeta estando dentro de ella

find . -maxdepth 1 -type f | wc -l

python analizador_documentos.py --ruta /Users/bitsamericas/Downloads/ORF_DOC_OFICIAL/30-11-2023acruzfinal
