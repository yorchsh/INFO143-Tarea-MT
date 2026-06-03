Lenguaje de programación: Python

Estado inicial: string
Ej: estado_inicial = "q0"
Estado actual: string
estado_actual = estado_inicial
Estado final: string
estado_final = "q2"
Transiciones: Diccionarios usando los estados como claves, 
              para cada valor de cada clave se define un diccionario con claves tomadas de símbolos de la cinta,
              donde cada valor de cada clave tiene una tupla (estado_siguiente: string, simbolo_reemplazante: string (de largo 1, python no soporta carácteres), direccion_cabezal: entero),
              se define como el simbolo blanco el string nulo: "\0"
Palabra de entrada: string

Ejemplo de las estructuras de datos: 

LEFT: int = -1 # Mover el cabezal hacia la izquierda
RIGHT: int = 1 # Mover el cabezal hacia la derecha
estado_inicial: str = "q0"
estado_actual: str = estado_inicial
estado_final: str = "q2"
palabra_entrada: str = # Tomar entrada del usuario

transiciones: dict[str, dict[str: tuple[string, string, int]]] = {"q0": {"a": (q1, "b", RIGHT), "b": (q1, "a", RIGHT)}, 
                                                                  "q1": {"c": ("q1", "d", RIGHT}, "\0": ("q2", "\0", LEFT)}
                                                                  }
