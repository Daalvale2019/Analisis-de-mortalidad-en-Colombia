
import pandas as pd
import numpy as np

# --- Rutas de Archivos ---
PATH_MOR = 'data/NoFetal2019.xlsx'
PATH_COD = 'data/CodigosDeMuerte.xlsx'
PATH_DIP = 'data/Divipola.xlsx'

# --- 1. Cargar Datos ---
df_mor = pd.read_excel(PATH_MOR)
df_cod = pd.read_excel(PATH_COD)
df_dip = pd.read_excel(PATH_DIP)

# --- 2. Limpieza y Creación de Claves ---

# 2.1 Limpieza de Divipola para Departamentos y Municipios
df_dip['Departamento_DANE'] = df_dip['Código Departamento'].astype(str).str.zfill(2)
df_dip['Municipio_DANE'] = df_dip['Código Municipio'].astype(str).str.zfill(5)

# 2.2 Limpieza de Códigos de Muerte
# Se asume que la columna 'CODIGO' es la clave de unión
df_cod.rename(columns={'CODIGO': 'CAUSA_DEF'}, inplace=True)

# 2.3 Creación de Códigos DANE en Datos de Mortalidad (para unión con Divipola)
# Crear código de municipio y departamento (COL_MPIO es el código DANE del municipio)
df_mor['Municipio_DANE'] = df_mor['COL_MPIO'].astype(str).str.zfill(5)
df_mor['Departamento_DANE'] = df_mor['Municipio_DANE'].str[:2]

# --- 3. Fusión de DataFrames ---

# 3.1 Unir Mortalidad con Nombres de Causa de Muerte
df_merged = pd.merge(df_mor, df_cod[['CAUSA_DEF', 'NOMBRE_CAUSA']], on='CAUSA_DEF', how='left')

# 3.2 Unir Mortalidad con Nombres de Localización
# Unir por Municipio
df_merged = pd.merge(
    df_merged,
    df_dip[['Municipio_DANE', 'Nombre Municipio']],
    on='Municipio_DANE',
    how='left'
)
# Unir por Departamento
df_merged = pd.merge(
    df_merged,
    df_dip[['Departamento_DANE', 'Nombre Departamento']].drop_duplicates(),
    on='Departamento_DANE',
    how='left'
)

# --- 4. Preparación de Variables Categóricas y Rangos de Edad ---

# 4.1 Mapeo de Rango de Edad (GRUPO_EDAD1 a Categoría)
edad_map = {
    range(0, 5): 'Mortalidad neonatal (Menor de 1 mes)',
    range(5, 7): 'Mortalidad infantil (1 a 11 meses)',
    range(7, 9): 'Primera infancia (1 a 4 años)',
    range(9, 11): 'Niñez (5 a 14 años)',
    range(11, 12): 'Adolescencia (15 a 19 años)',
    range(12, 14): 'Juventud (20 a 29 años)',
    range(14, 17): 'Adultez temprana (30 a 44 años)',
    range(17, 20): 'Adultez intermedia (45 a 59 años)',
    range(20, 25): 'Vejez (60 a 84 años)',
    range(25, 29): 'Longevidad / Centenarios (85 a 100+ años)',
    range(29, 30): 'Edad desconocida (Sin información)'
}

def map_edad(codigo):
    if pd.isna(codigo):
        return 'Edad desconocida (Sin información)'
    for r, label in edad_map.items():
        if codigo in r:
            return label
    return 'Edad desconocida (Sin información)'

df_merged['GRUPO_EDAD_CAT'] = df_merged['GRUPO_EDAD1'].apply(map_edad)

# Definir el orden correcto para el histograma
EDAD_ORDEN = [
    'Mortalidad neonatal (Menor de 1 mes)',
    'Mortalidad infantil (1 a 11 meses)',
    'Primera infancia (1 a 4 años)',
    'Niñez (5 a 14 años)',
    'Adolescencia (15 a 19 años)',
    'Juventud (20 a 29 años)',
    'Adultez temprana (30 a 44 años)',
    'Adultez intermedia (45 a 59 años)',
    'Vejez (60 a 84 años)',
    'Longevidad / Centenarios (85 a 100+ años)',
    'Edad desconocida (Sin información)'
]

# 4.2 Mapeo de Sexo
df_merged['SEXO_DESC'] = df_merged['SEXO'].map({1: 'Hombre', 2: 'Mujer', 9: 'Indeterminado'})

# Exportar el DataFrame final para usarlo en la app
df_final = df_merged.copy()

print("Datos de Mortalidad de Colombia 2019 listos para Dash.")