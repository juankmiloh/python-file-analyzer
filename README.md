# 🧠 Analizador de Documentos con Palabras Clave y Resúmenes

Este script analiza documentos ubicados en una carpeta especificada, busca palabras clave relevantes y genera un informe detallado.  
También puede incluir **resúmenes contextuales** de los fragmentos donde se encuentran las palabras clave.

---

## ⚙️ Preparar el entorno de ejecución

**Crea y activa un entorno virtual de Python:**

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📆 Requisitos

### 🔧 Instalación de dependencias (OCR y extracción de texto)

#### Downgrade de `pip` (recomendado para evitar errores con `textract`)

```bash
pip install "pip<24.1"
```

#### Instalar `textract` y dependencias auxiliares

```bash
brew install antiword
pip install textract
```

#### Instalar OCR con `Tesseract` (si necesitas escaneo de texto en imágenes o PDF escaneados)

```bash
brew install tesseract                          # OCR engine
brew install tesseract-lang                     # Idioma español
export TESSDATA_PREFIX="/opt/homebrew/share/"   # Configuración del idioma
source ~/.zshrc                                 # Recargar la configuración del shell
pip install pytesseract pillow                  # Librerías para usar OCR en Python
```

#### Instalar `unar` para descomprimir archivos `.rar`

```bash
brew install unar
```

---

## 🚀 Ejecutar análisis

**Ejecuta el script con alguna de las siguientes opciones:**

```bash
# Sin resumen
python main.py --ruta "/ruta/a/tu/carpeta"

# Con resumen contextual
python main.py --ruta "/ruta/a/tu/carpeta" --resumen

# Reprocesar todos los archivos, incluso los ya procesados
python main.py --ruta "/ruta/a/tu/carpeta" --reprocesar

# Reprocesar todos los archivos, incluso los ya procesados agregando resumen contextual
python main.py --ruta "/ruta/a/tu/carpeta" --reprocesar --resumen
```

---

## 🧪 Ejemplos de Uso

```bash
python main.py --ruta "/Users/bitsamericas/Documents/ORF/doc_pdf" --resumen
python main.py --ruta "/Users/bitsamericas/Documents/ORF/doc_pdf" --reprocesar --resumen
```

También puedes analizar subcarpetas específicas:

```bash
python main.py --ruta "/Users/bitsamericas/Documents/ORF/ORF_DOC_OFICIAL/30-11-2023acruzfinal"
python main.py --ruta "/Users/bitsamericas/Documents/ORF/ORF_DOC_OFICIAL/DocumentosEnviadosOracle"
python main.py --ruta "/Users/bitsamericas/Documents/ORF/ORF_DOC_OFICIAL/ProyectoTDO"
python main.py --ruta "/Users/bitsamericas/Documents/ORF/ORF_DOC_OFICIAL/Correos Humberto Celis"
```

---

## 📊 Utilidades

### Contar archivos en una carpeta desde la terminal

```bash
find . -maxdepth 1 -type f | wc -l
```
