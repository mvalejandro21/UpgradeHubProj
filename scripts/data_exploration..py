import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

# 1. Cargar el archivo CSV con los datos limpios.
file_path = "data/marketingcampaigns_clean.csv"
df = pd.read_csv(file_path)

# 2. Configuración de estilo para las gráficas.
sns.set_style("whitegrid")

# ----------------------------------------------------------------
# Gráfico 1: Frecuencia de uso por canal de marketing.
# ----------------------------------------------------------------

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


# 2. Calcular el beneficio neto (net_profit) como la diferencia entre los ingresos (revenue) y el presupuesto (budget).
df['net_profit'] = df['revenue'] - df['budget']

# 3. Ordenar las campañas por beneficio neto de forma descendente y seleccionar las top 10.
top_campaigns = df.sort_values(by='net_profit', ascending=False).head(10)

# Mostrar la tabla con las top 10 campañas y sus métricas clave.
print("Top 10 Campañas por Beneficio Neto:")
print(top_campaigns[['campaign_name', 'net_profit', 'roi', 'conversion_rate', 'budget', 'revenue']])

# ----------------------------------------------------------------
# Visualización 1: Gráfico de Barras Horizontal de Beneficio Neto
# ----------------------------------------------------------------
# Se utiliza un gráfico de barras horizontal para visualizar y comparar el beneficio neto
# de las campañas más exitosas. Este gráfico permite identificar rápidamente cuál campaña
# genera el mayor beneficio.
plt.figure(figsize=(10, 6))
sns.barplot(x='net_profit', y='campaign_name', data=top_campaigns, palette='viridis')
plt.title("Top 10 Campañas por Beneficio Neto", fontsize=14)
plt.xlabel("Beneficio Neto", fontsize=12)
plt.ylabel("Nombre de Campaña", fontsize=12)
plt.show()

# ----------------------------------------------------------------
# Visualización 2: Gráficos Comparativos de Características Clave
# ----------------------------------------------------------------
# Se generan tres gráficos de barras (ROI, Tasa de Conversión y Presupuesto) para comparar
# estas métricas en las campañas con mayor beneficio neto. Esto permite identificar patrones
# comunes o factores que puedan estar asociados con el éxito.
fig, axes = plt.subplots(1, 3, figsize=(20, 6))

# Comparación de ROI
sns.barplot(x='roi', y='campaign_name', data=top_campaigns, palette='coolwarm', ax=axes[0])
axes[0].set_title("ROI de las Top Campañas", fontsize=14)
axes[0].set_xlabel("ROI", fontsize=12)
axes[0].set_ylabel("Campaña", fontsize=12)

# Comparación de Tasa de Conversión
sns.barplot(x='conversion_rate', y='campaign_name', data=top_campaigns, palette='coolwarm', ax=axes[1])
axes[1].set_title("Tasa de Conversión de las Top Campañas", fontsize=14)
axes[1].set_xlabel("Tasa de Conversión", fontsize=12)
axes[1].set_ylabel("")

# Comparación de Presupuesto
sns.barplot(x='budget', y='campaign_name', data=top_campaigns, palette='coolwarm', ax=axes[2])
axes[2].set_title("Presupuesto de las Top Campañas", fontsize=14)
axes[2].set_xlabel("Presupuesto", fontsize=12)
axes[2].set_ylabel("")

plt.tight_layout()
plt.show()






