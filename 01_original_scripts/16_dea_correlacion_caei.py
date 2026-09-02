"""
Script 16: Correlación DEA con CAEI (2019-2022)
Paper 4 - Chile vs OECD-España
Valida la consistencia del CAEI como indicador de eficiencia
Autor: José Rodríguez López
Fecha: 2026-06-24
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from pathlib import Path

# =============================================================================
# CONFIGURACIÓN
# =============================================================================
RUTA_BASE = Path("C:/Users/joser/Documents/DOCTORADO_2026/P4_Spain_vs_Chile")
RUTA_DEA = RUTA_BASE / "3_resultados/tablas/resultados_dea_2019_2022.csv"
RUTA_DATOS_DEA = RUTA_BASE / "3_resultados/tablas/datos_dea_hospital_2019_2022.csv"
RUTA_SALIDA_TABLAS = RUTA_BASE / "3_resultados/tablas"
RUTA_SALIDA_FIGURAS = RUTA_BASE / "3_resultados/figuras"
RUTA_SALIDA_TABLAS.mkdir(parents=True, exist_ok=True)
RUTA_SALIDA_FIGURAS.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("SCRIPT 16: CORRELACIÓN DEA vs CAEI (2019-2022)")
print("=" * 70)

# =============================================================================
# 1. CARGA DE DATOS
# =============================================================================
df_dea = pd.read_csv(RUTA_DEA, encoding='utf-8')
df_datos = pd.read_csv(RUTA_DATOS_DEA, encoding='utf-8')

# Unir eficiencia DEA con variables originales
df_merged = df_datos.merge(df_dea, on=['COD_HOSPITAL', 'Año'], how='inner')
print(f"✅ Datos combinados: {len(df_merged)} observaciones")

# =============================================================================
# 2. ANÁLISIS DE CORRELACIÓN
# =============================================================================
print("\n📊 ANÁLISIS DE CORRELACIÓN DEA vs CAEI:")
print("-" * 60)

# Correlación entre Eficiencia_DEA y CAEI (CAEI más bajo = más eficiente)
# Esperamos que hospitales con CAEI bajo tengan mayor eficiencia DEA
corr, p_valor = stats.pearsonr(df_merged['Eficiencia_DEA'], df_merged['CAEI'])

print(f"   Correlación DEA vs CAEI (Pearson): {corr:.4f}")
print(f"   p-valor: {p_valor:.4f}")

if p_valor < 0.05:
    print("   ✅ Correlación estadísticamente significativa (p < 0.05)")
else:
    print("   ⚠️  Correlación no significativa (p ≥ 0.05)")

# Correlación con signo invertido (CAEI más bajo = más eficiente)
# Si CAEI es un buen indicador, debería correlacionar negativamente con eficiencia DEA
# (eficiencia alta = CAEI bajo)
corr_inv, p_valor_inv = stats.pearsonr(df_merged['Eficiencia_DEA'], -df_merged['CAEI'])
print(f"\n   Correlación DEA vs -CAEI (esperado positivo): {corr_inv:.4f}")

# =============================================================================
# 3. ANÁLISIS POR AÑO
# =============================================================================
print("\n📊 CORRELACIÓN POR AÑO:")
print("-" * 60)

for año in sorted(df_merged['Año'].unique()):
    df_año = df_merged[df_merged['Año'] == año]
    corr_año, p_año = stats.pearsonr(df_año['Eficiencia_DEA'], df_año['CAEI'])
    print(f"   {año}: n={len(df_año)}, r={corr_año:.4f}, p={p_año:.4f}")

# =============================================================================
# 4. RANKING DE HOSPITALES (por eficiencia DEA)
# =============================================================================
print("\n🏆 TOP 10 HOSPITALES MÁS EFICIENTES (promedio 2019-2022):")
print("-" * 60)

# Promedio de eficiencia por hospital
ranking = df_merged.groupby('COD_HOSPITAL').agg({
    'Eficiencia_DEA': 'mean',
    'CAEI': 'mean',
    'N_Casos': 'sum'
}).round(4).sort_values('Eficiencia_DEA', ascending=False)

print(ranking.head(10).to_string())

# =============================================================================
# 5. GUARDAR RESULTADOS DE CORRELACIÓN
# =============================================================================
resultados_corr = pd.DataFrame({
    'Año': ['Global'] + sorted(df_merged['Año'].unique()),
    'Correlación_DEA_vs_CAEI': [corr] + [stats.pearsonr(df_merged[df_merged['Año']==a]['Eficiencia_DEA'], 
                                                           df_merged[df_merged['Año']==a]['CAEI'])[0] for a in sorted(df_merged['Año'].unique())],
    'p_valor': [p_valor] + [stats.pearsonr(df_merged[df_merged['Año']==a]['Eficiencia_DEA'], 
                                             df_merged[df_merged['Año']==a]['CAEI'])[1] for a in sorted(df_merged['Año'].unique())]
})

archivo_corr = RUTA_SALIDA_TABLAS / "correlacion_dea_caei_2019_2022.csv"
resultados_corr.to_csv(archivo_corr, index=False, encoding='utf-8')
print(f"\n✅ Correlación guardada: {archivo_corr.name}")

# =============================================================================
# 6. GRÁFICO: DEA vs CAEI
# =============================================================================
plt.figure(figsize=(12, 8))

# Scatter plot
scatter = plt.scatter(df_merged['CAEI'], df_merged['Eficiencia_DEA'], 
                      c=df_merged['Año'], cmap='viridis', alpha=0.7, s=50)
plt.colorbar(scatter, label='Año')

# Línea de tendencia
m, b = np.polyfit(df_merged['CAEI'], df_merged['Eficiencia_DEA'], 1)
plt.plot(df_merged['CAEI'].sort_values(), 
         m * df_merged['CAEI'].sort_values() + b, 
         color='red', linestyle='--', label=f'Tendencia (r={corr:.3f})')

plt.xlabel('CAEI (días / peso GRD)')
plt.ylabel('Eficiencia DEA (1 = frontera eficiente)')
plt.title('Relación entre CAEI y Eficiencia DEA por Hospital (2019-2022)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

archivo_fig = RUTA_SALIDA_FIGURAS / "Figura_DEA_vs_CAEI_2019_2022.png"
plt.savefig(archivo_fig, dpi=300, bbox_inches='tight')
plt.close()
print(f"✅ Gráfico DEA vs CAEI guardado: {archivo_fig.name}")

print("\n✅ SCRIPT 16 COMPLETADO")