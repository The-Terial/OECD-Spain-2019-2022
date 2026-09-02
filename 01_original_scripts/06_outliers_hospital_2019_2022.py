"""
Script 06: Outliers por hospital (2019-2022)
Paper 4 - Chile vs OECD-España
Método: Q3 + 3×IQR (conservador)
Autor: José Rodríguez López
Fecha: 2026-06-23
"""

import pandas as pd
from pathlib import Path

# =============================================================================
# CONFIGURACIÓN
# =============================================================================
RUTA_BASE = Path("C:/Users/joser/Documents/DOCTORADO_2026/P4_Spain_vs_Chile")
RUTA_DATOS = RUTA_BASE / "3_resultados/datos_circulatorio_filtrados_2019_2022.csv"
RUTA_SALIDA = RUTA_BASE / "3_resultados/tablas"
RUTA_SALIDA.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("ANÁLISIS DE OUTLIERS POR HOSPITAL (2019-2022)")
print("(Método Q3 + 3×IQR)")
print("=" * 70)

# =============================================================================
# 1. CARGA DE DATOS Y CÁLCULO DE LÍMITES
# =============================================================================
df = pd.read_csv(RUTA_DATOS, encoding='utf-8')
anio_col = 'aÃ±o' if 'aÃ±o' in df.columns else 'año'

Q1 = df['dias_cama'].quantile(0.25)
Q3 = df['dias_cama'].quantile(0.75)
IQR = Q3 - Q1
limite_superior = Q3 + 3 * IQR

print(f"\n📊 LÍMITES GLOBALES (3×IQR):")
print(f"   Q1 = {Q1:.1f} días")
print(f"   Q3 = {Q3:.1f} días")
print(f"   IQR = {IQR:.1f}")
print(f"   Límite superior = {limite_superior:.1f} días")
print(f"   Casos > límite: {(df['dias_cama'] > limite_superior).sum():,} "
      f"({((df['dias_cama'] > limite_superior).sum()/len(df)*100):.1f}%)")

# =============================================================================
# 2. OUTLIERS POR HOSPITAL
# =============================================================================
outliers = df[df['dias_cama'] > limite_superior].copy()
outliers_por_hospital = outliers['COD_HOSPITAL'].value_counts().head(20)

print("\n🏥 TOP 20 HOSPITALES CON MÁS OUTLIERS (3×IQR):")
print("-" * 60)
for hosp, count in outliers_por_hospital.items():
    total_hosp = len(df[df['COD_HOSPITAL'] == hosp])
    pct = (count / total_hosp) * 100 if total_hosp > 0 else 0
    print(f"   Hospital {hosp}: {count} outliers ({pct:.1f}% de sus casos)")

# =============================================================================
# 3. GUARDAR RESULTADOS
# =============================================================================
df_outliers = pd.DataFrame({
    'COD_HOSPITAL': outliers_por_hospital.index,
    'N_Outliers_3IQR': outliers_por_hospital.values
})
archivo = RUTA_SALIDA / "outliers_por_hospital_3IQR_2019_2022.csv"
df_outliers.to_csv(archivo, index=False, encoding='utf-8')
print(f"\n✅ Resultados guardados: {archivo.name}")

print("\n📅 DISTRIBUCIÓN DE OUTLIERS POR AÑO (3×IQR):")
outliers_por_año = outliers[anio_col].value_counts().sort_index()
for año, count in outliers_por_año.items():
    total_año = len(df[df[anio_col] == año])
    pct = (count / total_año) * 100
    print(f"   {int(año)}: {count} outliers ({pct:.1f}% de casos del año)")

print("\n✅ ANÁLISIS COMPLETADO")