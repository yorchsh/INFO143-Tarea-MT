import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Constantes
IZQUIERDA = -1
DERECHA = 1
NUMERO_MAXIMO_TRANSICIONES = 2**16

# Errores Maquina de turing
ESTADO_INICIAL_VACIO = 2
ESTADO_FINAL_VACIO = 3
TRANSICIONES_INVALIDAS = 4
PALABRA_ENTRADA_VACIA = 5
MAQUINA_TURING_DEMASIADOS_PASOS = 6

def parsear_transiciones(transiciones_str: str) -> dict[str, dict[str, tuple[str, str, int]]] | None:
    try:
        print("transiciones_str:")
        print(transiciones_str)
        funcion_transicion: dict[str, dict[str, tuple[str, str, int]]] = {}
        # Elimina los espacios en blanco
        transiciones_str: str = transiciones_str.replace(' ', '')
        # Crea una lista de transiciones en str
        transiciones_list: list[str] = transiciones_str.split('\n')
        ## Hay que revisar si los saltos de linea en balnco se consideran ""
        
        for transicion in transiciones_list:
            # Ignorar saltos de linea
            if transicion != "":
                temp: list[str] = transicion.split('=', 1)
                entradas: list[str] = temp[0].split(',')

                if len(entradas) != 2:
                    print("entradas:", entradas)
                    return None

                if entradas[0][0:2] != 'd(':
                    print(1)
                    return None

                estado_entrada: str = entradas[0][2:]

                if len(entradas[1]) != 2:
                    print(2)
                    return None
                
                if entradas[1][1] != ')':
                    print(3)
                    return None

                simbolo_entrada: str = entradas[1][0]
                
                salidas: list[str] = temp[1].split(',')


                if len(salidas) != 3:
                    print(4)
                    return None

                if salidas[0][0] != '(':
                    print(5)
                    return None

                estado_salida: str = salidas[0][1:]
                simbolo_salida: str = salidas[1]
                direccion_salida = 0

                if salidas[2][1] != ')':
                    print(6)
                    return None

                if salidas[2][0] == 'I':
                    direccion_salida = -1
                elif salidas[2][0] == 'D':
                    direccion_salida = 1
                else:
                    print(7)
                    return None

                if estado_entrada in funcion_transicion:
                    if simbolo_entrada in funcion_transicion[estado_entrada]:
                        print(8)
                        return None
                    funcion_transicion[estado_entrada][simbolo_entrada] = (estado_salida, simbolo_salida, direccion_salida)

                else:
                    funcion_transicion[estado_entrada] = {simbolo_entrada: (estado_salida, simbolo_salida, direccion_salida)}
        
        print("funcion_transicion:")
        print(funcion_transicion)
        return funcion_transicion

    except Exception as e:
        print(e)
        return None


def construir_cinta(palabra_entrada: str) -> list[str]:
    '''Construye una cinta con los caracteres con la palabra de entrada'''
    cinta = []
    for x in palabra_entrada:
        cinta.append(x)
    # Si la cinta esta vacia agregar Blanco
    if len(cinta) == 0:
        cinta.append('B')
    return cinta


def maquina_turing(estado_inicial: str, estado_final: str, transiciones: dict[str, dict[str: tuple[str, str, int]]], palabra_entrada: str) -> bool | int:
    estado_actual: str = estado_inicial
    posicion = 0

    if estado_inicial == "":
        return ESTADO_INICIAL_VACIO
    
    if estado_final == "":
        return ESTADO_FINAL_VACIO

    if transiciones is None:
        return TRANSICIONES_INVALIDAS


    cinta = construir_cinta(palabra_entrada)

    numero_transiciones = 0
    print("Maquina de turing (traza):")
    print("estado_actual | posicion | cinta[posicion]")
    while estado_actual != estado_final and estado_actual in transiciones and cinta[posicion] in transiciones[estado_actual]:
        print(estado_actual, posicion, cinta[posicion])
        estado_actual, cinta[posicion], direccion = transiciones[estado_actual][cinta[posicion]]
        posicion += direccion
        
        if posicion < 0:
            return False

        if posicion >= len(cinta):
            # Agregar blancos a la cinta para simular ser semininfinita
            cinta.append('B')

        numero_transiciones += 1 
        if numero_transiciones >= NUMERO_MAXIMO_TRANSICIONES:
            return MAQUINA_TURING_DEMASIADOS_PASOS


    print("While finalizado:")
    print(estado_actual, posicion, cinta[posicion])

    if estado_actual == estado_final:
        # Acepta la palabra
        return True
    else:
        # Rechaza la palabra
        return False


def window():
    # Crea la ventana
    root = tk.Tk()
    
    # Crea un cuadro dentro de la ventana
    frame = ttk.Frame(root, padding=10)
    frame.grid(column=0, row=0)

    # Entrada para el estado inicial
    ttk.Label(frame, text="Estado inicial (ej: q0)", justify="left").grid(row=1)
    estado_inicial = ""
    entry_estado_inicial = ttk.Entry(frame, width=32)
    entry_estado_inicial.grid(row=2)

    # Entrada para el estado final
    ttk.Label(frame, text="Estado final (ej: q2)").grid(row=3)
    entry_estado_final = ttk.Entry(frame, width=32)
    entry_estado_final.grid(row=4)

    # Entrada para las transiciones
    ttk.Label(frame, text="Transiciones separadas por saltos de linea", justify="left").grid(row=5)
    ttk.Label(frame, text="Ejemplo:").grid(row=6)
    ttk.Label(frame, text="d(q0, a) = (q1, a, D)",).grid(row=7)
    ttk.Label(frame, text="d(q1, b) = (q1, b, D)",).grid(row=8)
    ttk.Label(frame, text="d(q1, B) = (q2, B, I)").grid(row=9)
    ttk.Label(frame, text="I: Mover el cabezal a la izquierda, D: Mover el cabezal a la derecha").grid(row=10)
    ttk.Label(frame, text="B: Blanco").grid(row=11)
    text_transiciones = tk.Text(frame)
    text_transiciones.grid(row=12)
    
    # Palabra de entrada
    ttk.Label(frame, text="Palabra de entrada (ej: abbb)").grid(row=13)
    entry_palabra_entrada = ttk.Entry(frame, width=32)
    entry_palabra_entrada.grid(row=14)


    def procesar_palabra():
        estado_inicial: str = entry_estado_inicial.get().replace(' ', '')
        estado_final: str = entry_estado_final.get().replace(' ', '')
        transiciones: str = parsear_transiciones(text_transiciones.get("1.0", "end"))
        palabra_entrada: str = entry_palabra_entrada.get().strip()

        resultado = maquina_turing(estado_inicial, estado_final, transiciones, palabra_entrada)

        if resultado == ESTADO_INICIAL_VACIO:
            messagebox.showerror(title="El estado inicial no puede estar vacio.", \
                                message="El estado inicial no puede estar vacio.")
        elif resultado == ESTADO_FINAL_VACIO:
            messagebox.showerror(title="El estado final no puede estar vacio.", \
                                message="El estado final no puede estar vacio.")
        elif resultado == TRANSICIONES_INVALIDAS:
            messagebox.showerror(title="Las transiciones no fueron definidas correctamente.", \
                                message="Las transiciones no fueron definidas correctamente.")
        elif resultado == PALABRA_ENTRADA_VACIA:
            messagebox.showerror(title="La palabra de entrada esta vacia.",
                                message="La palabra de entrada esta vacia.")
        elif resultado == MAQUINA_TURING_DEMASIADOS_PASOS:
            messagebox.showerror(title="La maquina de Turing realizo mas de 2^16=65536 cambios de estado...",
                                message="La maquina de turing realizo mas de 2^16=65536 cambios de estado. \n\
                                        Se detuvo la ejecución.")
        elif resultado == True:
            messagebox.showinfo(title="Palabra aceptada.",
                                message="Palabra aceptada.")
        elif resultado == False:
            messagebox.showerror("Palabra rechaza.",
                                message="Palabra rechazada.")
            
    
    button = ttk.Button(frame, text='Procesar Palabra', command=procesar_palabra).grid(row=15)

    root.mainloop()


def main():
    window()

if __name__ == "__main__":
    main()
