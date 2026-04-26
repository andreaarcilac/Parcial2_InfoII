from clases import(
    ArchivoSIATA,
    ArchivoEEG,
    AlmacenObjetos,
    pedir_entero,
    elegir_columna,
    elegir_columna_numerica,
    validar_archivo
)

Almacen = AlmacenObjetos

def submenu_siata(obj):
    while True:
        print("\n##########################################")
        print("#       MENÚ – ARCHIVO SIATA (CSV)       #")
        print("##########################################")
        print("#  1. Ver información básica             #")
        print("#  2. Graficar columna (plot/box/hist)   #")
        print("#  3. Operación con apply                #")
        print("#  4. Operación con map                  #")
        print("#  5. Sumar o restar dos columnas        #")
        print("#  6. Graficar remuestreo                #")
        print("#  0. Volver al menú principal           #")
        print("##########################################")


        Opcion = pedir_entero("Elija una opcion: ")
        
        if Opcion == 1:
            obj.informacion_basica()
            
        elif Opcion == 2:
            columna = elegir_columna_numerica(obj.datos)
            obj.graficar_columna(columna)
            
        elif Opcion == 3:
            columna = elegir_columna_numerica(obj.datos)
            obj.operacion_apply(columna)
        
        elif Opcion == 4:
            columna = elegir_columna_numerica(obj.datos)
            obj.opercion_map(columna)
            
        elif Opcion ==5:
            print("Eklija la primera columna: ")
            col1 = elegir_columna_numerica(obj.datos)
            print("Elija la segunda columna: ")
            col2 = elegir_columna_numerica(obj.datos)
            print("1. Suma")
            print("2. Resta")
            op = input("Operacion (1 o 2)").strip()
            obj.operar_dos_columnas(col1, col2, op)
        elif Opcion ==6:
            columna = elegir_columna_numerica(obj.datos)
            obj.graficar_remuestreo(columna)
        
        elif Opcion == 0:
            break
        
def submenu_eeg(obj):
    obj.mostrar_llaves()
    llave = input("Escriba la llave de la matriz: ").strip()
    obj.seleccionar_matriz(llave)

    while True:
        print("\n##########################################")
        print("#        MENÚ – ARCHIVO EEG (MAT)        #")
        print("##########################################")
        print("#  1. Sumar 3 canales y graficar         #")
        print("#  2. Promedio y desviación std (3D)     #")
        print("#  0. Volver al menú principal           #")
        print("##########################################")

        opcion = pedir_entero("Opción: ", 0, 2)

        if opcion == 1:
            mat2d = obj.obtener_matriz_2d()
            if mat2d is None:
                continue

            n_canales = mat2d.shape[0]
            n_puntos = mat2d.shape[1]
            print("Canales disponibles: 0 a", n_canales - 1)
            print("Puntos disponibles: 0 a", n_puntos - 1)

            c1 = pedir_entero("Canal 1: ", 0, n_canales - 1)
            c2 = pedir_entero("Canal 2: ", 0, n_canales - 1)
            c3 = pedir_entero("Canal 3: ", 0, n_canales - 1)
            p_min = pedir_entero("Punto mínimo: ", 0, n_puntos - 1)
            p_max = pedir_entero("Punto máximo: ", p_min + 1, n_puntos)
            obj.sumar_tres_canales(c1, c2, c3, p_min, p_max)

        elif opcion == 2:
            if obj.matriz is None:
                print("Primero seleccione una matriz.")
                continue
            if obj.matriz.ndim != 3:
                print("La matriz no es 3D.")
                continue
            eje = pedir_entero("Eje (0, 1 o 2): ", 0, 2)
            obj.promedio_y_desviacion_3d(eje)

        elif opcion == 0:
            break


def menu_principal():
    print("\n##################################################")
    print("#    SISTEMA DE EXPLORACIÓN NEUROAMBIENTAL      #")
    print("#    Universidad de Antioquia – Bioingeniería   #")
    print("##################################################")

    while True:
        print("\n##########################################")
        print("#            MENÚ PRINCIPAL              #")
        print("##########################################")
        print("#  1. Cargar archivo SIATA (CSV)         #")
        print("#  2. Cargar archivo EEG   (MAT)         #")
        print("#  3. Ver objetos guardados              #")
        print("#  4. Usar un objeto guardado            #")
        print("#  0. Salir                              #")
        print("##########################################")

        opcion = pedir_entero("Opción: ", 0, 4)

        if opcion == 1:
            ruta = input("Ruta del archivo CSV: ").strip()
            if not validar_archivo(ruta, ".csv"):
                continue
            try:
                obj = ArchivoSIATA(ruta)
                nombre = input("Nombre para guardar el objeto (Enter para no guardar): ").strip()
                if nombre != "":
                    Almacen.agregar_objeto(nombre, obj)
                submenu_siata(obj)
            except Exception as e:
                print("Error al cargar el archivo:", e)

        elif opcion == 2:
            ruta = input("Ruta del archivo MAT: ").strip()
            if not validar_archivo(ruta, ".mat"):
                continue
            try:
                obj = ArchivoEEG(ruta)
                nombre = input("Nombre para guardar el objeto (Enter para no guardar): ").strip()
                if nombre != "":
                    Almacen.agregar_objeto(nombre, obj)
                submenu_eeg(obj)
            except Exception as e:
                print("Error al cargar el archivo:", e)

        elif opcion == 3:
            Almacen.listar_objetos()

        elif opcion == 4:
            Almacen.listar_objetos()
            nombre = input("Nombre del objeto a usar: ").strip()
            obj = Almacen.buscar_objeto(nombre)
            if obj is None:
                continue
            if isinstance(obj, ArchivoSIATA):
                submenu_siata(obj)
            elif isinstance(obj, ArchivoEEG):
                submenu_eeg(obj)

        elif opcion == 0:
            print("Hasta luego.")
            break


if __name__ == "__main__":
    menu_principal()