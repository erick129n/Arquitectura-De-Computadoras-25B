import tkinter as tk
from tkinter import ttk, scrolledtext
import tkinter.messagebox as messagebox
import os

ventana = tk.Tk()
ventana.title("Decodificador de Instrucciones MIPS Tipo R")
ventana.geometry("700x600")

# Frame principal con scrollbar
main_frame = tk.Frame(ventana)
main_frame.pack(fill=tk.BOTH, expand=True)

# Canvas y scrollbar para la ventana principal
canvas = tk.Canvas(main_frame)
scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Diccionario de operaciones lógicas y aritméticas (funct)
instruccion_logica_aritmetica = {
    '100000': 'ADD', '100100': 'AND', 
    '101010': 'MAQ', '100111': 'NOR', '100101': 'OR'
}

valor_operacion_tipo_r = '000000'  # opcode
valor_shampt = '00000'             # shamt

# ---------------------------------
# Funciones auxiliares
# ---------------------------------

def limpiar_dato(dato):
    """Elimina los símbolos $, , y ; de un dato."""
    return dato.replace('$', '').replace(',', '').replace(';', '').strip()

def extraer_elementos(linea):
    """Devuelve la instrucción y los datos de una línea."""
    partes = linea.strip().split()
    if not partes:
        return None, []  # línea vacía

    instruccion = partes[0].upper()
    datos = [limpiar_dato(p) for p in partes[1:] if limpiar_dato(p)]
    return instruccion, datos

def obtener_codigo_binario(instruccion):
    """Devuelve el código binario asociado a la instrucción."""
    for clave, valor in instruccion_logica_aritmetica.items():
        if valor == instruccion:
            return clave
    return None

def convertir_a_binario(numero):
    """Convierte un número entero a binario de 5 bits."""
    return format(int(numero), '05b')

def dividir_en_bytes(binario):
    """Divide una cadena binaria en grupos de 8 bits separados por salto de línea."""
    bytes_list = [binario[i:i+8] for i in range(0, len(binario), 8)]
    return '\n'.join(bytes_list)

# Función para exportar a archivo
def exportar_a_archivo():
    contenido = memoria_text.get("1.0", tk.END).strip()
    with open("..\\ArqMIPS\\instrucciones.txt", "w") as archivo:
        archivo.write(contenido)

# ---------------------------------
# Conversión completa
# ---------------------------------

def convertir():
    texto = in_assembly.get("1.0", tk.END).strip()
    lineas = texto.splitlines()
    instruccion_convertida_text.delete("1.0", tk.END)
    memoria_text.delete("1.0", tk.END)  # Limpiar memoria también

    for linea in lineas:
        if not linea.strip():
            continue

        instruccion, datos = extraer_elementos(linea)
        if not instruccion or len(datos) < 3:
            messagebox.showerror("Error", f"Línea inválida: {linea}")
            continue

        funct = obtener_codigo_binario(instruccion)
        if not funct:
            messagebox.showerror("Error", f"Instrucción desconocida: {instruccion}")
            continue

        # Orden tipo R: $d, $s, $t
        rd = convertir_a_binario(datos[0])
        rs = convertir_a_binario(datos[1])
        rt = convertir_a_binario(datos[2])

        # Concatenación: opcode + rs + rt + rd + shamt + funct
        instruccion_final = valor_operacion_tipo_r + rs + rt + rd + valor_shampt + funct
        binario_en_bytes = dividir_en_bytes(instruccion_final)

        # Insertar en los campos de texto
        instruccion_convertida_text.insert(tk.END, instruccion_final + "\n")
        
        # Insertar los bytes con saltos de línea y un separador entre instrucciones
        memoria_text.insert(tk.END, binario_en_bytes + "\n" )


def binario_a_ensamblador():
    # Obtener el texto binario del campo de instrucción convertida
    texto_binario = instruccion_convertida_text.get("1.0", tk.END).strip()
    
    if not texto_binario:
        return
    
    lineas_binario = texto_binario.splitlines()
    resultado_ensamblador = ""
    resultado_memoria = ""
    
    for binario in lineas_binario:
        if len(binario) != 32:
            messagebox.showerror("Error", f"Instrucción binaria inválida: {binario}")
            continue
        
        # Extraer las partes de la instrucción tipo R
        opcode = binario[0:6]
        rs = binario[6:11]
        rt = binario[11:16]
        rd = binario[16:21]
        shamt = binario[21:26]
        funct = binario[26:32]
        
        # Verificar que sea tipo R
        if opcode != '000000':
            messagebox.showerror("Error", f"No es una instrucción tipo R: {binario}")
            continue
        
        # Buscar la instrucción en el diccionario
        instruccion = None
        for clave, valor in instruccion_logica_aritmetica.items():
            if clave == funct:
                instruccion = valor
                break
        
        if not instruccion:
            messagebox.showerror("Error", f"Instrucción desconocida para funct: {funct}")
            continue
        
        # Convertir registros a decimal
        try:
            reg_rd = int(rd, 2)
            reg_rs = int(rs, 2)
            reg_rt = int(rt, 2)
        except ValueError:
            messagebox.showerror("Error", f"Error al convertir registros en: {binario}")
            continue
        
        # Formar la instrucción ensamblador
        linea_ensamblador = f"{instruccion} ${reg_rd}, ${reg_rs}, ${reg_rt}"
        resultado_ensamblador += linea_ensamblador + "\n"
        
        # También generar la representación en bytes para memoria
        binario_en_bytes = dividir_en_bytes(binario)
        resultado_memoria += binario_en_bytes + "\n\n"
    
    # Mostrar los resultados en los cuadros existentes
    in_assembly.delete("1.0", tk.END)
    in_assembly.insert("1.0", resultado_ensamblador.strip())
    
    memoria_text.delete("1.0", tk.END)
    memoria_text.insert("1.0", resultado_memoria.strip())
# ---------------------------------
# Interfaz gráfica
# ---------------------------------

# Campo de entrada
instruccion_assembly_label = tk.Label(scrollable_frame, text="Instrucción en ensamblador:")
instruccion_assembly_label.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 5))

# Frame para el cuadro de texto de entrada con scrollbar
input_frame = tk.Frame(scrollable_frame)
input_frame.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 10))

in_assembly = tk.Text(input_frame, height=5, width=40)
in_assembly_scrollbar = ttk.Scrollbar(input_frame, command=in_assembly.yview)
in_assembly.configure(yscrollcommand=in_assembly_scrollbar.set)

in_assembly.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
in_assembly_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Botones
button_frame = tk.Frame(scrollable_frame)
button_frame.grid(row=1, column=1, padx=20, pady=(0, 10))

convertir_button = ttk.Button(button_frame, text="Convertir", command=convertir)
convertir_button.pack(pady=5)

exportar_button = ttk.Button(button_frame, text="Exportar a archivo", command=exportar_a_archivo)
exportar_button.pack(pady=5)

convertir_binario_assembly = ttk.Button(button_frame, text="Convertir Binario a Ensamblador", command=binario_a_ensamblador)
convertir_binario_assembly.pack(pady=5)

# Campo de salida - Instrucción convertida
instruccion_convertida_label = tk.Label(scrollable_frame, text="Instrucción convertida:")
instruccion_convertida_label.grid(row=2, column=0, sticky="w", padx=20, pady=(5, 2))


# Frame para el cuadro de texto de instrucción convertida con scrollbar
instruccion_frame = tk.Frame(scrollable_frame)
instruccion_frame.grid(row=3, column=0, sticky="w", padx=20, pady=(0, 10))

instruccion_convertida_text = tk.Text(instruccion_frame, height=5, width=33)
instruccion_scrollbar = ttk.Scrollbar(instruccion_frame, command=instruccion_convertida_text.yview)
instruccion_convertida_text.configure(yscrollcommand=instruccion_scrollbar.set)

instruccion_convertida_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
instruccion_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Campo de memoria
memoria_label = tk.Label(scrollable_frame, text="Memoria:")
memoria_label.grid(row=2, column=1, sticky="w", padx=20, pady=(10, 5))

# Frame para el cuadro de texto de memoria con scrollbar
memoria_frame = tk.Frame(scrollable_frame)
memoria_frame.grid(row=3, column=1, sticky="w", padx=20, pady=(0, 10))

memoria_text = tk.Text(memoria_frame, height=15, width=33)
memoria_scrollbar = ttk.Scrollbar(memoria_frame, command=memoria_text.yview)
memoria_text.configure(yscrollcommand=memoria_scrollbar.set)

memoria_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
memoria_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


# Configurar el scroll con la rueda del mouse
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)

ventana.mainloop()