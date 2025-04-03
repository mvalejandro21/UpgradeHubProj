import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
from matplotlib.dates import DateFormatter
import calendar

# 1. Cargar el archivo CSV con los datos limpios.
file_path = "data/marketingcampaigns_clean.csv"
df = pd.read_csv(file_path)

# 2. Configuración de estilo para las gráficas.
sns.set_style("whitegrid")

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# EJERCICIO 1
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def FrecuenciaYRoyPorCanal1():
    plt.figure(figsize=(10, 5))
    channel_counts = df["channel"].value_counts()
    sns.barplot(x=channel_counts.index, y=channel_counts.values, palette="viridis")

    plt.xlabel("Canal de Marketing", fontsize=12)
    plt.ylabel("Frecuencia de Uso", fontsize=12)
    plt.title("Frecuencia de Uso por Canal de Marketing", fontsize=14)
    plt.xticks(rotation=45)
    plt.show()

    # ----------------------------------------------------------------
    # Gráfico 2: Distribución del ROI por canal de marketing.
    # ----------------------------------------------------------------

    plt.figure(figsize=(10, 5))
    sns.boxplot(x="channel", y="roi", data=df, palette="muted")

    plt.xlabel("Canal de Marketing", fontsize=12)
    plt.ylabel("ROI", fontsize=12)
    plt.title("Distribución del ROI por Canal de Marketing", fontsize=14)
    plt.xticks(rotation=45)
    plt.show()



# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# EJERCICIO 2
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def ComparativaPorTipoDeCampaña2():
        
    # 2. Agrupar los datos por 'type' para calcular el promedio de ingresos y de tasa de conversión.
    # Esto nos permitirá comparar qué tipo de campaña genera más ingresos en promedio y cuál tiene mejor conversión.
    grouped = df.groupby("type").agg({
        "revenue": "mean",
        "conversion_rate": "mean"
    }).reset_index()

    # Configuración del estilo de las gráficas.
    sns.set_style("whitegrid")



    # ----------------------------------------------------------------
    # Gráfico de Barras: Ingresos y Tasa de Conversión Promedio por Tipo de Campaña 
    # ----------------------------------------------------------------
    # En este gráfico se crean dos subgráficos de barras:
    # - El primero muestra el promedio de ingresos generados por cada tipo de campaña.
    # - El segundo muestra la tasa de conversión promedio para cada tipo.
    # Esta visualización es ideal para comparar de forma directa y clara el rendimiento
    # financiero y la efectividad de cada tipo de campaña.
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Gráfico de ingresos promedio
    sns.barplot(x="type", y="revenue", data=grouped, palette="coolwarm", ax=axes[0])
    axes[0].set_title("Ingresos Promedio por Tipo de Campaña", fontsize=14)
    axes[0].set_xlabel("Tipo de Campaña", fontsize=12)
    axes[0].set_ylabel("Ingresos Promedio", fontsize=12)
    axes[0].tick_params(axis='x', rotation=45)

    # Gráfico de tasa de conversión promedio
    sns.barplot(x="type", y="conversion_rate", data=grouped, palette="coolwarm", ax=axes[1])
    axes[1].set_title("Tasa de Conversión Promedio por Tipo de Campaña", fontsize=14)
    axes[1].set_xlabel("Tipo de Campaña", fontsize=12)
    axes[1].set_ylabel("Tasa de Conversión Promedio", fontsize=12)
    axes[1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.show()



# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# EJERCICIO 3
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def AnalisisDeDistribucionesROI3():
    # 2. Configuración visual
    sns.set_style("whitegrid")
    plt.rcParams.update({'font.size': 12, 'figure.dpi': 120})

    # ------------------------------------------
    # Análisis de distribución del ROI
    # ------------------------------------------
    # Gráfico combinado histograma + boxplot
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    # Histograma con KDE
    sns.histplot(df['roi'], bins=30, kde=True, ax=ax[0], color='#2ecc71')
    ax[0].set_title('Distribución del ROI')
    ax[0].set_xlabel('ROI')
    ax[0].set_ylabel('Frecuencia')

    # Boxplot sin outliers extremos
    sns.boxplot(x=df['roi'], ax=ax[1], color='#3498db', showfliers=False)
    ax[1].set_title('Distribución del ROI (sin outliers)')
    ax[1].set_xlabel('ROI')

    plt.tight_layout()
    plt.show()

    # ------------------------------------------
    # Análisis de campañas de alto ROI (Top 20%)
    # ------------------------------------------
    high_roi = df[df['roi'] > df['roi'].quantile(0.8)]

    # Composición de canales en campañas exitosas
    plt.figure(figsize=(10, 6))
    (high_roi['channel'].value_counts(normalize=True)*100).plot(
        kind='bar', color='#f1c40f', edgecolor='black'
    )
    plt.title('Distribución de Canales en Top 20% ROI')
    plt.xlabel('Canal')
    plt.ylabel('Porcentaje (%)')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

    # ROI promedio por tipo de campaña
    plt.figure(figsize=(10, 6))
    df.groupby('type')['roi'].mean().sort_values().plot(
        kind='barh', color='#16a085', edgecolor='black'
    )
    plt.title('ROI Promedio por Tipo de Campaña')
    plt.xlabel('ROI Promedio')
    plt.ylabel('')
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.show()


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# EJERCICIO 4
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def EfectividadPorAudiencia():

    # ----------------------------------------------------------------
    # Configuración del estilo para las gráficas.
    sns.set_style("whitegrid")

    # ----------------------------------------------------------------
    # Visualización 1: Gráfico de Cajas Comparativo
    # ----------------------------------------------------------------
    # Este boxplot compara la tasa de conversión entre las audiencias B2B y B2C.
    # La visualización permite identificar la mediana, los cuartiles y la presencia de
    # posibles valores atípicos en cada grupo, facilitando la comparación de su distribución.
    plt.figure(figsize=(8, 6))
    sns.boxplot(x="target_audience", y="conversion_rate", data=df, palette="Set2")
    plt.title("Comparación de Tasa de Conversión: B2B vs B2C", fontsize=14)
    plt.xlabel("Tipo de Audiencia", fontsize=12)
    plt.ylabel("Tasa de Conversión", fontsize=12)
    plt.show()

    # ----------------------------------------------------------------
    # Visualización 2: Gráfico de Barras Agrupadas por Audiencia y Canal
    # ----------------------------------------------------------------
    # Aquí se calcula la tasa de conversión promedio por canal para cada audiencia (B2B y B2C).
    # Este gráfico de barras agrupadas permite observar si existen diferencias en la efectividad
    # según el canal utilizado, al segmentar por tipo de audiencia.
    grouped_channel = df.groupby(["target_audience", "channel"])["conversion_rate"].mean().reset_index()

    plt.figure(figsize=(10, 6))
    sns.barplot(x="channel", y="conversion_rate", hue="target_audience", data=grouped_channel, palette="Set1")
    plt.title("Tasa de Conversión Promedio por Canal y Audiencia", fontsize=14)
    plt.xlabel("Canal de Marketing", fontsize=12)
    plt.ylabel("Tasa de Conversión Promedio", fontsize=12)
    plt.xticks(rotation=45)
    plt.legend(title="Audiencia")
    plt.show()

    # ----------------------------------------------------------------
    # Visualización 3: Gráfico de Barras Agrupadas por Audiencia y Tipo de Campaña
    # ----------------------------------------------------------------
    # Este gráfico muestra la tasa de conversión promedio según el tipo de campaña, 
    # segmentada por audiencia (B2B y B2C). Permite analizar si la naturaleza de la campaña
    # (por ejemplo: email, social media, webinar, etc.) influye en la conversión en cada segmento.
    grouped_type = df.groupby(["target_audience", "type"])["conversion_rate"].mean().reset_index()

    plt.figure(figsize=(10, 6))
    sns.barplot(x="type", y="conversion_rate", hue="target_audience", data=grouped_type, palette="Set2")
    plt.title("Tasa de Conversión Promedio por Tipo de Campaña y Audiencia", fontsize=14)
    plt.xlabel("Tipo de Campaña", fontsize=12)
    plt.ylabel("Tasa de Conversión Promedio", fontsize=12)
    plt.xticks(rotation=45)
    plt.legend(title="Audiencia")
    plt.show()


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# EJERCICIO 5
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def CampanasRentables():


    # 1. Calcular beneficio neto y seleccionar top campañas
    df['net_profit'] = df['revenue'] - df['budget']
    top_campaigns = df.nlargest(10, 'net_profit').reset_index(drop=True)

    # 2. Visualización de top campañas
    plt.figure(figsize=(12, 6))
    sns.barplot(x='net_profit', y='campaign_name', data=top_campaigns, 
                palette='viridis', estimator=sum, ci=None)
    plt.title('Top 10 Campañas por Beneficio Neto', fontsize=16)
    plt.xlabel('Beneficio Neto (USD)', fontsize=12)
    plt.ylabel('')
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10, rotation=0)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    # ----------------------------------------------------------------
    # Análisis de correlación: Beneficio Neto vs otras métricas.
    # ----------------------------------------------------------------
    # Para determinar qué variables están asociadas al éxito, calculamos el coeficiente
    # de correlación de Pearson entre beneficio neto y cada una de las siguientes variables:
    #   - ROI
    #   - Tasa de Conversión
    #   - Presupuesto
    metrics = ['roi', 'conversion_rate', 'budget']
    
    
    # ----------------------------------------------------------------
    # Visualización 3: Gráficos de dispersión con línea de tendencia.
    # ----------------------------------------------------------------
    # Se crean scatter plots para visualizar la relación entre beneficio neto y cada variable,
    # añadiendo una línea de regresión para evidenciar la tendencia.
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    
    # Beneficio Neto vs ROI
    sns.regplot(x='roi', y='net_profit', data=top_campaigns, ax=axes[0],
                scatter_kws={'s': 100, 'alpha': 0.7}, line_kws={'color': 'red'})
    axes[0].set_title("Beneficio Neto vs ROI", fontsize=14)
    axes[0].set_xlabel("ROI", fontsize=12)
    axes[0].set_ylabel("Beneficio Neto (USD)", fontsize=12)
    
    # Beneficio Neto vs Tasa de Conversión
    sns.regplot(x='conversion_rate', y='net_profit', data=top_campaigns, ax=axes[1],
                scatter_kws={'s': 100, 'alpha': 0.7}, line_kws={'color': 'red'})
    axes[1].set_title("Beneficio Neto vs Tasa de Conversión", fontsize=14)
    axes[1].set_xlabel("Tasa de Conversión", fontsize=12)
    axes[1].set_ylabel("Beneficio Neto (USD)", fontsize=12)
    
    # Beneficio Neto vs Presupuesto
    sns.regplot(x='budget', y='net_profit', data=top_campaigns, ax=axes[2],
                scatter_kws={'s': 100, 'alpha': 0.7}, line_kws={'color': 'red'})
    axes[2].set_title("Beneficio Neto vs Presupuesto", fontsize=14)
    axes[2].set_xlabel("Presupuesto (USD)", fontsize=12)
    axes[2].set_ylabel("Beneficio Neto (USD)", fontsize=12)
    
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(x=top_campaigns['channel'], 
                        y=top_campaigns['type'], 
                        s=top_campaigns['net_profit'] / 1000,  # Escala del tamaño: ajustar según el rango de net_profit.
                        c=top_campaigns['net_profit'], 
                        cmap='viridis', 
                        alpha=0.7)

    plt.title("Correlación de las Mejores Campañas\ncon Canal y Tipo de Campaña", fontsize=16)
    plt.xlabel("Canal de Marketing", fontsize=12)
    plt.ylabel("Tipo de Campaña", fontsize=12)

    # Agregar barra de color para interpretar el beneficio neto.
    cbar = plt.colorbar(scatter)
    cbar.set_label("Beneficio Neto (USD)", fontsize=12)


    plt.tight_layout()
    plt.show()

        

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# EJERCICIO 6
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def RelacionPresupuestosIngresos():
    

    # Análisis de correlación
    corr, p_value = pearsonr(df["budget"], df["revenue"])

    # Gráfico 1: Dispersión general
    plt.figure(figsize=(10, 6))
    ax = sns.scatterplot(data=df, x="budget", y="revenue", hue="channel", 
                        palette="viridis", alpha=0.7, s=80)
    sns.regplot(data=df, x="budget", y="revenue", scatter=False, 
            color="red", line_kws={"linestyle":"--"})

    # Ajustar rangos y formato
    plt.xlim(0, 60000) 
    plt.ylim(0, 1000000)


    plt.title("Relación Presupuesto vs Ingresos (Rango ajustado)")
    plt.xlabel("Presupuesto")
    plt.ylabel("Ingresos")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.grid(alpha=0.3)
    plt.show()

    # Gráfico 2: Presupuestos altos (ajustado)
    high_budget = df[df["budget"] > 30000]  # Nuevo límite inferior

    plt.figure(figsize=(10, 6))
    ax = sns.scatterplot(data=high_budget, x="budget", y="revenue", 
                        hue="type", palette="Set2", s=80)

    # Ajustar formato y rango
    plt.xlim(30000, 60000)
    plt.ylim(0, 1000000)
  

    plt.title("Rendimientos en Presupuestos Altos (>$30k)")
    plt.xlabel("Presupuesto")
    plt.ylabel("Ingresos")
    plt.grid(alpha=0.3)
    plt.show()

    


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# EJERCICIO 7
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def CampanasAltoRendimiento():

    # Filtrar datos
    high_performers = df[
        (df['roi'] > 0.5) & 
        (df['revenue'] > 500000)
    ].sort_values('revenue', ascending=False).head(10)  # Top 10 por ingresos

    # Configurar figura
    plt.figure(figsize=(12, 6))
    ax = plt.gca()

    # Gráfico de barras para ingresos
    bars = plt.bar(
        high_performers['campaign_name'],
        high_performers['revenue'],
        color='skyblue',
        alpha=0.7,
        label='Ingresos'
    )

    # Gráfico de línea para ROI
    ax2 = ax.twinx()
    line = ax2.plot(
        high_performers['campaign_name'],
        high_performers['roi'],
        color='coral',
        marker='o',
        linewidth=2,
        label='ROI'
    )

    # Personalización
    plt.title('Top Campañas: Alto ROI e Ingresos', fontsize=14, pad=20)
    ax.set_ylabel('Ingresos (USD)', fontsize=12)
    ax2.set_ylabel('ROI', fontsize=12)
    ax.tick_params(axis='x', rotation=45, labelsize=10)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x/1000:.0f}K'))
    ax2.set_ylim(0, high_performers['roi'].max() + 0.2)

    # Añadir valores
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'${height/1000:.0f}K',
                ha='center', va='bottom', fontsize=8)

    for x, y in zip(high_performers['campaign_name'], high_performers['roi']):
        ax2.text(x, y + 0.05, f'{y:.2f}', 
                ha='center', va='bottom', fontsize=8, color='coral')

    # Leyenda combinada
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines + lines2, labels + labels2, loc='upper left')

    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    



#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#  EJERCICIO 8
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def AnalisisTemporal():

    # Convertir a datetime y extraer componentes temporales
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['month'] = df['start_date'].dt.month
    df['quarter'] = df['start_date'].dt.quarter
    df['year'] = df['start_date'].dt.year

    # Agrupar datos temporales
    monthly_perf = df.groupby(['year', 'month']).agg({
        'revenue': 'sum',
        'roi': 'mean',
        'conversion_rate': 'mean'
    }).reset_index()

 
    # ---------------------------------------------------------------
    # Gráfico 2: Heatmap Estacional por Tipo de Campaña
    # ---------------------------------------------------------------
    # Preparar datos para heatmap
    heatmap_data = df.groupby(['month', 'type']).agg({
        'conversion_rate': 'mean'
    }).unstack()

    plt.figure(figsize=(12, 6))
    sns.heatmap(
        heatmap_data['conversion_rate'],
        cmap='YlGnBu',
        annot=True,
        fmt=".1%",
        linewidths=.5,
        cbar_kws={'label': 'Tasa de Conversión'}
    )

    # Personalización
    plt.title('Rendimiento Estacional por Tipo de Campaña', fontsize=14)
    plt.xlabel('Tipo de Campaña')
    plt.ylabel('Mes')
    plt.yticks(
        ticks=range(12),
        labels=[calendar.month_abbr[i] for i in range(1,13)],
        rotation=0
    )
    plt.tight_layout()
    plt.show()


FrecuenciaYRoyPorCanal1()
#ComparativaPorTipoDeCampaña2()
#AnalisisDeDistribucionesROI3()
EfectividadPorAudiencia()
CampanasRentables()
RelacionPresupuestosIngresos()
CampanasAltoRendimiento()
AnalisisTemporal()