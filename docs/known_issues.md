# Problemas conocidos y TODOs

---

## Bugs activos

### BUG-01 — Ambos botones del popup dicen "Si"
- **Archivo:** [file_destructor.py](../file_destructor.py)
- **Función:** `mostrar_popup()`
- **Descripción:** El popup Tkinter tiene dos botones pero ambos están etiquetados como "Si". El botón de "No" no existe. La función está actualmente comentada en el main, así que no tiene impacto operativo, pero si se reactiva fallará.
- **Fix:** Cambiar el label del segundo botón a "No" y asegurarse que retorne `False`.

### BUG-02 — Índices de extensiones intercambiados en `cidi_scrapper.py`
- **Archivo:** [cidi_scrapper.py](../cidi_scrapper.py) líneas 42-48
- **Descripción:** El diccionario `extensiones` asocia `'html'` con `deleting_paths_csv` y `'csv'` con `deleting_paths_html`. Los nombres de las variables sugieren que están al revés.
- **Impacto:** Bajo — el resultado final (limpiar carpetas 2/3 y 5/6) puede ser el correcto de todas formas si las rutas en paths.txt están en el orden esperado, pero el código es confuso.
- **Fix:** Revisar la lógica o al menos renombrar las variables para que sean claras.

---

## Problemas de seguridad

### SEC-01 — Token de Telegram hardcodeado
- **Archivo:** [tx.py](../tx.py) líneas 5-6
- **Descripción:** El token del bot de Telegram y el chat ID están escritos directamente en el código fuente.
- **Riesgo:** Si el código se sube a un repositorio público o compartido, las credenciales quedan expuestas. Cualquiera con el token puede enviar mensajes en nombre del bot.
- **Fix recomendado:** Mover a variables de entorno o a un archivo de credenciales separado (con el mismo mecanismo que `cidi_user_key.txt`).

### SEC-02 — Credenciales en texto plano
- **Archivos:** `cidi_user_key.txt`, `shpt_user_key.txt`
- **Descripción:** Las contraseñas se almacenan como texto plano en archivos `.txt`.
- **Riesgo:** Si el directorio del proyecto es accesible por otros usuarios o si se sube a un repositorio, las contraseñas quedan expuestas.
- **Fix recomendado:** Usar variables de entorno o el gestor de credenciales del sistema operativo (`keyring` en Python).
- **Mitigación mínima:** Asegurarse de que los archivos no están incluidos en ningún sistema de control de versiones.

---

## Hardcodeos problemáticos

### HARD-01 — Ruta de ChromeDriver específica del usuario
- **Archivos:** [turnero_scrapper.py](../turnero_scrapper.py), [client_info_scrapper.py](../client_info_scrapper.py)
- **Descripción:** La ruta `D:/Usuarios/mdelgadillo/Documents/chromeBrowser/chromedriver-win64/chromedriver.exe` está hardcodeada.
- **Impacto:** El proyecto no funciona en otra máquina sin modificar el código.
- **Fix recomendado:** Mover la ruta a `paths.txt` (agregar línea 9) o a una variable de configuración.

### HARD-02 — Timeouts de Selenium hardcodeados
- **Archivos:** scrapers
- **Descripción:** Los tiempos de espera (240s turnero, 120s comentarios) están escritos directamente en el código.
- **Impacto:** Bajo. Pero si el portal CIDI se vuelve más lento o rápido, hay que cambiar el código.

---

## Deuda técnica

### TECH-01 — Duplicación entre scrapers
- **Archivos:** [turnero_scrapper.py](../turnero_scrapper.py), [client_info_scrapper.py](../client_info_scrapper.py)
- **Descripción:** ~80% del código de los scrapers es idéntico. Solo difieren en el endpoint, el timeout y el sufijo del nombre de archivo.
- **Fix sugerido:** Extraer la lógica común a una función base y parametrizar las diferencias.

### TECH-02 — Sin sistema de logging
- **Descripción:** El sistema usa `print()` para todo feedback. No hay logs persistentes ni niveles de severidad.
- **Impacto:** Difícil diagnosticar problemas post-ejecución.
- **Fix sugerido:** Integrar el módulo `logging` de Python con output a archivo.

### TECH-03 — Sin docstrings ni type hints
- **Descripción:** Ninguna función tiene docstrings ni anotaciones de tipos.
- **Impacto:** Bajo si el código no crece, pero dificulta mantenimiento.

### TECH-04 — `pruebasharepoint.py` eliminado
- Contenía solo código comentado. Fue removido en la limpieza del 2026-06-17.

---

## TODOs del código fuente

Extraídos de comentarios en `cidi_scrapper.py`:

- Agregar CAC **GENERAL CABRERA** (no está disponible en CIDI a 12/8/25)
- Agregar CAC **PASCANAS** (no está disponible en CIDI a 12/8/25)
- Mejorar el selector de fechas para el historial (opciones 6 y 7)
- Explotar mejor el concepto "desde/hasta" para evitar ingresar fechas una a una

---

## Archivos grandes en el proyecto

| Archivo | Tamaño | Ubicación | Notas |
|---------|--------|-----------|-------|
| `DB_CACs_MANUALES_HISTORICO.csv` | ~45.6 MB | `data/` | Datos históricos de referencia. Movido de raíz el 2026-06-17. Verificar si ya está cargado en OneLake y si se puede eliminar localmente. |
