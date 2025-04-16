import unicodedata

# Normaliza un texto eliminando acentos y convirtiendo a minúsculas y eliminando caracteres no ASCII
def normalizar(texto):
    return unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode("ASCII").lower()