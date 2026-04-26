import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.io import loadmat, whosmat
import os

def pedir_entero(texto, minimo=None, maximo=None):
    while True:
        try:
            numero = int(input(texto))
            if minimo is not None and numero < minimo:
                print("El numero debe ser mayor o igual a", minimo)
            elif maximo is not None and numero > maximo:
                print("El numero debe ser menor o igual a", maximo)
            else:
                return numero
        except ValueError:
            print("Error: debe escribir un numero entero.")


def validar_archivo(ruta, extension):
    if not os.path.exists(ruta):
        print("No se encontro el archivo.")
        return False
    if not ruta.lower().endswith(extension):
        print("El archivo debe tener extension", extension)
        return False
    return True


def elegir_columna(dataframe):
    print("\nColumnas disponibles:")
    for columna in dataframe.columns:
        print("-", columna)

    while True:
        columna = input("Escriba el nombre de la columna: ").strip()
        if columna in dataframe.columns:
            return columna
        else:
            print("Esa columna no existe. Intente otra vez.")


def elegir_columna_numerica(dataframe):
    while True:
        columna = elegir_columna(dataframe)
        if pd.api.types.is_numeric_dtype(dataframe[columna]):
            return columna
        else:
            print("La columna elegida no es numerica.")

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
    
    def graficar_remuestreo(self, columna):
        if not isinstance(self.datos.index, pd.DatetimeIndex):
            columna_fecha = self.datos.columns[0]
            self.datos[columna_fecha] = pd.to_datetime(self.datos[columna_fecha])
            self.datos = self.datos.set_index(columna_fecha)
            self.datos = self.datos.sort_index()
        print("La columna de fecha quedó como índice:")
        print(self.datos.index[:5])
    
        diario = self.datos[columna].resample("D").mean()
        mensual = self.datos[columna].resample("M").mean()
        trimestral = self.datos[columna].resample("Q").mean()

        fig, axes = plt.subplots(3, 1, figsize=(10, 9))

        diario.plot(ax=axes[0])
        axes[0].set_title("Remuestreo diario de " + columna)
        axes[0].set_xlabel("Fecha")
        axes[0].set_ylabel(columna)

        mensual.plot(ax=axes[1])
        axes[1].set_title("Remuestreo mensual de " + columna)
        axes[1].set_xlabel("Fecha")
        axes[1].set_ylabel(columna)

        trimestral.plot(ax=axes[2])
        axes[2].set_title("Remuestreo trimestral de " + columna)
        axes[2].set_xlabel("Fecha")
        axes[2].set_ylabel(columna)

        plt.tight_layout()
        nombre_imagen = "remuestreo_siata_" + columna + ".png"
        plt.savefig(nombre_imagen, dpi=150)
        plt.show()
        print("Grafico guardado como:", nombre_imagen)


class ArchivoEEG:
    def __init__(self, ruta):
        self.ruta = ruta
        self.frecuencia_muestreo = 1000  # Hz, es decir, 1000 muestras por segundo
        self.archivo = loadmat(ruta)
        self.matriz = None
        self.llave_matriz = None

    def mostrar_llaves(self):
        print("\n========== LLAVES DEL ARCHIVO MAT ==========")
        llaves = whosmat(self.ruta)
        for item in llaves:
            print(item[0])
    
    def seleccionar_matriz(self, llave):
        if llave in self.archivo:
            self.matriz = np.array(self.archivo[llave])
            self.llave_matriz = llave
            print("Matriz seleccionada:", llave)
            print("Dimensiones:", self.matriz.shape)
        else:
            print("Esa llave no esta en el archivo.")

    def obtener_matriz_2d(self):
        if self.matriz is None:
            print("Primero seleccione una matriz.")
            return None

        elif self.matriz.ndim == 2:
            return self.matriz

        elif self.matriz.ndim == 3:
            print("La matriz es 3D. Para esta parte se usa matriz[:, :, 0].")
            return self.matriz[:, :, 0]

        else:
            print("La matriz no es 2D ni 3D.")
            return None
    
    def sumar_tres_canales(self, canal1, canal2, canal3, punto_minimo, punto_maximo):
        matriz_2d = self.obtener_matriz_2d()
        if matriz_2d is None:
            return

        canales = [canal1, canal2, canal3]
        numero_canales = matriz_2d.shape[0]
        numero_puntos = matriz_2d.shape[1]

        for canal in canales:
            if canal < 0 or canal >= numero_canales:
                print("Canal fuera del rango. Los canales van de 0 a", numero_canales - 1)
                return

        if punto_minimo < 0 or punto_maximo > numero_puntos or punto_minimo >= punto_maximo:
            print("Puntos no validos. Los puntos van de 0 a", numero_puntos)
            return

        tiempo = np.arange(punto_minimo, punto_maximo) / self.frecuencia_muestreo

        senal1 = matriz_2d[canal1, punto_minimo:punto_maximo]
        senal2 = matriz_2d[canal2, punto_minimo:punto_maximo]
        senal3 = matriz_2d[canal3, punto_minimo:punto_maximo]
        suma = senal1 + senal2 + senal3

        fig, axes = plt.subplots(2, 1, figsize=(10, 7))

        axes[0].plot(tiempo, senal1, label="Canal " + str(canal1))
        axes[0].plot(tiempo, senal2, label="Canal " + str(canal2))
        axes[0].plot(tiempo, senal3, label="Canal " + str(canal3))
        axes[0].set_title("Tres canales EEG elegidos")
        axes[0].set_xlabel("Tiempo (s)")
        axes[0].set_ylabel("Amplitud (microvoltios)")
        axes[0].legend()

        axes[1].plot(tiempo, suma, label="Suma")
        axes[1].set_title("Suma de los tres canales")
        axes[1].set_xlabel("Tiempo (s)")
        axes[1].set_ylabel("Amplitud (microvoltios)")
        axes[1].legend()

        plt.tight_layout()
        nombre_imagen = "suma_canales_eeg.png"
        plt.savefig(nombre_imagen, dpi=150)
        plt.show()
        print("Grafico guardado como:", nombre_imagen)

    def promedio_y_desviacion_3d(self, eje):
        if self.matriz is None:
            print("Primero seleccione una matriz.")
            return

        if self.matriz.ndim != 3:
            print("Esta opción necesita la matriz original en 3D.")
            return

        if eje < 0 or eje > 2:
            print("El eje debe ser 0, 1 o 2.")
            return

        promedio = np.mean(self.matriz, axis=eje)
        desviacion = np.std(self.matriz, axis=eje)

        promedio_1d = promedio.flatten()
        desviacion_1d = desviacion.flatten()

        limite = min(200, len(promedio_1d))
        x = np.arange(limite)

        fig, axes = plt.subplots(1, 2, figsize=(13, 5))

        axes[0].stem(x, promedio_1d[:limite])
        axes[0].set_title("Promedio en el eje " + str(eje))
        axes[0].set_xlabel("Punto")
        axes[0].set_ylabel("Promedio (microvoltios)")

        axes[1].stem(x, desviacion_1d[:limite])
        axes[1].set_title("Desviación estándar en el eje " + str(eje))
        axes[1].set_xlabel("Punto")
        axes[1].set_ylabel("Desviación estándar (microvoltios)")

        plt.tight_layout()
        nombre_imagen = "promedio_desviacion_eeg.png"
        plt.savefig(nombre_imagen, dpi=150)
        plt.show()
        print("Gráfico guardado como:", nombre_imagen)


class AlmacenObjetos:
    def __init__(self):
        self.objetos = {}

    def agregar_objeto(self, nombre, objeto):
        self.objetos[nombre] = objeto
        print("Objeto agregado con nombre:", nombre)

    def buscar_objeto(self, nombre):
        if nombre in self.objetos:
            return self.objetos[nombre]
        else:
            print("No se encontró un objeto con ese nombre.")
            return None

    def listar_objetos(self):
        if len(self.objetos) == 0:
            print("No hay objetos guardados.")
        else:
            print("\nObjetos guardados:")
            for nombre in self.objetos:
                print("-", nombre, "->", type(self.objetos[nombre]).__name__)




