README.md
# Análisis de Mortalidad en Colombia (2019) 🇨🇴

## Introducción del Proyecto
Este proyecto desarrolla una **aplicación web dinámica** utilizando **Python**, **Dash** y **Plotly** para analizar los datos de mortalidad en Colombia correspondientes al año 2019, provenientes del DANE (Estadísticas Vitales - EEVV). La herramienta ofrece informes gráficos interactivos que facilitan la interpretación de patrones demográficos y regionales de las defunciones.

## Objetivo
El objetivo principal es proporcionar una **herramienta accesible y completa** que permita la exploración visual intuitiva de los datos de mortalidad de 2019, facilitando la identificación de las principales causas de muerte, la distribución geográfica de los decesos, las diferencias por sexo y el impacto de la violencia en las principales ciudades.

## Estructura del Proyecto
nombre_del_proyecto/ ├── app.py # Lógica de la aplicación Dash y diseño del layout. ├── data_processing.py # Script para la carga, limpieza y fusión de los datos de Excel. ├── requirements.txt # Dependencias de Python. ├── Procfile # Configuración de despliegue para el PaaS. ├── README.md # Documentación del proyecto. └── data/ # Carpeta que contiene los archivos de datos originales. ├── NoFetal2019.xlsx ├── CodigosDeMuerte.xlsx ├── Divipola.xlsx └── colombia.geojson # Archivo GeoJSON utilizado para el mapa de coropletas.


## Requisitos
Para ejecutar la aplicación, se requiere tener **Python 3.7+** instalado y las siguientes librerías:

```bash
pip install -r requirements.txt
