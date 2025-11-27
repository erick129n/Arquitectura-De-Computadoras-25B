import re

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