import os
import glob
import time
import tkinter as tk

def mostrar_popup(titulo, mensaje):
    """Muestra un pop-up con dos botones personalizados y devuelve la opción seleccionada."""
    def respuesta_opcion(opcion):
        nonlocal resultado
        resultado = opcion
        ventana.destroy()
    
    ventana = tk.Tk()
    ventana.title(titulo)
    
    # Establecer el tamaño de la ventana (ancho x alto)
    ventana.geometry('300x150')  # Cambia estos valores según tus necesidades
    
    # Centrar la ventana en la pantalla
    ventana.update_idletasks()  # Actualizar las tareas de la ventana para obtener su tamaño
    width = ventana.winfo_width()
    height = ventana.winfo_height()
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    ventana.geometry(f'{width}x{height}+{int(x)}+{int(y)}')


    # Crear una etiqueta para el mensaje
    etiqueta = tk.Label(ventana, text=mensaje)
    etiqueta.pack(padx=20, pady=10)
    
    # Botón 'Si'
    boton_seguir = tk.Button(ventana, text='Si', command=lambda: respuesta_opcion('Si'))
    boton_seguir.pack(side=tk.LEFT, padx=20)
    
    # Botón 'No'
    boton_no = tk.Button(ventana, text='No', command=lambda: respuesta_opcion('No'))
    boton_no.pack(side=tk.RIGHT, padx=20)
    
    resultado = None
    ventana.mainloop()
    
    return resultado


# DEPRECATED — cambiar_directorio ya no se usa. borrar_archivos usa rutas absolutas.
def cambiar_directorio(path):
    """Cambia al directorio especificado."""
    try:
        os.chdir(path)
        print(f'Cambio de directorio a: {path}')
    except FileNotFoundError:
        print(f'El directorio no se encuentra: {path}')
    except PermissionError:
        print(f'Permiso denegado para cambiar al directorio: {path}')
    except Exception as e:
        print(f'Error al cambiar de directorio: {e}')

def borrar_archivos(extension, path):
    archivos = glob.glob(os.path.join(path, f'*.{extension}'))
    for archivo in archivos:
        try:
            os.remove(archivo)
            print(f'Archivo borrado: {archivo}')
        except FileNotFoundError:
            print(f'Archivo no encontrado: {archivo}')
        except PermissionError:
            print(f'Permiso denegado para borrar el archivo: {archivo}')
        except Exception as e:
            print(f'Error al borrar el archivo {archivo}: {e}')
