
import pandas as pd
import numpy as np

# --- 0. Constantes y Rutas ---
PATH_MOR = 'data/NoFetal2019.xlsx'
PATH_COD = 'data/CodigosDeMuerte.xlsx'
PATH_DIP = 'data/Divipola.xlsx'
OUTPUT_PATH = 'data/df_mortalidad_processed.csv'

# Definir el orden correcto para el histograma de edad
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

# Mapeo de Rango de Edad (GRUPO_EDAD1 a Categoría)
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
    if pd.isna(codigo) or codigo == 29:
        return 'Edad desconocida (Sin información)'
    for r, label in edad_map.items():
        if codigo in r:
            return label
    return 'Edad desconocida (Sin información)'

# --- 1. Cargar Datos ---
print("Cargando y procesando datos...")
try:
    df_mor = pd.read_excel(PATH_MOR)
    df_cod = pd.read_excel(PATH_COD)
    df_dip = pd.read_excel(PATH_DIP)
except FileNotFoundError as e:
    print(f"Error: No se encontró el archivo en la ruta especificada. {e}")
    exit()

# --- 2. Preparación y Estandarización de Claves DANE ---

# 2.1 Datos de Mortalidad (df_mor)
# Crear códigos DANE estandarizados (2 y 5 dígitos, con ceros iniciales)
df_mor['COD_DEPARTAMENTO'] = df_mor['COD_DEPARTAMENTO'].astype(str).str.zfill(2)
df_mor['COD_MUNICIPIO'] = df_mor['COD_MUNICIPIO'].astype(str).str.zfill(5)
# Renombrar la causa de muerte para la unión
df_mor.rename(columns={'COD_MUERTE': 'CAUSA_DEF'}, inplace=True) 

# 2.2 Códigos de Muerte (df_cod)
# Usaremos el código CIE-10 de tres caracteres como clave de unión (CAUSA_DEF)
df_cod.rename(columns={
    'Código de la CIE-10 tres caracteres': 'CAUSA_DEF',
    'Descripción de códigos mortalidad a tres caracteres': 'NOMBRE_CAUSA'
}, inplace=True)
# Asegurar que la clave de unión sea una cadena y esté en mayúsculas
df_cod['CAUSA_DEF'] = df_cod['CAUSA_DEF'].astype(str).str.upper()

# 2.3 Divipola (df_dip)
df_dip['COD_DEPARTAMENTO'] = df_dip['COD_DEPARTAMENTO'].astype(str).str.zfill(2)
df_dip['COD_MUNICIPIO'] = df_dip['COD_MUNICIPIO'].astype(str).str.zfill(5)


# --- 3. Fusión de DataFrames ---

# 3.1 Unir Mortalidad con Nombres de Causa de Muerte
df_merged = pd.merge(
    df_mor, 
    df_cod[['CAUSA_DEF', 'NOMBRE_CAUSA']], 
    on='CAUSA_DEF', 
    how='left'
)

# 3.2 Unir el resultado con Nombres de Localización (DIVIPOLA)
df_merged = pd.merge(
    df_merged,
    df_dip[['COD_DEPARTAMENTO', 'DEPARTAMENTO']].drop_duplicates(),
    on='COD_DEPARTAMENTO',
    how='left'
)
df_merged = pd.merge(
    df_merged,
    df_dip[['COD_MUNICIPIO', 'MUNICIPIO']].drop_duplicates(),
    on='COD_MUNICIPIO',
    how='left',
    suffixes=('_DEP', '_MUN')
)

# --- 4. Creación de Variables Categóricas Finales ---

# 4.1 Grupos de Edad
df_merged['GRUPO_EDAD_CAT'] = df_merged['GRUPO_EDAD1'].apply(map_edad)

# 4.2 Mes de Defunción
# Se asume que la columna 'MES' contiene el número del mes (1 a 12)
MESES = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
    7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
}
df_merged['MES_NOMBRE'] = df_merged['MES'].map(MESES)

# 4.3 Sexo
df_merged['SEXO_DESC'] = df_merged['SEXO'].map({1: 'Hombre', 2: 'Mujer', 9: 'Indeterminado'})


# --- 5. Exportar el DataFrame Final ---
df_final = df_merged.copy()

# Guardar el DataFrame procesado para la aplicación Dash
df_final.to_csv(OUTPUT_PATH, index=False)

print(f"✅ Proceso completado. Datos procesados guardados en: {OUTPUT_PATH}")
print("El script app.py debe cargar ahora este archivo CSV.")