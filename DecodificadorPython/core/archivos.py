import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import os

def abrir_archivo():
    """Abre un archivo existente."""
    archivo = filedialog.askopenfilename(
        title="Abrir archivo",
        filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
    )
    
    if not archivo:
        return None
    
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            contenido = f.read().strip()
        return contenido
    except Exception as e:
        raise Exception(f"Error al abrir el archivo: {str(e)}")

def guardar_archivo(contenido, titulo, nombre_default, tipo="instrucciones"):
    """Guarda contenido en un archivo."""
    if not contenido:
        raise ValueError(f"No hay contenido para guardar ({tipo})")
    
    opcion_guardar = messagebox.askyesno(
        "Guardar archivo",
        f"¿Desea seleccionar un archivo existente para sobrescribir?\n\n"
        f"Sí: Seleccionar archivo existente para sobrescribir\n"
        f"No: Crear nuevo archivo"
    )
    
    if opcion_guardar:
        archivo = filedialog.askopenfilename(title=titulo)
    else:
        archivo = filedialog.asksaveasfilename(
            title=titulo,
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
            initialfile=nombre_default
        )
    
    if not archivo:
        return None
    
    try:
        if not opcion_guardar and os.path.exists(archivo):
            respuesta = messagebox.askyesno(
                "Archivo existente", 
                f"El archivo '{os.path.basename(archivo)}' ya existe.\n¿Desea sobrescribirlo?"
            )
            if not respuesta:
                return None
        
        with open(archivo, "w", encoding="utf-8") as f:
            f.write(contenido)
        
        return archivo
        
    except Exception as e:
        raise Exception(f"Error al guardar el archivo: {str(e)}")