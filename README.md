# Este script analiza documentos en una carpeta especificada, busca palabras clave y genera un informe.

# Se pueden incluir resúmenes contextuales de las palabras clave encontradas.

# Para ejecutar el script, usa el siguiente comando en la terminal:

# python main.py --ruta /ruta/a/tu/carpeta --resumen

# python main.py --ruta /ruta/a/tu/carpeta --reprocesar (Elimina todos los archivos del procesamiento; sino se envia el flag no se procesan los archivos ya procesados)

💻 Instalar unar para poder descomprimir archivos .rar

Para instalar `unar`, ejecuta el siguiente comando en la terminal:

```bash
brew install unar
```

Para instalar `tesseract` ejecuta los siguientes comandos en la terminal:

```bash
brew install tesseract // Sirve para usar el escaneo OCR
brew install tesseract-lang // Instalar los datos del idioma español
export TESSDATA_PREFIX="/opt/homebrew/share/" // Configurar la variable de entorno TESSDATA_PREFIX
source ~/.zshrc // Recarga tu archivo de configuración del shell
# En el entorno virtual
pip install pytesseract pillow // Ejecutar esto para poder instalar pytesseract y leer OCR
```

🚀 Cómo ejecutarlo

1. Crear un entorno virtual de Python:
   python3 -m venv venv
   source venv/bin/activate
   python -m pip install --upgrade pip
   pip install -r requirements.txt
2. python main.py --ruta "/ruta/a/tu/carpeta" --resumen

O si no quieres resumen:
python main.py --ruta "/ruta/a/tu/carpeta"

🧪 Ejemplo de uso

python main.py --ruta "/Users/bitsamericas/Documents/ORF/doc_pdf" --resumen

O sin resumen:
python main.py --ruta "/Users/bitsamericas/Documents/ORF/doc_pdf"
python main.py --ruta "/Users/bitsamericas/Documents/ORF/orf"
python main.py --ruta "/Users/bitsamericas/Documents/ORF/INCUMPLIMIENTO"
python main.py --ruta "/Users/bitsamericas/Documents/ORF/ACTA"

O si se quiere reprocesar todo:
python main.py --ruta "/Users/bitsamericas/Documents/ORF/INCUMPLIMIENTO" --reprocesar

# Downgrade de pip (recomendado para instalar textract)

brew install antiword
pip install "pip<24.1"
pip install textract

# Comando para contar cantidad de archivos de una carpeta estando dentro de ella

find . -maxdepth 1 -type f | wc -l

python main.py --ruta /Users/bitsamericas/Documents/ORF/ORF_DOC_OFICIAL/30-11-2023acruzfinal
python main.py --ruta /Users/bitsamericas/Documents/ORF/ORF_DOC_OFICIAL/DocumentosEnviadosOracle
python main.py --ruta /Users/bitsamericas/Documents/ORF/ORF_DOC_OFICIAL/ProyectoTDO
python main.py --ruta /Users/bitsamericas/Documents/ORF/ORF_DOC_OFICIAL/Correos Humberto Celis
python main.py --ruta /Users/bitsamericas/Documents/ORF/ORF_DOC_OFICIAL/Correos\ Humberto\ Celis/
