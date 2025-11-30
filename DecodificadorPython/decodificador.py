import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import tkinter.messagebox as messagebox
import os
import re

ventana = tk.Tk()
ventana.title("Decodificador de Instrucciones MIPS")
ventana.geometry("900x700")
ventana.configure(bg='#f0f0f0')

# Estilo moderno
style = ttk.Style()
style.configure('TButton', font=('Arial', 10), padding=6)
style.configure('TFrame', background='#f0f0f0')
style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
style.configure('TLabelframe', background='#f0f0f0', font=('Arial', 10, 'bold'))
style.configure('TLabelframe.Label', background='#f0f0f0', font=('Arial', 10, 'bold'))

# Diccionario de operaciones lógicas y aritméticas (funct)
instruccion_logica_aritmetica = {
    '100000': 'ADD',   # Add
    '100010': 'SUB',   # Subtract
    '100100': 'AND',   # And
    '100111': 'NOR',   # Nor
    '100101': 'OR',    # Or
    '101010': 'SLT',   # Set Less Than
    '000000': 'NOP'    # No Operation
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

# Diccionario de instrucciones de carga/almacenamiento (opcode)
instrucciones_memoria = {
    '100011': 'LW',    # Load Word
    '101011': 'SW',    # Store Word
    '100000': 'LB',    # Load Byte
    '101000': 'SB'     # Store Byte
}

# Diccionario de instrucciones de salto condicional (opcode)
instrucciones_condicionales = {
    '000100': 'BEQ',   # Branch if Equal
    '000101': 'BNE'    # Branch if Not Equal
}

# Diccionario de instrucciones de salto incondicional (opcode)
instrucciones_salto = {
    '000010': 'J',     # Jump
    '000011': 'JAL'    # Jump and Link
}

valor_operacion_tipo_r = '000000'
valor_shampt = '00000'

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
        return None, []
    instruccion = partes[0].upper()
    datos = [limpiar_dato(p) for p in partes[1:] if limpiar_dato(p)]
    return instruccion, datos

def obtener_codigo_binario(instruccion):
    """Devuelve el código binario asociado a la instrucción."""
    for clave, valor in instruccion_logica_aritmetica.items():
        if valor == instruccion:
            return ('R', clave)
    for clave, valor in instruccion_logica_aritmetica_inmediata.items():
        if valor == instruccion:
            return ('I', clave)
    for clave, valor in instrucciones_memoria.items():
        if valor == instruccion:
            return ('M', clave)
    for clave, valor in instrucciones_condicionales.items():
        if valor == instruccion:
            return ('C', clave)
    for clave, valor in instrucciones_salto.items():
        if valor == instruccion:
            return ('J', clave)
    return (None, None)

def convertir_a_binario(numero, bits=5):
    """Convierte un número entero a binario con la cantidad de bits especificada."""
    if isinstance(numero, str) and numero.upper() == 'ZERO':
        return format(0, f'0{bits}b')
    return format(int(numero), f'0{bits}b')

def convertir_inmediato_a_binario(numero, bits=16):
    """Convierte un número inmediato a binario de 16 bits (complemento a 2 para negativos)."""
    num = int(numero)
    if num < 0:
        return format((1 << bits) + num, f'0{bits}b')
    else:
        return format(num, f'0{bits}b')

def convertir_desplazamiento_a_binario(numero, bits=16):
    """Convierte un desplazamiento de salto a binario de 16 bits."""
    num = int(numero)
    desplazamiento = num // 4
    return convertir_inmediato_a_binario(desplazamiento, bits)

def convertir_direccion_a_binario(numero, bits=26):
    """Convierte una dirección de salto a binario de 26 bits."""
    num = int(numero)
    direccion = num // 4
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
    actualizar_estado("Abriendo archivo...")
    archivo = filedialog.askopenfilename(
        title="Abrir archivo",
        filetypes=[("Archivos MIPS", "*.asm"), ("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
    )
    
    if not archivo:
        actualizar_estado("Operación cancelada")
        return
    
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            contenido = f.read().strip()
        
        if not contenido:
            messagebox.showwarning("Advertencia", "El archivo está vacío")
            actualizar_estado("Archivo vacío")
            return
        
        respuesta = messagebox.askyesno(
            "Cargar archivo",
            f"¿Desea cargar el contenido del archivo '{os.path.basename(archivo)}' al programa?"
        )
        
        if respuesta:
            in_assembly.delete("1.0", tk.END)
            in_assembly.insert("1.0", contenido)
            lineas = len(contenido.splitlines())
            actualizar_estado(f"Archivo cargado: {lineas} líneas")
            messagebox.showinfo("Éxito", "Archivo cargado correctamente")
        else:
            actualizar_estado("Carga cancelada por el usuario")
        
    except FileNotFoundError:
        messagebox.showerror("Error", "El archivo no fue encontrado")
        actualizar_estado("Error: Archivo no encontrado")
    except PermissionError:
        messagebox.showerror("Error", "No tiene permisos para leer este archivo")
        actualizar_estado("Error: Sin permisos")
    except UnicodeDecodeError:
        messagebox.showerror("Error", "Error al leer el archivo. Formato no compatible")
        actualizar_estado("Error: Formato no compatible")
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado al abrir el archivo:\n{str(e)}")
        actualizar_estado("Error al abrir archivo")

def guardar_instrucciones():
    """Guarda las instrucciones escritas por el usuario en un archivo de texto."""
    actualizar_estado("Guardando instrucciones...")
    contenido_ensamblador = in_assembly.get("1.0", tk.END).strip()
    
    if not contenido_ensamblador:
        messagebox.showwarning("Advertencia", "No hay instrucciones para guardar")
        actualizar_estado("No hay contenido para guardar")
        return
    
    archivo = filedialog.asksaveasfilename(
        title="Guardar instrucciones MIPS",
        defaultextension=".asm",
        filetypes=[("Archivos MIPS", "*.asm"), ("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
        initialfile="programa_mips.asm"
    )
    
    if not archivo:
        actualizar_estado("Guardado cancelado")
        return
    
    try:
        with open(archivo, "w", encoding="utf-8") as f:
            f.write(contenido_ensamblador)
        
        actualizar_estado(f"Instrucciones guardadas en: {os.path.basename(archivo)}")
        messagebox.showinfo("Éxito", f"Instrucciones guardadas en:\n{archivo}")
        
    except PermissionError:
        messagebox.showerror("Error", "No tiene permisos para guardar en esta ubicación")
        actualizar_estado("Error: Sin permisos de escritura")
    except OSError as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")
        actualizar_estado("Error al guardar archivo")
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado:\n{str(e)}")
        actualizar_estado("Error inesperado al guardar")

def exportar_a_archivo():
    """Exporta el contenido del campo Memoria a un archivo."""
    actualizar_estado("Exportando memoria...")
    contenido_memoria = memoria_text.get("1.0", tk.END).strip()
    
    if not contenido_memoria:
        messagebox.showwarning("Advertencia", "No hay contenido en Memoria para exportar")
        actualizar_estado("No hay memoria para exportar")
        return
    
    archivo = filedialog.asksaveasfilename(
        title="Exportar memoria",
        defaultextension=".bin",
        filetypes=[("Archivos binarios", "*.bin"), ("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
        initialfile="memoria_mips.bin"
    )
    
    if not archivo:
        actualizar_estado("Exportación cancelada")
        return
    
    try:
        with open(archivo, "w", encoding="utf-8") as f:
            f.write(contenido_memoria)
        
        actualizar_estado(f"Memoria exportada: {os.path.basename(archivo)}")
        messagebox.showinfo("Éxito", f"Contenido de Memoria exportado en:\n{archivo}")
        
    except PermissionError:
        messagebox.showerror("Error", "No tiene permisos para guardar en esta ubicación")
        actualizar_estado("Error: Sin permisos de escritura")
    except OSError as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")
        actualizar_estado("Error al exportar archivo")
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado:\n{str(e)}")
        actualizar_estado("Error inesperado al exportar")

# ---------------------------------
# Conversión completa
# ---------------------------------

def convertir():
    """Convierte código ensamblador a binario"""
    actualizar_estado("Convirtiendo instrucciones...")
    texto = in_assembly.get("1.0", tk.END).strip()
    lineas = texto.splitlines()
    instruccion_convertida_text.delete("1.0", tk.END)
    memoria_text.delete("1.0", tk.END)

    lineas_procesadas = 0
    errores = 0

    for linea in lineas:
        if not linea.strip():
            continue

        instruccion, datos = extraer_elementos(linea)
        if not instruccion:
            messagebox.showerror("Error", f"Línea inválida: {linea}")
            errores += 1
            continue

        # Manejar instrucción NOP primero
        if instruccion == 'NOP':
            instruccion_final = '00000000000000000000000000000000'
        
        else:
            tipo, codigo = obtener_codigo_binario(instruccion)
            if not tipo or not codigo:
                messagebox.showerror("Error", f"Instrucción desconocida: {instruccion}")
                errores += 1
                continue

            if tipo == 'R':
                if len(datos) < 3:
                    messagebox.showerror("Error", f"Instrucción tipo R requiere 3 operandos: {linea}")
                    errores += 1
                    continue
                
                try:
                    rd = convertir_a_binario(datos[0])
                    rs = convertir_a_binario(datos[1])
                    rt = convertir_a_binario(datos[2])
                    instruccion_final = valor_operacion_tipo_r + rs + rt + rd + valor_shampt + codigo
                except Exception as e:
                    messagebox.showerror("Error", f"Error en operandos: {linea}\n{str(e)}")
                    errores += 1
                    continue

            elif tipo == 'I':
                if len(datos) < 3:
                    messagebox.showerror("Error", f"Instrucción tipo I requiere 3 operandos: {linea}")
                    errores += 1
                    continue
                
                try:
                    rt = convertir_a_binario(datos[0])
                    rs = convertir_a_binario(datos[1])
                    inmediato = convertir_inmediato_a_binario(datos[2])
                    instruccion_final = codigo + rs + rt + inmediato
                except Exception as e:
                    messagebox.showerror("Error", f"Error en operandos: {linea}\n{str(e)}")
                    errores += 1
                    continue

            elif tipo == 'M':
                rt, rs, offset = parsear_instruccion_memoria(datos)
                if rt is None or rs is None or offset is None:
                    messagebox.showerror("Error", f"Formato inválido para {instruccion}. Use: {instruccion} $t, offset($s)")
                    errores += 1
                    continue

                try:
                    rt_bin = convertir_a_binario(rt)
                    rs_bin = convertir_a_binario(rs)
                    offset_bin = convertir_inmediato_a_binario(offset)
                    instruccion_final = codigo + rs_bin + rt_bin + offset_bin
                except Exception as e:
                    messagebox.showerror("Error", f"Error en operandos: {linea}\n{str(e)}")
                    errores += 1
                    continue

            elif tipo == 'C':
                if len(datos) < 3:
                    messagebox.showerror("Error", f"Instrucción {instruccion} requiere 3 operandos: {linea}")
                    errores += 1
                    continue
                
                try:
                    rs = convertir_a_binario(datos[0])
                    rt = convertir_a_binario(datos[1])
                    desplazamiento = convertir_desplazamiento_a_binario(datos[2])
                    instruccion_final = codigo + rs + rt + desplazamiento
                except Exception as e:
                    messagebox.showerror("Error", f"Error en operandos: {linea}\n{str(e)}")
                    errores += 1
                    continue

            elif tipo == 'J':
                if len(datos) < 1:
                    messagebox.showerror("Error", f"Instrucción {instruccion} requiere 1 operando: {linea}")
                    errores += 1
                    continue
                
                try:
                    direccion = convertir_direccion_a_binario(datos[0])
                    instruccion_final = codigo + direccion
                except Exception as e:
                    messagebox.showerror("Error", f"Error en operando: {linea}\n{str(e)}")
                    errores += 1
                    continue

            else:
                messagebox.showerror("Error", f"Tipo de instrucción no soportado: {tipo}")
                errores += 1
                continue

        binario_en_bytes = dividir_en_bytes(instruccion_final)
        instruccion_convertida_text.insert(tk.END, instruccion_final + "\n")
        memoria_text.insert(tk.END, binario_en_bytes + "\n")
        lineas_procesadas += 1
    
    if errores == 0:
        actualizar_estado(f"Conversión completada - {lineas_procesadas} instrucciones procesadas")
    else:
        actualizar_estado(f"Conversión con {errores} errores - {lineas_procesadas} instrucciones procesadas")

def binario_a_ensamblador():
    """Convierte el contenido de Instrucción convertida (binario) a ensamblador"""
    actualizar_estado("Convirtiendo binario a ensamblador...")
    texto_binario = instruccion_convertida_text.get("1.0", tk.END).strip()
    
    if not texto_binario:
        messagebox.showwarning("Advertencia", "No hay código binario para convertir")
        actualizar_estado("No hay binario para convertir")
        return
    
    lineas_binario = texto_binario.splitlines()
    resultado_ensamblador = ""
    resultado_memoria = ""
    lineas_procesadas = 0
    errores = 0
    
    for binario in lineas_binario:
        if len(binario) != 32:
            messagebox.showerror("Error", f"Instrucción binaria inválida: {binario}")
            errores += 1
            continue
        
        opcode = binario[0:6]
        
        if opcode == '000000':
            rs = binario[6:11]
            rt = binario[11:16]
            rd = binario[16:21]
            shamt = binario[21:26]
            funct = binario[26:32]
            
            # Verificar si es NOP (todos los campos en cero)
            if binario == '00000000000000000000000000000000':
                linea_ensamblador = "NOP"
            else:
                instruccion = None
                for clave, valor in instruccion_logica_aritmetica.items():
                    if clave == funct:
                        instruccion = valor
                        break
                
                if not instruccion:
                    messagebox.showerror("Error", f"Instrucción desconocida para funct: {funct}")
                    errores += 1
                    continue
                
                try:
                    reg_rd = int(rd, 2)
                    reg_rs = int(rs, 2)
                    reg_rt = int(rt, 2)
                    linea_ensamblador = f"{instruccion} ${reg_rd}, ${reg_rs}, ${reg_rt}"
                except ValueError:
                    messagebox.showerror("Error", f"Error al convertir registros en: {binario}")
                    errores += 1
                    continue
            
        elif opcode in ['000010', '000011']:
            direccion_bin = binario[6:32]
            
            instruccion = None
            for clave, valor in instrucciones_salto.items():
                if clave == opcode:
                    instruccion = valor
                    break
            
            if not instruccion:
                messagebox.showerror("Error", f"Instrucción desconocida para opcode: {opcode}")
                errores += 1
                continue
            
            try:
                direccion_valor = int(direccion_bin, 2)
                direccion_bytes = direccion_valor * 4
                linea_ensamblador = f"{instruccion} {direccion_bytes}"
            except ValueError:
                messagebox.showerror("Error", f"Error al convertir dirección en: {binario}")
                errores += 1
                continue
            
        else:
            rs = binario[6:11]
            rt = binario[11:16]
            inmediato = binario[16:32]
            
            instruccion = None
            tipo_instruccion = None
            
            for clave, valor in instruccion_logica_aritmetica_inmediata.items():
                if clave == opcode:
                    instruccion = valor
                    tipo_instruccion = 'A'
                    break
            
            if not instruccion:
                for clave, valor in instrucciones_memoria.items():
                    if clave == opcode:
                        instruccion = valor
                        tipo_instruccion = 'M'
                        break
            
            if not instruccion:
                for clave, valor in instrucciones_condicionales.items():
                    if clave == opcode:
                        instruccion = valor
                        tipo_instruccion = 'C'
                        break
            
            if not instruccion:
                messagebox.showerror("Error", f"Instrucción desconocida para opcode: {opcode}")
                errores += 1
                continue
            
            try:
                reg_rs = int(rs, 2)
                reg_rt = int(rt, 2)
                
                imm_valor = int(inmediato, 2)
                if inmediato[0] == '1':
                    imm_valor = imm_valor - (1 << 16)
                
                if tipo_instruccion == 'A':
                    linea_ensamblador = f"{instruccion} ${reg_rt}, ${reg_rs}, {imm_valor}"
                elif tipo_instruccion == 'M':
                    linea_ensamblador = f"{instruccion} ${reg_rt}, {imm_valor}(${reg_rs})"
                elif tipo_instruccion == 'C':
                    direccion = imm_valor * 4
                    linea_ensamblador = f"{instruccion} ${reg_rs}, ${reg_rt}, {direccion}"
            except ValueError:
                messagebox.showerror("Error", f"Error al convertir registros/inmediato en: {binario}")
                errores += 1
                continue
        
        resultado_ensamblador += linea_ensamblador + "\n"
        binario_en_bytes = dividir_en_bytes(binario)
        resultado_memoria += binario_en_bytes + "\n\n"
        lineas_procesadas += 1
    
    in_assembly.delete("1.0", tk.END)
    in_assembly.insert("1.0", resultado_ensamblador.strip())
    
    memoria_text.delete("1.0", tk.END)
    memoria_text.insert("1.0", resultado_memoria.strip())
    
    if errores == 0:
        actualizar_estado(f"Conversión completada - {lineas_procesadas} instrucciones")
        messagebox.showinfo("Éxito", "Conversión completada correctamente")
    else:
        actualizar_estado(f"Conversión con {errores} errores - {lineas_procesadas} instrucciones")
        messagebox.showwarning("Advertencia", f"Conversión completada con {errores} errores")

# ---------------------------------
# Interfaz gráfica
# ---------------------------------

# Frame principal organizado en dos columnas
main_frame = ttk.Frame(ventana)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# -----------------------------------------------
# COLUMNA IZQUIERDA - ENTRADA Y BOTONES
# -----------------------------------------------
left_frame = ttk.Frame(main_frame)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Campo de entrada más grande
input_frame = ttk.LabelFrame(left_frame, text="Código Ensamblador MIPS", padding=10)
input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

in_assembly = scrolledtext.ScrolledText(input_frame, height=15, width=60, font=('Consolas', 10))
in_assembly.pack(fill=tk.BOTH, expand=True)

# Frame para botones principales en grid
buttons_main_frame = ttk.Frame(left_frame)
buttons_main_frame.pack(fill=tk.X, pady=5)

# Primera fila de botones
button_row1 = ttk.Frame(buttons_main_frame)
button_row1.pack(fill=tk.X, pady=2)

abrir_button = ttk.Button(button_row1, text="📂 Abrir Archivo", command=abrir_archivo)
abrir_button.pack(side=tk.LEFT, padx=2)

guardar_button = ttk.Button(button_row1, text="💾 Guardar Instrucciones", command=guardar_instrucciones)
guardar_button.pack(side=tk.LEFT, padx=2)

# Segunda fila de botones
button_row2 = ttk.Frame(buttons_main_frame)
button_row2.pack(fill=tk.X, pady=2)

convertir_button = ttk.Button(button_row2, text="🔄 Convertir a Binario", command=convertir)
convertir_button.pack(side=tk.LEFT, padx=2)

convertir_binario_assembly = ttk.Button(button_row2, text="🔁 Binario a Ensamblador", command=binario_a_ensamblador)
convertir_binario_assembly.pack(side=tk.LEFT, padx=2)

# Tercera fila de botones
button_row3 = ttk.Frame(buttons_main_frame)
button_row3.pack(fill=tk.X, pady=2)

exportar_button = ttk.Button(button_row3, text="📤 Exportar Memoria", command=exportar_a_archivo)
exportar_button.pack(side=tk.LEFT, padx=2)

# Información sobre instrucciones
info_frame = ttk.LabelFrame(left_frame, text="📋 Instrucciones Soportadas", padding=8)
info_frame.pack(fill=tk.X, pady=5)

info_text = """Tipo R:    ADD, SUB, AND, NOR, OR, SLT, NOP
Tipo I:    ADDI, ADDIU, ANDI, ORI, XORI, SLTI, SLTIU
Memoria:   LW, SW, LB, SB
Saltos:    BEQ, BNE, J, JAL

Registros especiales:
$zero o $0 = registro constante 0"""

info_label = ttk.Label(info_frame, text=info_text, font=('Consolas', 9), justify=tk.LEFT)
info_label.pack()

# -----------------------------------------------
# COLUMNA DERECHA - RESULTADOS
# -----------------------------------------------
right_frame = ttk.Frame(main_frame)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

# Instrucción convertida
instruccion_frame = ttk.LabelFrame(right_frame, text="Instrucción Convertida (32 bits)", padding=8)
instruccion_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

instruccion_convertida_text = scrolledtext.ScrolledText(instruccion_frame, height=8, width=40, 
                                                       font=('Consolas', 10), background='#f8f8f8')
instruccion_convertida_text.pack(fill=tk.BOTH, expand=True)

# Memoria
memoria_frame = ttk.LabelFrame(right_frame, text="Memoria (Bytes)", padding=8)
memoria_frame.pack(fill=tk.BOTH, expand=True)

memoria_text = scrolledtext.ScrolledText(memoria_frame, height=12, width=40, 
                                        font=('Consolas', 10), background='#f8f8f8')
memoria_text.pack(fill=tk.BOTH, expand=True)

# -----------------------------------------------
# BARRA DE ESTADO
# -----------------------------------------------
status_frame = ttk.Frame(ventana)
status_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

status_label = ttk.Label(status_frame, text="Listo", font=('Arial', 9))
status_label.pack(side=tk.LEFT)

def actualizar_estado(mensaje):
    """Actualiza la barra de estado"""
    status_label.config(text=mensaje)
    ventana.update_idletasks()

# -----------------------------------------------
# EJECUCIÓN
# -----------------------------------------------
actualizar_estado("Decodificador MIPS listo - Escriba su código o abra un archivo")

# Ejemplo de código por defecto
codigo_ejemplo = """add $8, $9, $10
addi $11, $zero, 100
lw $12, 4($8)
sw $13, 8($9)
lb $14, 0($15)
sb $16, 4($17)
beq $8, $9, 16
j 2048
nop
sub $18, $19, $20"""

in_assembly.insert("1.0", codigo_ejemplo)

ventana.mainloop()