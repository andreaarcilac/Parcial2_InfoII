import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.io import loadmat, whosmat

class ArchivoSIATA:
    def __init__(self, ruta):
        self.ruta = ruta
        self.datos = pd.read_csv(ruta)

    def informacion_basica(self):
        print("\n===== INFORMACIÓN BÁSICA DEL DATAFRAME =====\n")
        print(f"\nTamaño (total de elementos): {self.datos.size}")
        print(f"\nDimensiones: {self.datos.ndim}")
        print(f"\nValores (primeras filas): {self.datos.values[:5].tolist()}")
        print("\n===== DESCRIPCIÓN ESTADÍSTICA =====")
        print(self.datos.describe())
        print("\n===== INFO DEL DATAFRAME =====")
        self.datos.info()
