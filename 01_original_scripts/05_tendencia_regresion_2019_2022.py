"""
Script 05: Regresión de tendencia (2019-2022)
Paper 4 - Chile vs OECD-España
Estima pendiente de cambio en días/año por especialidad
Autor: José Rodríguez López
Fecha: 2026-06-23
"""

import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path

# =============================================================================
# CONFIGURACIÓN
# =============================================================================
RUTA_BASE = Path("C:/Users/joser/Documents/DOCTORADO_2026/P4_Spain_vs_Chile")
RUTA_DATOS = RUTA_BASE / "3_resultados/datos_circulatorio_filtrados_2019_2022.csv"
RUTA_SALIDA = RUTA_BASE / "3_resultados/tablas"
RUTA_SALIDA.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("ANÁLISIS DE TENDENCIA - REGRESIÓN LINEAL (2019-2022)")
print("=" * 70)

# =============================================================================
# 1. CARGA DE DATOS
# =============================================================================
df = pd.read_csv(RUTA_DATOS, encoding='utf-8')

def normalizar_especialidad(esp):
    esp = esp.upper()
    if 'CARDIOLOG' in esp:
        return 'CARDIOLOGÍA'
    elif 'CARDIOVASCULAR' in esp and 'CIRUG' in esp:
        return 'CIRUGÍA CARDIOVASCULAR'
    elif 'VASCULAR PERIF' in esp:
        return 'CIRUGÍA VASCULAR PERIFÉRICA'
    return esp

df['especialidad_norm'] = df['ESPECIALIDAD_MEDICA'].apply(normalizar_especialidad)

# =============================================================================
# 2. REGRESIÓN POR ESPECIALIDAD
# =============================================================================
especialidades = df['especialidad_norm'].unique()
resultados = []

print("\n📊 TENDENCIA DE ESTADÍA POR ESPECIALIDAD (2019-2022):")
print("-" * 60)

for esp in especialidades:
    df_esp = df[df['especialidad_norm'] == esp]
    años = []
    medias = []
    for año in [2019, 2020, 2021, 2022]:
        media = df_esp[df_esp['aÃ±o'] == año]['dias_cama'].mean()
        if not np.isnan(media):
            años.append(año)
            medias.append(media)
    if len(años) >= 3:
        slope, intercept, r_value, p_value, std_err = stats.linregress(años, medias)
        resultados.append({
            'Especialidad': esp,
            'Pendiente_días/año': round(slope, 3),
            'R²': round(r_value**2, 3),
            'p_valor': p_value,
            'Significancia': '***' if p_value < 0.001 else '**' if p_value < 0.01 else '*' if p_value < 0.05 else 'ns',
            'Tendencia': 'Aumento' if slope > 0 else 'Disminución'
        })
        print(f"\n{esp}:")
        print(f"   Pendiente = {slope:.3f} días/año")
        print(f"   R² = {r_value**2:.3f}")
        print(f"   p-valor = {p_value:.4f} {resultados[-1]['Significancia']}")

# =============================================================================
# 3. GUARDAR RESULTADOS
# =============================================================================
df_result = pd.DataFrame(resultados)
archivo = RUTA_SALIDA / "tendencias_regresion_2019_2022.csv"
df_result.to_csv(archivo, index=False, encoding='utf-8')
print(f"\n✅ Resultados guardados: {archivo.name}")

print("\n📊 TABLA RESUMEN:")
print(df_result.to_string(index=False))

print("\n✅ ANÁLISIS DE TENDENCIA COMPLETADO")