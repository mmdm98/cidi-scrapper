# Módulo: Utilidades

Cuatro módulos de soporte que no forman parte del pipeline de datos.

---

## `credentials.py` — Lectura de credenciales y rutas

### Funciones

```python
read_credentials(file_path) -> (str, str)
```
Lee un archivo de 2 líneas y retorna `(línea1, línea2)`. Usado para archivos de credenciales (CUIL + contraseña).

```python
read_paths_from_file(file_path) -> list[str]
```
Lee todas las líneas del archivo `paths.txt` y retorna una lista. El main verifica que tenga exactamente 8 elementos.

### Consideración

No tiene manejo de errores de encoding. Si el archivo tiene BOM u otro encoding, puede fallar.

---

## `menu.py` — Interfaz de menú CLI

### Función

```python
menu(opcion)
```

Imprime el menú formateado con el logo ASCII de EPEC y las opciones disponibles. Usa `colorama` para color en la terminal.

Las opciones del menú son:

```
[0] Borrar todo
[1] Upload to SharePoint
[2] Download Data (today - 1)
[3] Download Data (custom date)
[4] Download Comment Data (custom date)
[5] Exit
[6] DEVS - custom dates array
[7] DEVS 2nd - desde hasta
```

El parámetro `opcion` no se usa actualmente (preparado para futura extensión del menú).

---

## `file_destructor.py` — Limpieza de archivos temporales

### Función principal

```python
borrar_archivos(extension, path)
```

Cambia al directorio `path` y elimina todos los archivos con la `extension` dada (sin el punto).

Maneja `FileNotFoundError` y `PermissionError` silenciosamente.

### Cuándo se llama

Al inicio de cada ejecución de `cidi_scrapper.py`, limpia las carpetas intermedias:
- Elimina `.html` de las carpetas de HTML bruto (1 y 4)
- Elimina `.csv` de las carpetas de CSV intermedio (2 y 5) 
  - Nota: los índices en `deleting_paths_csv` y `deleting_paths_html` están intercambiados en el código (ver [known_issues.md](../known_issues.md))

### Función auxiliar

```python
mostrar_popup(titulo, mensaje) -> bool
```

Muestra un popup Tkinter con dos botones. Actualmente ambos botones dicen "Si" (bug conocido). La función está comentada en el main y no se usa.

---

## `tx.py` — Notificaciones por Telegram

### Función principal

```python
alerta_error(mensaje, parse_mode="Markdown")
```

Envía un mensaje de texto al bot de Telegram configurado. Usado para notificar errores durante el scrapping.

### Funciones adicionales

```python
recibir_mensajes()
```
Polling de mensajes entrantes. No está en uso actualmente.

```python
text_analysis(mensaje)
```
Parsea texto recibido por Telegram para extraer una fecha o número. No está en uso actualmente.

### Configuración

El token del bot y el chat ID están hardcodeados en las primeras líneas del archivo. Ver [known_issues.md](../known_issues.md) para la implicación de seguridad.
