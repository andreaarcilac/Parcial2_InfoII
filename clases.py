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

    def operacion_apply(self, columna):
        nueva_columna = columna + "_por_2_apply"
        self.datos[nueva_columna] = self.datos[columna].apply(lambda x: x * 2)
        print("Se creó la columna:", nueva_columna)
        print(self.datos[[columna, nueva_columna]].head())

    def operacion_map(self, columna):
        promedio = self.datos[columna].mean()
        nueva_columna = columna + "_clasificacion_map"
        self.datos[nueva_columna] = self.datos[columna].map(lambda x: "alto" if x >= promedio else "bajo")
        print("Promedio de", columna, ":", promedio)
        print("Se creó la columna:", nueva_columna)
        print(self.datos[[columna, nueva_columna]].head())
    
    def operar_dos_columnas(self, columna1, columna2, operacion):
        if operacion == "1":
            nueva_columna = columna1 + "_mas_" + columna2
            self.datos[nueva_columna] = self.datos[columna1] + self.datos[columna2]
        elif operacion == "2":
            nueva_columna = columna1 + "_menos_" + columna2
            self.datos[nueva_columna] = self.datos[columna1] - self.datos[columna2]
        else:
            print("Operación no válida. Use '1' para suma o '2' para resta.")
            return

        print("Se creó la columna:", nueva_columna)
        print(self.datos[[columna1, columna2, nueva_columna]].head())