import pandas as pd
import numpy as np

# ==================================================
# FUNCIONES DE CARGA Y LIMPIEZA DE DATOS
# ==================================================

def cargar_datos(ruta: str) -> pd.DataFrame:
    """
    Carga el dataset desde un archivo CSV y muestra un preview inicial
    """
    df = pd.read_csv(ruta, delimiter=',', quotechar='"')
    print("\n[INFO] Dataset cargado correctamente")
    print("Primeras 5 filas del dataset original:")
    print(df.head())
    return df

def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza transformaciones y limpieza completa del dataset
    """
    # Convertir a datetime manteniendo el tipo para procesamiento
    df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce')
    df['end_date'] = pd.to_datetime(df['end_date'], errors='coerce')
    
    # Eliminar filas con fechas faltantes
    filas_antes = df.shape[0]
    df.dropna(subset=['start_date', 'end_date'], inplace=True)
    print(f"\n[INFO] Filas eliminadas por fechas faltantes: {filas_antes - df.shape[0]}")

    df['channel'] = df['channel'].replace({'referal': 'referral'}, regex=False)    
    # Eliminar filas con end_date anterior a start_date
    mask_invalid = df['end_date'] < df['start_date']
    df = df[~mask_invalid]
    print(f"[INFO] Filas eliminadas por fechas inconsistentes: {mask_invalid.sum()}")
    
    # Resto de transformaciones (formato string para fechas)
    df['start_date'] = df['start_date'].dt.strftime('%Y-%m-%d')
    df['end_date'] = df['end_date'].dt.strftime('%Y-%m-%d')
    
    # Estandarización de formatos numéricos
    df['budget'] = pd.to_numeric(df['budget'], errors='coerce')
    df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')
    
    df['conversion_rate'] = df['conversion_rate'].clip(0, 1)
    mask = df["type"] == "B2B"

    df.loc[mask, "target_audience"] = "B2B"
    df.loc[mask, "type"] = pd.NA  # Marcar como faltante
    
    # Manejo de valores faltantes (resto de columnas)
    budget_median = df.groupby(['type', 'channel'])['budget'].transform('median')
    df['budget'] = df['budget'].fillna(budget_median)
    
    mode_by_channel = df.groupby('channel')['type'].transform(
        lambda x: x.mode()[0] if not x.mode().empty else 'Unknown')
    df['type'] = df['type'].fillna(mode_by_channel)
    df['type'] = df['type'].fillna('Unknown')
    
    df['conversion_rate'].fillna(df['conversion_rate'].mean(), inplace=True)

    numeric_cols = ['budget', 'revenue', 'roi', 'conversion_rate']
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())
    
    categorical_cols = ['type', 'target_audience', 'channel']
    for col in categorical_cols:
        df[col] = df[col].fillna('Unknown')

    print("\nValores faltantes después de la imputación:") 
    print(df.isnull().sum())
    
    filas_originales = df.shape[0]
    df.drop_duplicates(inplace=True)
    print(f"\n[INFO] Duplicados eliminados: {filas_originales - df.shape[0]} filas")

    
    return df


# ==================================================
# FUNCIONES DE VALIDACIÓN DE CALIDAD (ACTUALIZADAS)
# ==================================================

def validar_datos_crudos(df: pd.DataFrame) -> bool:
    """
    Realiza un análisis exploratorio detallado de los datos sin procesar
    """
    print("\n[ANÁLISIS EXPLORATORIO INICIAL]")
    problemas = {'criticos': [], 'advertencias': [], 'observaciones': []}

    # 1. Examinar estructura del dataset
    print("\n1. Muestra de datos:")
    print("Primeras 3 filas:\n", df.head(3))
    print("\nÚltimas 3 filas:\n", df.tail(3))
    print(f"\nDimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")

   

    # 3. Análisis de valores faltantes
    print("\n3. Valores faltantes:")
    missing = df.isna().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    print(pd.DataFrame({'Faltantes': missing, '%': missing_pct}))

    # 4. Estadísticas descriptivas
    print("\n4. Estadísticas numéricas:")
    numeric_cols = df.select_dtypes(include=np.number).columns
    if not numeric_cols.empty:
        stats = df[numeric_cols].describe(percentiles=[.01, .25, .5, .75, .99])
        print(stats)

    # 5. Análisis de variables categóricas
    print("\n5. Distribución categóricas:")
    cat_cols = ['type', 'target_audience', 'channel']
    for col in cat_cols:
        if col in df.columns:
            dist = df[col].value_counts(normalize=True).head(10)
            print(f"\n{col}:\n{dist}")

    # 6. Documentación de problemas
    print("\n6. Problemas detectados:")
    for severidad in ['criticos', 'advertencias', 'observaciones']:
        if problemas[severidad]:
            print(f"\n=== {severidad.upper()} ===")
            for i, problema in enumerate(problemas[severidad], 1):
                print(f"{i}. {problema}")

    return len(problemas['criticos']) == 0

def validar_datos_limpios(df: pd.DataFrame) -> bool:
    """
    Valida el estado final de los datos después de la limpieza
    """
    print("\n[VALIDACIÓN FINAL]")

    print(df['target_audience'].value_counts())

    checks = [
        
        ('Valores faltantes', df.isnull().sum().sum() == 0),
        
        ('Rangos lógicos', all([
            df['conversion_rate'].between(0, 1).all(),
            df['roi'].between(-1, 1).all()
        ])),
        
        ('Integridad temporal', (pd.to_datetime(df['end_date']) >= pd.to_datetime(df['start_date'])).all()),
        
        ('Duplicados', df.duplicated().sum() == 0)
    ]

    for nombre, resultado in checks:
        print(f"✓ {nombre}: {'OK' if resultado else 'Error'}")

    return all(resultado for _, resultado in checks)

# ==================================================
# FUNCIÓN DE EXPORTACIÓN
# ==================================================

def exportar_datos(df: pd.DataFrame, ruta_salida: str) -> None:
    """
    Exporta el DataFrame limpio a un nuevo archivo CSV
    """
    df.to_csv(ruta_salida, index=False)
    print(f"\n[INFO] Dataset limpio exportado: {ruta_salida}")

# ==================================================
# EJECUCIÓN PRINCIPAL
# ==================================================

if __name__ == "__main__":
    RUTA_ENTRADA = 'data/marketingcampaigns.csv'
    RUTA_SALIDA = 'data/marketingcampaigns_clean.csv'
    
    try:
        print("\n[ETAPA 1/3] Cargando datos...")
        dataset = cargar_datos(RUTA_ENTRADA)
        
        print("\n[ETAPA 2/3] Limpiando datos...")
        dataset_limpio = limpiar_datos(dataset)
        
        print("\n[ETAPA 3/3] Validando datos limpios...")
        if validar_datos_limpios(dataset_limpio):
            exportar_datos(dataset_limpio, RUTA_SALIDA)
            print("\n✅ Proceso completado exitosamente")
        else:
            print("\n❌ Problemas en datos limpios - Requiere revisión manual")
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")