import tkinter as tk
from tkinter import messagebox
import nltk
from nltk import CFG, ChartParser

# Variable  para elegir el tipo de árbol
tipo_arbol = "normal"

# Función para analizar la expresión ingresada
def analizar_expresion():
    # Obtener la opción de derivación
    opcion = derivacion_var.get()

    # Definir la gramática segun si el usuario escogio derivacion por derecha o por izquierda.
    if opcion == "Izquierda":
        gramatica = CFG.fromstring("""
            E -> E '+' T | E '-' T | T
            T -> T '*' F | T '/' F | F
            F -> '(' E ')' | 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
        """)
    elif opcion == "Derecha":
        gramatica = CFG.fromstring("""
            E -> T '+' E | T '-' E | T
            T -> F '*' T | F '/' T | F
            F -> '(' E ')' | 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
        """)
    else:
        messagebox.showerror("Error", "Opción no válida. Se usará derivación por izquierda.")
        gramatica = CFG.fromstring("""
            E -> E '+' T | E '-' T | T
            T -> T '*' F | T '/' F | F
            F -> '(' E ')' | 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
        """)

    entrada_usuario = entrada_text.get()
    expresion_objetivo = entrada_usuario.split()

    # Crear el parser
    parser = ChartParser(gramatica)

    try:
        # Generar árboles de derivación normal y el ats
        for tree in parser.parse(expresion_objetivo):
            resultado_text.delete(1.0, tk.END)

            if tipo_arbol == "normal":
                resultado_text.insert(tk.END, "Árbol de derivación:\n")
                tree.pretty_print()
                tree.draw()
            elif tipo_arbol == "ATS":
                resultado_text.insert(tk.END, "\nÁrbol ATS simplificado:\n")
                ats_arbol = arbol_ats_crear(tree)
                ats_arbol.pretty_print()
                ats_arbol.draw()
    except ValueError:
        messagebox.showerror("Error ", "La expresión no es válida vuelva a ingresar una expresio diferente.")

# Función para construir el árbol ats
def arbol_ats_crear(tree):
    ats_arbol = tree.copy()
    for subtree in ats_arbol.subtrees():
        if subtree.label() not in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            subtree.set_label('')
    return ats_arbol

# Función para derivación paso a paso
def derivacion_paso_a_paso():
    
    gramatica = CFG.fromstring("""
        E -> E '+' T | E '-' T | T
        T -> T '*' F | T '/' F | F
        F -> '(' E ')' | 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
    """)

    entrada_usuario = entrada_text.get()
    expresion_objetivo = entrada_usuario.split()

    parser = ChartParser(gramatica)

    try:
        arboles = list(parser.parse(expresion_objetivo))
        if not arboles:
            raise ValueError("La expresión no se puede analizar, vuelva a ingresar una diferente.")

        resultado_text.delete(1.0, tk.END)
        resultado_text.insert(tk.END, "Derivación paso a paso:\n\n")

        pasos = []
        derivar_paso_a_paso(arboles[0], pasos)

        for paso in pasos:
            resultado_text.insert(tk.END, paso + "\n")

        # Mostrar la expresión final 
        resultado_text.insert(tk.END, f"\nExpresión derivada: {' '.join(expresion_objetivo)}")

    except ValueError:
        messagebox.showerror("Error ", "segun la gramatica hay un error vuelva a intentarlo.")

# Función para construir la derivación paso a paso
def derivar_paso_a_paso(tree, pasos):
    def derivar(nodo):
        if isinstance(nodo, nltk.Tree):
            if nodo.height() == 2:
                return " ".join(nodo.leaves())
            else:
                regla = f"{nodo.label()} -> {' '.join([sub.label() if isinstance(sub, nltk.Tree) else sub for sub in nodo])}"
                pasos.append(regla)
                return " ".join([derivar(sub) if isinstance(sub, nltk.Tree) else sub for sub in nodo])
        else:
            return nodo

    derivar(tree)

# Función para cambiar el tipo de árbol
def elegir_arbol_normal():
    global tipo_arbol
    tipo_arbol = "normal"

def elegir_arbol_ats():
    global tipo_arbol
    tipo_arbol = "ATS"

# Interfaz gráfica
ventana = tk.Tk()
ventana.title("Analizador de Expresiones")

entrada_label = tk.Label(ventana, text="Introduce la funcion que quieras derivar:")
entrada_label.pack(pady=10)

entrada_text = tk.Entry(ventana, width=50)
entrada_text.pack(pady=5)

derivacion_var = tk.StringVar(value="Izquierda")

derivacion_label = tk.Label(ventana, text="Elige el tipo de derivación qui quiere:")
derivacion_label.pack(pady=10)

derivacion_izquierda_radio = tk.Radiobutton(ventana, text="Izquierda", variable=derivacion_var, value="Izquierda")
derivacion_izquierda_radio.pack()

derivacion_derecha_radio = tk.Radiobutton(ventana, text="Derecha", variable=derivacion_var, value="Derecha")
derivacion_derecha_radio.pack()

arbol_normal_boton = tk.Button(ventana, text="Árbol normal", command=elegir_arbol_normal)
arbol_normal_boton.pack(pady=5)

arbol_ats_boton = tk.Button(ventana, text="Árbol ATS", command=elegir_arbol_ats)
arbol_ats_boton.pack(pady=5)

analizar_boton = tk.Button(ventana, text="Analizar", command=analizar_expresion)
analizar_boton.pack(pady=10)

derivar_paso_boton = tk.Button(ventana, text="Derivación paso a paso", command=derivacion_paso_a_paso)
derivar_paso_boton.pack(pady=10)

resultado_text = tk.Text(ventana, width=60, height=15)
resultado_text.pack(pady=10)

ventana.mainloop()
