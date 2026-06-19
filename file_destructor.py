import os
import glob
import time
import logging
import tkinter as tk

logger = logging.getLogger(__name__)


def mostrar_popup(titulo, mensaje):
    """Muestra un pop-up con dos botones personalizados y devuelve la opción seleccionada."""
    def respuesta_opcion(opcion):
        nonlocal resultado
        resultado = opcion
        ventana.destroy()

    ventana = tk.Tk()
    ventana.title(titulo)

    ventana.geometry('300x150')

    ventana.update_idletasks()
    width = ventana.winfo_width()
    height = ventana.winfo_height()
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    ventana.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    etiqueta = tk.Label(ventana, text=mensaje)
    etiqueta.pack(padx=20, pady=10)

    boton_seguir = tk.Button(ventana, text='Si', command=lambda: respuesta_opcion('Si'))
    boton_seguir.pack(side=tk.LEFT, padx=20)

    boton_no = tk.Button(ventana, text='No', command=lambda: respuesta_opcion('No'))
    boton_no.pack(side=tk.RIGHT, padx=20)

    resultado = None
    ventana.mainloop()

    return resultado


# DEPRECATED — cambiar_directorio ya no se usa. borrar_archivos usa rutas absolutas.
def cambiar_directorio(path):
    try:
        os.chdir(path)
        logger.info('Cambio de directorio a: %s', path)
    except FileNotFoundError:
        logger.error('El directorio no se encuentra: %s', path)
    except PermissionError:
        logger.error('Permiso denegado para cambiar al directorio: %s', path)
    except Exception as e:
        logger.error('Error al cambiar de directorio: %s', e)


def borrar_archivos(extension, path):
    archivos = glob.glob(os.path.join(path, f'*.{extension}'))
    for archivo in archivos:
        try:
            os.remove(archivo)
            logger.debug('Archivo borrado: %s', archivo)
        except FileNotFoundError:
            logger.warning('Archivo no encontrado: %s', archivo)
        except PermissionError:
            logger.error('Permiso denegado para borrar el archivo: %s', archivo)
        except Exception as e:
            logger.error('Error al borrar el archivo %s: %s', archivo, e)
