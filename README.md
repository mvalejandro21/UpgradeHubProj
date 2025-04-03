Documentación del Proyecto de Limpieza de Datos

Introducción

Este proyecto consiste en la limpieza y validación de un conjunto de datos relacionado con campañas de marketing. Antes de poder analizar los datos, es necesario corregir errores en la estructura, valores inconsistentes y datos faltantes. También se realizaron ajustes manuales, como cambiar los decimales que estaban separados por comas a un formato correcto con puntos.

Problemas Encontrados y Soluciones Aplicadas

Errores en Formatos de Fechas

Problema: Algunas fechas estaban en formatos incorrectos o contenían valores nulos.

Solución: Se convirtieron a formato datetime y se eliminaron las filas donde faltaban datos en start_date o end_date. Además, se eliminaron registros donde end_date era anterior a start_date para mantener coherencia temporal.

Valores Faltantes y Estrategia de Imputación

Para manejar los valores faltantes, se utilizaron diferentes estrategias según el tipo de dato:

Columna budget: Se imputa con la mediana agrupada por type y channel para mantener una estimación razonable de los presupuestos dentro de cada categoría.

Columna type: Se imputan los valores faltantes utilizando la moda por channel. Si no hay una moda clara, se asigna 'Unknown'.

Columna conversion_rate:

Problema Detectado: Algunos valores estaban fuera del rango esperado (0 a 1) o eran nulos.

Solución Aplicada: Se ajustaron los valores fuera del rango para que se mantengan entre 0 y 1. Además, los valores faltantes se imputaron con la media de la columna para no afectar el análisis.

Variables categóricas (type, target_audience, channel): Se imputaron con 'Unknown' para evitar afectar el análisis de las variables numéricas.

Variables de fechas (start_date, end_date): Se eliminaron las filas con valores faltantes para no especular con posibles fechas erróneas y evitar problemas en los análisis de cronología.

Duplicados

Se identificaron y eliminaron registros duplicados para evitar sesgos en los análisis.

Validación de Datos

Después de la limpieza, se realizaron validaciones para asegurar la calidad del dataset. Se verificó que no hubiera valores faltantes, que los rangos fueran lógicos y que no existieran inconsistencias en las fechas.

