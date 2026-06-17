# Módulo: Procesamiento CSV

Tres módulos que transforman el HTML bruto en datos limpios y unificados.

---

## `csv_parser.py` — Conversión HTML → CSV

### Función pública

```python
convert_html_files_to_csv(html_directory, output_folder, Ns)
```

Procesa en lote todos los `.html` de `html_directory` y guarda un `.csv` por archivo en `output_folder`.

### Lógica interna

```python
convert_html_to_csv(html_content)
```

1. Usa BeautifulSoup para extraer el contenido del tag `<pre>` del HTML
2. Parsea el texto como JSON
3. Retorna la lista de registros y las claves del primer registro como headers

### Parámetro `Ns`

| Valor | Comportamiento |
|-------|----------------|
| `0` | Modo turnero: escritura directa del CSV |
| `1` | Modo comentarios: reemplaza `\n` por espacios dentro de los campos (los comentarios de texto libre pueden tener saltos de línea) |

### Output

Un CSV por cada HTML procesado, con el mismo nombre base. El header se extrae del primer registro JSON.

---

## `csv_stacker.py` — Fusión y clasificación

### Función pública

```python
merge_csv_files(csv_directory, output_folder, date, turnero_or_client)
```

### Lógica

1. Lee todos los `.csv` de `csv_directory` con `glob`
2. Concatena en un único `DataFrame` con `pandas`
3. Si `turnero_or_client == 'COMENTARIOS'`: aplica clasificación por regex (ver abajo)
4. Guarda como:
   - `CACs_{date}.csv` para turnero
   - `CACs_Comments_{date}.csv` para comentarios
5. Llama a `guardar_en_onelake()` si el tipo es `'TURNERO'`

### Clasificación de comentarios

Aplica regex sobre la columna de texto libre para asignar una de 14 categorías:

```
ALTA SERVICIO, BAJA DE SERVICIO, RECLAMO POR FACTURACION, RECLAMO POR CORTE,
TRAMITES VARIOS, INFORMACION, PAGO, CONEXION, CAMBIO DE TITULAR,
CONVENIO DE PAGO, MEDIDOR, SUBSIDIO, ATENCION COMERCIAL, OTRO
```

La categoría se agrega como nueva columna al DataFrame.

### Parámetros

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `csv_directory` | str | Carpeta con CSVs intermedios (folders 2 o 5) |
| `output_folder` | str | Carpeta de salida (folders 3 o 6) |
| `date` | str | Fecha o período (YYYY-MM-DD o YYYY-MM-DD-YYYY-MM-DD) |
| `turnero_or_client` | str | `'TURNERO'` o `'COMENTARIOS'` |

---

## `csv_process.py` — Limpieza de columnas de comentarios

### Función pública

```python
delete_columns_in_csv(folder_path)
```

### Lógica

1. Encuentra el CSV más reciente en `folder_path` (por fecha de modificación)
2. Elimina 15 columnas técnicas/de sistema que no son necesarias para el análisis:
   `Estado`, `Tramite`, `Id_Tramite_Relevado`, `Turno`, `Id_Estado`, `Agente`, `Color`, `Notifica_*` (4 cols), `Id_Agenda`, `N_Agenda`, `Id_Modalidad`, `N_Centro_Atencion`, `Id_Centro_Atencion`, `Sticker_SUAC`
3. Columnas que **se conservan**: `Interesado`, `Cuil_Interesado`, `Id_Turno`, `Fec_Solicitado`, `Datos_Particulares`, `Comentarios`
4. Sobreescribe el CSV con el resultado limpio
5. Llama a `guardar_en_onelake()` con tipo comentarios

### Cuándo se llama

Solo en el flujo de comentarios (opciones 2, 4, 7 del menú) después de `merge_csv_files`.
