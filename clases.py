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
    
    def graficar_columna(self, columna):
        fig, axes = plt.subplots(1, 3, figsize=(15, 4))

        self.datos[columna].plot(ax=axes[0])
        axes[0].set_title("Plot de " + columna)
        axes[0].set_xlabel("Índice")
        axes[0].set_ylabel(columna)

        self.datos.boxplot(column=columna, ax=axes[1])
        axes[1].set_title("Boxplot de " + columna)
        axes[1].set_ylabel(columna)

        self.datos[columna].hist(ax=axes[2], bins=20)
        axes[2].set_title("Histograma de " + columna)
        axes[2].set_xlabel(columna)
        axes[2].set_ylabel("Frecuencia")

        plt.tight_layout()
        nombre_imagen = "graficos_siata_" + columna + ".png"
        plt.savefig(nombre_imagen, dpi=150)
        plt.show()
        print("Grafico guardado como:", nombre_imagen)
