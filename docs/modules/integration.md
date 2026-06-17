# Módulo: Integración Cloud

Dos módulos para subir datos a Microsoft Fabric / SharePoint.

---

## `onelake.py` — Azure OneLake (Microsoft Fabric)

### Función pública

```python
guardar_en_onelake(cacs_or_comm, file_name)
```

### Lógica

1. Crea un `DataLakeServiceClient` usando `InteractiveBrowserCredential` (abre browser para MFA si el token no está cacheado)
2. Apunta al workspace `"Protelem - Premium"`
3. Según `cacs_or_comm`:
   - `'CACs'` → sube a `LH_CIDI.Lakehouse/Files/CACs/`
   - `'CACs_Comments'` → sube a `LH_CIDI.Lakehouse/Files/CACs_Comments/`
4. Sube el archivo `file_name`

### Cuándo se llama

- Desde `csv_stacker.py` al finalizar el merge de turnero
- Desde `csv_process.py` al finalizar la limpieza de comentarios

### Dependencias

```
azure-storage-filedatalake
azure-identity
```

---

## `sharepoint.py` — SharePoint vía Microsoft Graph API

### Función pública

```python
upload_file_to_sharepoint(username, password, site_name, base_path, nested_folder, local_folder)
```

### Lógica

1. Busca el archivo más reciente en `local_folder` (por fecha de modificación)
2. Obtiene un token de acceso con `InteractiveBrowserCredential`
3. Consulta la Graph API para obtener el `drive_id` del sitio SharePoint:
   ```
   GET https://graph.microsoft.com/v1.0/sites/{site_url}/drives
   ```
4. Sube el archivo vía PUT:
   ```
   PUT https://graph.microsoft.com/v1.0/drives/{drive_id}/root:/{nested_folder}/{filename}:/content
   ```
5. Retorna `True` si la subida fue exitosa

### Parámetros

| Parámetro | Ejemplo |
|-----------|---------|
| `site_name` | `'PROTELEM-INDICADORES'` |
| `base_path` | `'https://epeccba.sharepoint.com/'` |
| `nested_folder` | `'Documentos compartidos/m_actividad_turnero_cidi'` |
| `local_folder` | Ruta local de la carpeta con el CSV a subir |

### Cuándo se llama

- Opción 1 del menú: subida directa del archivo filtrado existente
- Opciones 6 y 7: después de procesar cada fecha
- Opción 2: si el usuario confirma subida de comentarios

### Nota histórica

El archivo contiene código comentado de una implementación anterior con la librería `shareplum`. Fue reemplazada por Graph API para soportar MFA.
