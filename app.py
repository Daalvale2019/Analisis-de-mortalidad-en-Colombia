
# Importar el DataFrame preprocesado
# Asume que data_processing.py se ha ejecutado y tienes el df_final disponible,
# o idealmente, guárdalo y cárgalo aquí (e.g., df_final.to_csv('data/df_final.csv')).
# Por simplicidad, se importa la variable si se ejecuta en el mismo entorno.
from data_processing import df_final, EDAD_ORDEN
import dash
from dash import dcc, html, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
# Necesitarás 'pip install dash pandas plotly gunicorn'

# Inicializar la aplicación Dash
app = dash.Dash(__name__)
server = app.server # Necesario para el despliegue en PaaS

# --- Funciones para Generar Gráficos Plotly ---

# 1. Mapa: Distribución total de muertes por departamento
def create_mapa_muertes(df):
    # Agrupar por departamento y contar
    df_map = df.groupby(['Departamento_DANE', 'Nombre Departamento']).size().reset_index(name='Total Muertes')
    
    # NOTA: Para un mapa de coropletas preciso de Colombia (departamentos),
    # necesitarás un archivo GeoJSON de Colombia (e.g., colombia_deptos.geojson)
    # y mapear por el código DANE. Sin el GeoJSON, se usa un mapa de puntos.

    # Usaremos el mapa de puntos (scatter_mapbox) como alternativa si no hay GeoJSON
    # NOTA: La latitud y longitud no están en los datos originales, esta es una aproximación:
    # Si no tienes coordenadas de centroides, este gráfico fallará o será inexacto.
    
    # Para la entrega, la MEJOR opción es buscar o crear un GeoJSON de departamentos DANE.
    # Con GeoJSON:
    # fig = px.choropleth_mapbox(
    #     df_map, 
    #     geojson=geojson_data, 
    #     locations='Departamento_DANE', 
    #     featureidkey='properties.DANE_CODE',
    #     color='Total Muertes',
    #     # ... otros parámetros ...
    # )
    
    # Como alternativa simple (para demostrar la lógica):
    fig = px.bar(
        df_map.sort_values(by='Total Muertes', ascending=False),
        x='Nombre Departamento',
        y='Total Muertes',
        title='Distribución Total de Muertes por Departamento (Barra Sustituta)',
        height=400
    )
    return fig

# 6. Gráfico de Barras Apiladas: Comparación del total de muertes por sexo en cada departamento
def create_barras_sexo_depto(df):
    # Agrupar por departamento y sexo
    df_sexo_depto = df.groupby(['Nombre Departamento', 'SEXO_DESC']).size().reset_index(name='Total Muertes')

    fig = px.bar(
        df_sexo_depto,
        x='Nombre Departamento',
        y='Total Muertes',
        color='SEXO_DESC',
        barmode='stack', # Barras apiladas
        title='Total de Muertes por Sexo y Departamento',
        labels={'Total Muertes': 'Total de Muertes', 'Nombre Departamento': 'Departamento', 'SEXO_DESC': 'Sexo'},
        hover_data={'Total Muertes': True}
    )
    fig.update_layout(xaxis={'categoryorder': 'total descending'})
    return fig

# --- Layout de la Aplicación Dash ---

app.layout = html.Div(children=[
    html.H1(children='Análisis de Mortalidad en Colombia 2019', style={'textAlign': 'center', 'color': '#1f2d56'}),
    html.P(children='Aplicación web dinámica desarrollada con Plotly y Dash para la exploración visual de datos de mortalidad del DANE.', style={'textAlign': 'center', 'marginBottom': '30px'}),

    # Fila 1: Mapa (o Barra Sustituta) y Gráfico de Líneas
    html.Div(className='row', style={'display': 'flex'}, children=[
        # Mapa (o Barra Sustituta)
        html.Div(style={'width': '50%', 'padding': '10px'}, children=[
            dcc.Graph(
                id='mapa-muertes-depto',
                figure=create_mapa_muertes(df_final)
            )
        ]),
        # Gráfico de Líneas (Aquí iría la función create_lineas_mes)
        html.Div(style={'width': '50%', 'padding': '10px'}, children=[
            html.H3("Gráfico de Líneas: Muertes por Mes", style={'textAlign': 'center'}),
            dcc.Graph(id='lineas-muertes-mes', figure={}) # Pendiente de implementación
        ]),
    ]),

    # Fila 2: Gráfico de Barras Violencia y Gráfico Circular
    html.Div(className='row', style={'display': 'flex'}, children=[
        # Gráfico de Barras (Ciudades más violentas)
        html.Div(style={'width': '50%', 'padding': '10px'}, children=[
            html.H3("Gráfico de Barras: 5 Ciudades más Violentas", style={'textAlign': 'center'}),
            dcc.Graph(id='barras-violencia', figure={}) # Pendiente de implementación
        ]),
        # Gráfico Circular (10 Ciudades con menor mortalidad)
        html.Div(style={'width': '50%', 'padding': '10px'}, children=[
            html.H3("Gráfico Circular: 10 Ciudades con Menor Mortalidad", style={'textAlign': 'center'}),
            dcc.Graph(id='circular-menor-mortalidad', figure={}) # Pendiente de implementación
        ]),
    ]),

    # Fila 3: Tabla (10 Principales Causas)
    html.Div(style={'width': '100%', 'padding': '10px'}, children=[
        html.H2('Tabla: 10 Principales Causas de Muerte', style={'textAlign': 'center'}),
        # dash_table.DataTable iría aquí (Pendiente de implementación)
    ]),

    # Fila 4: Barras Apiladas por Sexo/Depto e Histograma de Edad
    html.Div(className='row', style={'display': 'flex'}, children=[
        # Barras Apiladas (Sexo vs Departamento)
        html.Div(style={'width': '50%', 'padding': '10px'}, children=[
            dcc.Graph(
                id='barras-sexo-depto',
                figure=create_barras_sexo_depto(df_final)
            )
        ]),
        # Histograma (Grupos de Edad)
        html.Div(style={'width': '50%', 'padding': '10px'}, children=[
            html.H3("Histograma: Distribución de Muertes por Grupo de Edad", style={'textAlign': 'center'}),
            dcc.Graph(id='histograma-edad', figure={}) # Pendiente de implementación
        ]),
    ]),
])

if __name__ == '__main__':
    # Para ejecución local, usa debug=True. Para despliegue, usa gunicorn/waitress.
    app.run_server(debug=True, port=8050)