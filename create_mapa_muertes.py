
def create_lineas_mes(df):
    # 1. Asegurar columna de fecha de defunción
    df['FECHA_DEF_DT'] = pd.to_datetime(df['FECHA_DEF'], format='%d/%m/%Y', errors='coerce')
    df['Mes'] = df['FECHA_DEF_DT'].dt.month_name(locale='es')
    
    # 2. Agrupar por Mes y contar
    df_mes = df.groupby('Mes').size().reset_index(name='Total Muertes')

    # 3. Ordenar correctamente los meses (importante para gráficos de línea)
    meses_orden = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                   'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    df_mes['Mes'] = pd.Categorical(df_mes['Mes'], categories=meses_orden, ordered=True)
    df_mes.sort_values('Mes', inplace=True)

    fig = px.line(
        df_mes,
        x='Mes',
        y='Total Muertes',
        title='Total de Muertes por Mes en Colombia',
        markers=True
    )
    return fig

# En app.py, reemplaza:
# dcc.Graph(id='lineas-muertes-mes', figure={}) 
# con:
# dcc.Graph(id='lineas-muertes-mes', figure=create_lineas_mes(df_final))