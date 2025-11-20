import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import tkinter.messagebox as messagebox
import os
import re

ventana = tk.Tk()
ventana.title("Decodificador de Instrucciones MIPS")
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

# Diccionario de operaciones lógicas y aritméticas (funct) - ACTUALIZADO CON SUB
instruccion_logica_aritmetica = {
    '100000': 'ADD',   # Add
    '100010': 'SUB',   # Subtract - NUEVO
    '100100': 'AND',   # And
    '100111': 'NOR',   # Nor
    '100101': 'OR',    # Or
    '101010': 'SLT'    # Set Less Than
}

# Diccionario de instrucciones inmediatas (opcode)
instruccion_logica_aritmetica_inmediata = {
    '001000': 'ADDI',  # Add Immediate
    '001001': 'ADDIU', # Add Immediate Unsigned
    '001100': 'ANDI',  # And Immediate
    '001101': 'ORI',   # Or Immediate
    '001110': 'XORI',  # Xor Immediate
    '001010': 'SLTI',  # Set Less Than Immediate
    '001011': 'SLTIU'  # Set Less Than Immediate Unsigned
}

# Diccionario de instrucciones de carga/almacenamiento (opcode) - TIPO I MEMORIA
instrucciones_memoria = {
    '100011': 'LW',    # Load Word
    '101011': 'SW',    # Store Word
}

# Diccionario de instrucciones de salto condicional (opcode) - TIPO I
instrucciones_condicionales = {
    '000100': 'BEQ',   # Branch if Equal
    '000101': 'BNE'    # Branch if Not Equal
}

# Diccionario de instrucciones de salto incondicional (opcode) - TIPO J
instrucciones_salto = {
    '000010': 'J',     # Jump
    '000011': 'JAL'    # Jump and Link
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
    # Buscar en instrucciones tipo R
    for clave, valor in instruccion_logica_aritmetica.items():
        if valor == instruccion:
            return ('R', clave)
    
    # Buscar en instrucciones inmediatas
    for clave, valor in instruccion_logica_aritmetica_inmediata.items():
        if valor == instruccion:
            return ('I', clave)
    
    # Buscar en instrucciones de memoria
    for clave, valor in instrucciones_memoria.items():
        if valor == instruccion:
            return ('M', clave)
    
    # Buscar en instrucciones de salto condicional
    for clave, valor in instrucciones_condicionales.items():
        if valor == instruccion:
            return ('C', clave)  # 'C' para condicional
    
    # Buscar en instrucciones de salto incondicional (tipo J)
    for clave, valor in instrucciones_salto.items():
        if valor == instruccion:
            return ('J', clave)  # 'J' para jump
    
    return (None, None)

def convertir_a_binario(numero, bits=5):
    """Convierte un número entero a binario con la cantidad de bits especificada."""
    # Si el número es 'zero', convertir a 0
    if isinstance(numero, str) and numero.upper() == 'ZERO':
        return format(0, f'0{bits}b')
    return format(int(numero), f'0{bits}b')

def convertir_inmediato_a_binario(numero, bits=16):
    """Convierte un número inmediato a binario de 16 bits (complemento a 2 para negativos)."""
    num = int(numero)
    if num < 0:
        # Complemento a 2 para números negativos
        return format((1 << bits) + num, f'0{bits}b')
    else:
        return format(num, f'0{bits}b')

def convertir_desplazamiento_a_binario(numero, bits=16):
    """Convierte un desplazamiento de salto a binario de 16 bits."""
    # Para saltos, el desplazamiento es el número de instrucciones a saltar
    # Se divide entre 4 porque cada instrucción ocupa 4 bytes
    num = int(numero)
    desplazamiento = num // 4  # Convertir dirección de bytes a palabras
    return convertir_inmediato_a_binario(desplazamiento, bits)

def convertir_direccion_a_binario(numero, bits=26):
    """Convierte una dirección de salto a binario de 26 bits."""
    # Para saltos tipo J, la dirección se divide entre 4 (dirección de palabra)
    num = int(numero)
    direccion = num // 4  # Convertir dirección de bytes a palabras
    return format(direccion, f'0{bits}b')

def dividir_en_bytes(binario):
    """Divide una cadena binaria en grupos de 8 bits separados por salto de línea."""
    bytes_list = [binario[i:i+8] for i in range(0, len(binario), 8)]
    return '\n'.join(bytes_list)

def parsear_instruccion_memoria(datos):
    if len(datos) < 2:
        return None, None, None
    
    rt = datos[0]

    match = re.match(r'(\-?\d+)\((\d+)\)', datos[1])
    if match:
        offset = match.group(1)
        rs = match.group(2)
        return rt, rs, offset
    else:
        if len(datos) >= 3:
            return datos[0], datos[2], datos[1]
    return None, None, None

# ---------------------------------
# Funciones para manejar archivos
# ---------------------------------

def abrir_archivo():
    """Abre un archivo existente y pregunta si cargar los datos al programa."""
    archivo = filedialog.askopenfilename(
        title="Abrir archivo",
        filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
    )
    
    if not archivo:
        return
    
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            contenido = f.read().strip()
        
        if not contenido:
            messagebox.showwarning("Advertencia", "El archivo está vacío")
            return
        
        # Preguntar si cargar los datos al programa
        respuesta = messagebox.askyesno(
            "Cargar archivo",
            f"¿Desea cargar el contenido del archivo '{os.path.basename(archivo)}' al programa?\n\n"
            "Nota: Esto reemplazará el contenido actual en el campo de ensamblador."
        )
        
        if respuesta:
            in_assembly.delete("1.0", tk.END)
            in_assembly.insert("1.0", contenido)
            messagebox.showinfo("Éxito", "Archivo cargado correctamente")
        
    except FileNotFoundError:
        messagebox.showerror("Error", "El archivo no fue encontrado")
    except PermissionError:
        messagebox.showerror("Error", "No tiene permisos para leer este archivo")
    except UnicodeDecodeError:
        messagebox.showerror("Error", "Error al leer el archivo. Formato no compatible")
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado al abrir el archivo:\n{str(e)}")

def exportar_a_archivo():
    """Exporta el contenido del campo Memoria a un archivo."""
    contenido_memoria = memoria_text.get("1.0", tk.END).strip()
    
    if not contenido_memoria:
        messagebox.showwarning("Advertencia", "No hay contenido en Memoria para exportar")
        return
    
    # Preguntar si sobrescribir o crear nuevo
    opcion_guardar = messagebox.askyesno(
        "Guardar archivo",
        "¿Desea seleccionar un archivo existente para sobrescribir?\n\n"
        "Sí: Seleccionar archivo existente para sobrescribir\n"
        "No: Crear nuevo archivo"
    )
    
    if opcion_guardar:
        # Sobrescribir archivo existente
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo para sobrescribir (Memoria)",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
    else:
        # Crear nuevo archivo
        archivo = filedialog.asksaveasfilename(
            title="Guardar como nuevo archivo (Memoria)",
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
            initialfile="memoria_instrucciones.txt"
        )
    
    if not archivo:
        return
    
    try:
        # Verificar si el archivo ya existe (para el caso de crear nuevo)
        if not opcion_guardar and os.path.exists(archivo):
            respuesta = messagebox.askyesno(
                "Archivo existente", 
                f"El archivo '{os.path.basename(archivo)}' ya existe.\n¿Desea sobrescribirlo?"
            )
            if not respuesta:
                return
        
        # Guardar el archivo
        with open(archivo, "w", encoding="utf-8") as f:
            f.write(contenido_memoria)
        
        messagebox.showinfo("Éxito", f"Contenido de Memoria guardado en:\n{archivo}")
        
    except PermissionError:
        messagebox.showerror("Error", "No tiene permisos para guardar en esta ubicación")
    except OSError as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado:\n{str(e)}")

# ---------------------------------
# Conversión completa
# ---------------------------------

def convertir():
    texto = in_assembly.get("1.0", tk.END).strip()
    lineas = texto.splitlines()
    instruccion_convertida_text.delete("1.0", tk.END)
    memoria_text.delete("1.0", tk.END)

    for linea in lineas:
        if not linea.strip():
            continue

        instruccion, datos = extraer_elementos(linea)
        if not instruccion or len(datos) < 1:
            messagebox.showerror("Error", f"Línea inválida: {linea}")
            continue

        tipo, codigo = obtener_codigo_binario(instruccion)
        if not tipo or not codigo:
            messagebox.showerror("Error", f"Instrucción desconocida: {instruccion}")
            continue

        if tipo == 'R':
            # Instrucción tipo R: $d, $s, $t
            if len(datos) < 3:
                messagebox.showerror("Error", f"Instrucción tipo R requiere 3 operandos: {linea}")
                continue
            
            rd = convertir_a_binario(datos[0])
            rs = convertir_a_binario(datos[1])
            rt = convertir_a_binario(datos[2])

            # Concatenación: opcode + rs + rt + rd + shamt + funct
            instruccion_final = valor_operacion_tipo_r + rs + rt + rd + valor_shampt + codigo

        elif tipo == 'I':
            # Instrucción tipo I: $t, $s, inmediato
            if len(datos) < 3:
                messagebox.showerror("Error", f"Instrucción tipo I requiere 3 operandos: {linea}")
                continue
            
            rt = convertir_a_binario(datos[0])
            rs = convertir_a_binario(datos[1])
            inmediato = convertir_inmediato_a_binario(datos[2])

            # Concatenación: opcode + rs + rt + inmediato
            instruccion_final = codigo + rs + rt + inmediato

        elif tipo == 'M':
            # Instrucción tipo I de memoria: lw $t, offset($s)
            rt, rs, offset = parsear_instruccion_memoria(datos)

            if rt is None or rs is None or offset is None:
                messagebox.showerror("Error", f"Formato inválido para {instruccion}. Use: {instruccion} $t, offset($s)")
                continue

            rt_bin = convertir_a_binario(rt)
            rs_bin = convertir_a_binario(rs)
            offset_bin = convertir_inmediato_a_binario(offset)

            instruccion_final = codigo + rs_bin + rt_bin + offset_bin

        elif tipo == 'C':
            # Instrucción de salto condicional: beq $s, $t, desplazamiento
            if len(datos) < 3:
                messagebox.showerror("Error", f"Instrucción {instruccion} requiere 3 operandos: {linea}")
                continue
            
            rs = convertir_a_binario(datos[0])
            rt = convertir_a_binario(datos[1])
            desplazamiento = convertir_desplazamiento_a_binario(datos[2])

            # Concatenación: opcode + rs + rt + desplazamiento
            instruccion_final = codigo + rs + rt + desplazamiento

        elif tipo == 'J':
            # Instrucción tipo J: j dirección
            if len(datos) < 1:
                messagebox.showerror("Error", f"Instrucción {instruccion} requiere 1 operando: {linea}")
                continue
            
            direccion = convertir_direccion_a_binario(datos[0])

            # Concatenación: opcode + dirección
            instruccion_final = codigo + direccion

        else:
            messagebox.showerror("Error", f"Tipo de instrucción no soportado: {tipo}")
            continue

        binario_en_bytes = dividir_en_bytes(instruccion_final)

        # Insertar en los campos de texto
        instruccion_convertida_text.insert(tk.END, instruccion_final + "\n")
        memoria_text.insert(tk.END, binario_en_bytes + "\n")

def binario_a_ensamblador():
    """Convierte el contenido de Instrucción convertida (binario) a ensamblador"""
    # Obtener el texto binario del campo de instrucción convertida
    texto_binario = instruccion_convertida_text.get("1.0", tk.END).strip()
    
    if not texto_binario:
        messagebox.showwarning("Advertencia", "No hay código binario para convertir")
        return
    
    lineas_binario = texto_binario.splitlines()
    resultado_ensamblador = ""
    resultado_memoria = ""
    
    for binario in lineas_binario:
        if len(binario) != 32:
            messagebox.showerror("Error", f"Instrucción binaria inválida: {binario}")
            continue
        
        # Extraer opcode primero para determinar el tipo
        opcode = binario[0:6]
        
        if opcode == '000000':
            # Instrucción tipo R
            rs = binario[6:11]
            rt = binario[11:16]
            rd = binario[16:21]
            shamt = binario[21:26]
            funct = binario[26:32]
            
            # Buscar la instrucción en el diccionario tipo R
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
            
            # Formar la instrucción ensamblador tipo R
            linea_ensamblador = f"{instruccion} ${reg_rd}, ${reg_rs}, ${reg_rt}"
            
        elif opcode in ['000010', '000011']:
            # Instrucción tipo J: j dirección o jal dirección
            direccion_bin = binario[6:32]  # 26 bits de dirección
            
            # Buscar la instrucción en el diccionario tipo J
            instruccion = None
            for clave, valor in instrucciones_salto.items():
                if clave == opcode:
                    instruccion = valor
                    break
            
            if not instruccion:
                messagebox.showerror("Error", f"Instrucción desconocida para opcode: {opcode}")
                continue
            
            # Convertir dirección (de palabras a bytes)
            try:
                direccion_valor = int(direccion_bin, 2)
                direccion_bytes = direccion_valor * 4  # Convertir a dirección de bytes
            except ValueError:
                messagebox.showerror("Error", f"Error al convertir dirección en: {binario}")
                continue
            
            # Formar la instrucción ensamblador tipo J
            linea_ensamblador = f"{instruccion} {direccion_bytes}"
            
        else:
            # Instrucción tipo I (inmediata)
            rs = binario[6:11]
            rt = binario[11:16]
            inmediato = binario[16:32]
            
            # Buscar la instrucción en los diccionarios
            instruccion = None
            tipo_instruccion = None
            
            # Buscar en instrucciones aritméticas inmediatas
            for clave, valor in instruccion_logica_aritmetica_inmediata.items():
                if clave == opcode:
                    instruccion = valor
                    tipo_instruccion = 'A'
                    break
            
            # Buscar en instrucciones de memoria
            if not instruccion:
                for clave, valor in instrucciones_memoria.items():
                    if clave == opcode:
                        instruccion = valor
                        tipo_instruccion = 'M'
                        break
            
            # Buscar en instrucciones de salto condicional
            if not instruccion:
                for clave, valor in instrucciones_condicionales.items():
                    if clave == opcode:
                        instruccion = valor
                        tipo_instruccion = 'C'
                        break
            
            if not instruccion:
                messagebox.showerror("Error", f"Instrucción desconocida para opcode: {opcode}")
                continue
            
            # Convertir registros e inmediato
            try:
                reg_rs = int(rs, 2)
                reg_rt = int(rt, 2)
                
                # Convertir inmediato (complemento a 2 para negativos)
                imm_valor = int(inmediato, 2)
                if inmediato[0] == '1':  # Si es negativo
                    imm_valor = imm_valor - (1 << 16)
                
            except ValueError:
                messagebox.showerror("Error", f"Error al convertir registros/inmediato en: {binario}")
                continue
            
            # Formar la instrucción ensamblador según el tipo
            if tipo_instruccion == 'A':
                linea_ensamblador = f"{instruccion} ${reg_rt}, ${reg_rs}, {imm_valor}"
            elif tipo_instruccion == 'M':
                # Instrucción de memoria: $t, offset($s)
                linea_ensamblador = f"{instruccion} ${reg_rt}, {imm_valor}(${reg_rs})"
            elif tipo_instruccion == 'C':
                # Instrucción de salto condicional: beq $s, $t, desplazamiento
                # Convertir desplazamiento de palabras a bytes (multiplicar por 4)
                direccion = imm_valor * 4
                linea_ensamblador = f"{instruccion} ${reg_rs}, ${reg_rt}, {direccion}"
        
        resultado_ensamblador += linea_ensamblador + "\n"
        
        # También generar la representación en bytes para memoria
        binario_en_bytes = dividir_en_bytes(binario)
        resultado_memoria += binario_en_bytes + "\n\n"
    
    # Mostrar los resultados en los cuadros existentes
    in_assembly.delete("1.0", tk.END)
    in_assembly.insert("1.0", resultado_ensamblador.strip())
    
    memoria_text.delete("1.0", tk.END)
    memoria_text.insert("1.0", resultado_memoria.strip())
    
    messagebox.showinfo("Éxito", "Conversión completada correctamente")

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

abrir_button = ttk.Button(button_frame, text="Abrir Archivo", command=abrir_archivo)
abrir_button.pack(pady=5)

convertir_button = ttk.Button(button_frame, text="Convertir", command=convertir)
convertir_button.pack(pady=5)

exportar_button = ttk.Button(button_frame, text="Exportar Memoria", command=exportar_a_archivo)
exportar_button.pack(pady=5)

convertir_binario_assembly = ttk.Button(button_frame, text="Binario a Ensamblador", command=binario_a_ensamblador)
convertir_binario_assembly.pack(pady=5)

# Información sobre instrucciones soportadas - ACTUALIZADA CON SUB
info_label = tk.Label(button_frame, 
                     text="\nInstrucciones soportadas:\n"
                          "Tipo R: ADD, SUB, AND, NOR, OR, SLT\n"
                          "Tipo I: ADDI, ADDIU, ANDI, ORI, XORI, SLTI, SLTIU\n"
                          "Memoria: LW, SW\n"
                          "Salto Condicional: BEQ, BNE\n"
                          "Salto Incondicional: J, JAL\n\n"
                          "Registros especiales:\n"
                          "$zero o $0 = registro constante 0", 
                     justify=tk.LEFT, font=("Arial", 8))
info_label.pack(pady=10)

# Campo de salida - Instrucción convertida
instruccion_convertida_label = tk.Label(scrollable_frame, text="Instrucción convertida (32 bits):")
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
memoria_label = tk.Label(scrollable_frame, text="Memoria (bytes):")
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