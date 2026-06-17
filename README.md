# CIDI Scrapper

Scrapper web que automatiza la descarga diaria de datos de **turnero y comentarios** de los Centros de Atención Comercial (CACs) de EPEC desde el portal CIDI (Córdoba Digital), y los sube a Microsoft Fabric OneLake / SharePoint.

## Documentación

- [Visión general y menú](docs/README.md)
- [Arquitectura y flujo de datos](docs/architecture.md)
- [Guía de instalación](docs/setup.md)
- [Centros de Atención Comercial (45 CACs)](docs/centros_de_atencion.md)
- [Módulos: Scrapers](docs/modules/scrapers.md) · [Procesamiento](docs/modules/processing.md) · [Integración cloud](docs/modules/integration.md) · [Utilidades](docs/modules/utilities.md)
- [Problemas conocidos y TODOs](docs/known_issues.md)

## Inicio rápido

```bash
# 1. Instalar dependencias
pip install selenium beautifulsoup4 pandas azure-storage-filedatalake azure-identity requests colorama

# 2. Copiar y completar los archivos de configuración
cp paths.example.txt paths.txt
cp cidi_user_key.example.txt cidi_user_key.txt
cp shpt_user_key.example.txt shpt_user_key.txt

# 3. Editar los archivos copiados con los valores reales

# 4. Ejecutar
python cidi_scrapper.py
```

Ver [docs/setup.md](docs/setup.md) para instrucciones completas, incluyendo ChromeDriver.

## Estructura del proyecto

```
cidi/
├── cidi_scrapper.py          ← Punto de entrada
├── docs/                     ← Documentación
├── 1_scrapped_html/          ← Pipeline (datos temporales, no versionados)
├── 2_scrapped_csv/
├── 3_filtered_data/          ← Output de turnero
├── 4_comments_scrapped_html/
├── 5_comments_scrapped_csv/
└── 6_comments_filtered_data/ ← Output de comentarios
```

> Los archivos `paths.txt`, `cidi_user_key.txt` y `shpt_user_key.txt` contienen credenciales y **no están versionados**. Usar los `.example.txt` como plantilla.
