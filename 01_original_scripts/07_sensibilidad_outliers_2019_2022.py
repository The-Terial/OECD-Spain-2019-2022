"""
Script 07: Análisis de Sensibilidad y Outliers por año (2019-2022)
Paper 4 - Chile vs OECD-España
Método: Q3 + 3×IQR y filtro ≤60 días
Autor: José Rodríguez López
Fecha: 2026-06-23
"""

import pandas as pd
import numpy as np
from pathlib import Path

# =============================================================================
# CONFIGURACIÓN
# =============================================================================
RUTA_BASE = Path("C:/Users/joser/Documents/DOCTORADO_2026/P4_Spain_vs_Chile")
RUTA_DATOS = RUTA_BASE / "3_resultados/datos_circulatorio_filtrados_2019_2022.csv"
RUTA_SALIDA_TABLAS = RUTA_BASE / "3_resultados/tablas"
RUTA_SALIDA_TABLAS.mkdir(parents=True, exist_ok=True)

oecd_espana = {2019: 9.1, 2020: 8.6, 2021: 8.5, 2022: 8.9}

print("=" * 70)
print("ANÁLISIS DE SENSIBILIDAD Y OUTLIERS (2019-2022)")
print("(Método Q3 + 3×IQR)")
print("=" * 70)

# =============================================================================
# 1. CARGA DE DATOS
# =============================================================================
df = pd.read_csv(RUTA_DATOS, encoding='utf-8')
anio_col = 'aÃ±o' if 'aÃ±o' in df.columns else 'año'
df[anio_col] = pd.to_numeric(df[anio_col], errors='coerce')

# =============================================================================
# 2. ANÁLISIS DE OUTLIERS POR AÑO (3×IQR)
# =============================================================================
print(f"\n📊 DISTRIBUCIÓN DE ESTADÍAS POR AÑO (con límite 3×IQR):")
print("-" * 60)

resultados = []
for año in [2019, 2020, 2021, 2022]:
    df_año = df[df[anio_col] == año]
    media = df_año['dias_cama'].mean()
    mediana = df_año['dias_cama'].median()
    maximo = df_año['dias_cama'].max()
    Q1 = df_año['dias_cama'].quantile(0.25)
    Q3 = df_año['dias_cama'].quantile(0.75)
    IQR = Q3 - Q1
    limite_superior = Q3 + 3 * IQR
    outliers = df_año[df_año['dias_cama'] > limite_superior]
    pct_outliers = len(outliers) / len(df_año) * 100

    print(f"\n   {int(año)}:")
    print(f"      Media: {media:.1f} días")
    print(f"      Mediana: {mediana:.1f} días")
    print(f"      Q3 = {Q3:.1f}, IQR = {IQR:.1f}")
    print(f"      Límite 3×IQR = {limite_superior:.1f} días")
    print(f"      Máximo: {maximo:.1f} días")
    print(f"      Outliers (3×IQR): {len(outliers)} ({pct_outliers:.1f}%)")

    resultados.append({
        'Año': año,
        'N_Casos': len(df_año),
        'Media': round(media, 2),
        'Mediana': round(mediana, 2),
        'Q3': round(Q3, 2),
        'IQR': round(IQR, 2),
        'Limite_3IQR': round(limite_superior, 2),
        'Maximo': round(maximo, 2),
        'Outliers_3IQR': len(outliers),
        'Pct_Outliers': round(pct_outliers, 1)
    })

df_estadisticas = pd.DataFrame(resultados)
archivo = RUTA_SALIDA_TABLAS / "estadisticas_por_año_3IQR_2019_2022.csv"
df_estadisticas.to_csv(archivo, index=False, encoding='utf-8')
print(f"\n✅ Estadísticas guardadas: {archivo.name}")

# =============================================================================
# 3. ANÁLISIS DE SENSIBILIDAD CON FILTRO ≤60 DÍAS
# =============================================================================
print("\n" + "=" * 70)
print("ANÁLISIS DE SENSIBILIDAD - FILTRO ≤60 DÍAS")
print("=" * 70)

def calcular_metricas_con_filtro(df, max_dias=None):
    resultados = []
    for año in [2019, 2020, 2021, 2022]:
        df_año = df[df[anio_col] == año]
        if año not in oecd_espana:
            continue
        if max_dias:
            df_año = df_año[df_año['dias_cama'] <= max_dias]
        if len(df_año) == 0:
            continue
        estadia = df_año['dias_cama'].mean()
        ref = oecd_espana[año]
        brecha = estadia - ref
        brecha_pct = (brecha / ref) * 100
        resultados.append({
            'Año': año,
            'N_Casos': len(df_año),
            'Estadia': round(estadia, 2),
            'Brecha_%': round(brecha_pct, 1)
        })
    return pd.DataFrame(resultados)

print("\n📊 SIN FILTRO:")
df_sin_filtro = calcular_metricas_con_filtro(df)
print(df_sin_filtro.to_string(index=False))

print("\n📊 CON FILTRO ≤60 DÍAS:")
df_con_filtro = calcular_metricas_con_filtro(df, max_dias=60)
print(df_con_filtro.to_string(index=False))

df_sin_filtro.to_csv(RUTA_SALIDA_TABLAS / "analisis_sin_filtro_3IQR_2019_2022.csv", index=False)
df_con_filtro.to_csv(RUTA_SALIDA_TABLAS / "analisis_con_filtro_60dias_3IQR_2019_2022.csv", index=False)

print("\n✅ ANÁLISIS DE SENSIBILIDAD COMPLETADO")