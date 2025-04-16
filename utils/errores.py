class ExtractionError(Exception):
    def __init__(self, mensaje, archivo=None):
        super().__init__(mensaje)
        self.archivo = archivo