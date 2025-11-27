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

valor_operacion_tipo_r = '000000'  # opcode
valor_shampt = '00000'             # shamt