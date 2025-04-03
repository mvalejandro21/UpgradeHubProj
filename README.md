Introducción
El objetivo principal de este proyecto es preparar y analizar un conjunto de datos de campañas de marketing. La limpieza de datos es esencial para asegurar que los análisis posteriores sean confiables. Una vez depurado el dataset, se realizan distintos ejercicios de exploración para identificar patrones, relaciones y oportunidades de mejora en las estrategias de marketing.

Limpieza y Validación de Datos
Problemas Detectados y Soluciones

Valores Numéricos con Decimales Incorrectos

Problema: Algunos decimales estaban escritos con comas en lugar de puntos.

Solución: Corrección manual de los archivos antes de la carga de datos para asegurar que se utilicen puntos como separadores decimales.



Errores en Formatos de Fechas

Problema: Fechas en formatos incorrectos o con valores nulos.

Solución: Conversión a formato datetime y eliminación de registros con fechas faltantes o inconsistentes (por ejemplo, donde end_date es anterior a start_date).



Valores Faltantes e Imputación

Columna budget:
Se imputa con la mediana agrupada por type y channel.

Columna type:
Se imputan utilizando la moda por channel y, si no es suficiente, se asigna 'Unknown'.

Columna conversion_rate:

Problema: Valores fuera del rango [0, 1] o faltantes.

Solución: Se recorta para mantener el rango [0, 1] y se imputa con la media en caso de faltar datos.

Variables categóricas (como target_audience, channel):
Se imputa con 'Unknown' para no afectar el análisis de las variables numéricas.

Variables de fechas:
Se eliminaron las filas con valores faltantes para evitar especulaciones sobre posibles errores y mantener la integridad cronológica.




Duplicados

Se identificaron y eliminaron registros duplicados usando drop_duplicates() para evitar sesgos en los análisis.












Exploración de Datos
Se desarrollaron diferentes ejercicios para extraer insights y evaluar el rendimiento de las campañas de marketing.




Ejercicio 1: Frecuencia y ROI por Canal
Objetivo:
Visualizar la frecuencia de uso de cada canal de marketing y analizar la distribución del ROI.

Visualizaciones:

Gráfico de barras de frecuencia de uso.

Boxplot de la distribución del ROI por canal.

Resultados:

Canal más usado: Promotion es el canal que se utiliza con mayor frecuencia.

Mejor ROI: El canal referral destaca por tener la media de ROI más alta.



![1 1](https://github.com/user-attachments/assets/5b660ab4-9825-4946-a801-e3f44e5ae836)
![1 2](https://github.com/user-attachments/assets/a1644559-1f8a-4b15-891f-77670d5a2ea8)



Ejercicio 2: Comparativa por Tipo de Campaña
Objetivo:
Comparar los ingresos y la tasa de conversión promedio por tipo de campaña.

Visualizaciones:

Gráficos de barras para ingresos y tasa de conversión.

Resultados:

Las campañas de social media y webinar son las que generan mayores ingresos y cuentan con la mejor tasa de conversión.


![2 1](https://github.com/user-attachments/assets/0dec90d9-04e5-49a3-862e-a69a7c0319d0)




Ejercicio 3: Distribución del ROI
Objetivo:
Analizar la distribución del ROI y explorar las campañas con ROI en el top 20%.

Visualizaciones:

Histograma con KDE y boxplot para el ROI.

Gráfico de barras para la distribución de canales en el top 20% de ROI.

Gráfico horizontal de ROI promedio por tipo de campaña.

Resultados:

La mayoría de las campañas tienen un ROI superior a 0.5.

Social media presenta el ROI más alto y el canal referral posee el mayor porcentaje de campañas con altos ROI.

![3 11](https://github.com/user-attachments/assets/21ee58a1-6699-4561-9a39-4a59b59f0b6b)

![3 22](https://github.com/user-attachments/assets/19763cdf-73bc-46d8-879e-16537aa3341e)

![3 33](https://github.com/user-attachments/assets/35de6c72-38c1-48f7-9937-ba4b35552b2f)



Ejercicio 4: Efectividad por Audiencia (B2B vs B2C)
Objetivo:
Evaluar la diferencia en la tasa de conversión entre audiencias B2B y B2C.

Visualizaciones:

Boxplot comparativo de la tasa de conversión.

Gráficos de barras agrupadas por canal y por tipo de campaña.

Resultados:

La tasa de conversión es, en promedio, mayor en campañas B2B.

Las campañas orgánicas (organic) funcionan mejor en B2B, mientras que las pagadas (paid) favorecen a B2C.

Según el tipo de campaña, B2B destaca en email y podcast, en social media las diferencias son menores, y en webinar B2C resulta superior.
![4 11](https://github.com/user-attachments/assets/3f14389f-d66f-4766-9923-d9f62bc26c69)
![4 22](https://github.com/user-attachments/assets/6fc17bbd-f02f-4a1e-b620-502aea9d09c9)
![4 33](https://github.com/user-attachments/assets/affbe3c5-2e5c-49f7-ac58-db01b294bca3)





Ejercicio 5: Campañas Rentables
Objetivo:
Identificar las campañas con mayor beneficio neto y analizar las variables asociadas al éxito.

Visualizaciones:

Gráfico de barras del top 10 de campañas por beneficio neto.

Análisis de correlación entre beneficio neto y métricas como ROI, tasa de conversión y presupuesto.

Gráficos de dispersión con líneas de tendencia.

Resultados:

Un ROI y una tasa de conversión altos están asociados con mayores ingresos.

Un presupuesto elevado no garantiza altos ingresos, lo que sugiere que campañas con presupuestos dirigidos a organic (enfocadas en B2B) tienen más casos de éxito, mientras que las pagadas son más efectivas en B2C.

![5 11](https://github.com/user-attachments/assets/c3a50a0b-c765-408c-b352-2e4f90d688a6)

![5 22](https://github.com/user-attachments/assets/8a79a2b9-ca57-40b9-a593-9d242ad6bebc)

![5 33](https://github.com/user-attachments/assets/87ab4662-3672-4e2f-8490-b1e308ae85ee)


Ejercicio 6: Relación entre Presupuesto e Ingresos
Objetivo:
Explorar la relación entre el presupuesto y los ingresos de las campañas.

Visualizaciones:

Se realizaron dos gráficos de dispersión: uno para todo el rango y otro para presupuestos altos (>$30k), con líneas de regresión.

Resultados:

Observación: Los datos no parecen significativos debido a la equidad en la dispersión de ambos gráficos, lo que indica que la relación entre presupuesto e ingresos no es tan marcada como se esperaba.

![6 11](https://github.com/user-attachments/assets/c07ce974-7671-44db-90c9-e117501f7657)


![6 22](https://github.com/user-attachments/assets/9662c5a5-6f62-4d59-b54a-0d329cebd7ef)



Ejercicio 7: Campañas de Alto Rendimiento
Objetivo:
Identificar campañas con alto rendimiento en términos de ROI e ingresos.

Visualizaciones:

Gráfico combinado de barras (para ingresos) y línea (para ROI).

Gráfico de dispersión relacionando canal y tipo de campaña con beneficio neto.

Resultados:

Se destacan tres campañas en particular:

Balanced Optimizing Software

Function Based LeadingEdge Budget and Management

Network Zero Administration Hardware

Estas campañas muestran un rendimiento superior, lo que sugiere que su combinación de estrategia, canal y tipo de campaña es especialmente efectiva.


![7 1](https://github.com/user-attachments/assets/c417c7fa-43cd-42da-94c8-9ed6d276db89)





Ejercicio 8: Análisis Temporal
Objetivo:
Evaluar la evolución de los ingresos, ROI y tasa de conversión a lo largo del tiempo, y detectar patrones estacionales.

Visualizaciones:

Se extrajeron componentes temporales (mes, trimestre, año) a partir de start_date y se agruparon los datos.

Gráficos de línea y un heatmap para analizar la evolución estacional.

Resultados:

Email: Se observa un patrón estacionario con un orden descendente de la tasa de conversión a medida que avanza el año.

Podcast: Se presentan altas cifras en invierno y principios de verano.

Social Media: Se destacan altos valores desde marzo hasta agosto.

Webinar: No se obtuvieron conclusiones claras sobre su comportamiento estacional.

![8 1](https://github.com/user-attachments/assets/ffa212dc-dfd8-4af5-b364-eae6aacbc34b)

