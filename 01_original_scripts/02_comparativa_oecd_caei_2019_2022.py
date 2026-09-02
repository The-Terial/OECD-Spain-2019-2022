"""
Script 02: Comparativa Chile vs OECD-España con CAEI (2019-2022)
Paper 4 - Chile vs OECD-España
Indicador: CAEI = Estadia_promedio / Complejidad_promedio (IR_29301_PESO)
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
RUTA_SALIDA_FIGURAS = RUTA_BASE / "3_resultados/figuras"
RUTA_SALIDA_TABLAS.mkdir(parents=True, exist_ok=True)
RUTA_SALIDA_FIGURAS.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("COMPARATIVA CHILE vs OECD-ESPAÑA (2019-2022)")
print("=" * 70)

# =============================================================================
# 1. DATOS OECD-ESPAÑA (2019-2022)
# =============================================================================
oecd_espana = {
    2019: 9.1,
    2020: 8.6,
    2021: 8.5,
    2022: 8.9
}

print("\n📊 ESTÁNDARES OECD-ESPAÑA (días de estancia, 2019-2022):")
for año, valor in oecd_espana.items():
    print(f"   {año}: {valor} días")

# =============================================================================
# 2. CARGA DE DATOS CHILE
# =============================================================================
try:
    df = pd.read_csv(RUTA_DATOS, low_memory=False, encoding='utf-8')
    print(f"\n✅ Datos Chile cargados: {len(df):,} registros (2019-2022)")
except Exception as e:
    raise SystemExit(f"❌ Error al cargar datos: {e}")

anio_col = 'aÃ±o' if 'aÃ±o' in df.columns else 'año'
df[anio_col] = pd.to_numeric(df[anio_col], errors='coerce')

# =============================================================================
# 3. CÁLCULO DE MÉTRICAS POR AÑO CON CAEI
# =============================================================================
resultados = []
for año in sorted(df[anio_col].dropna().unique()):
    if año not in oecd_espana:
        continue
    df_año = df[df[anio_col] == año]
    if len(df_año) == 0:
        continue

    n_casos = len(df_año)
    estadia_prom = df_año['dias_cama'].mean()
    complejidad_prom = df_año['IR_29301_PESO'].mean()
    caei = estadia_prom / complejidad_prom if complejidad_prom > 0 else None

    estadia_ref = oecd_espana[año]
    brecha_dias = estadia_prom - estadia_ref
    brecha_pct = (brecha_dias / estadia_ref) * 100

    resultados.append({
        'Año': año,
        'N_Casos_Chile': n_casos,
        'Estadia_Promedio_Chile': round(estadia_prom, 2),
        'Desviacion_Chile': round(df_año['dias_cama'].std(), 2),
        'Complejidad_Promedio_Chile': round(complejidad_prom, 2),
        'CAEI_Chile': round(caei, 2) if caei else None,
        'Estadia_OECD_España': estadia_ref,
        'Brecha_Días': round(brecha_dias, 2),
        'Brecha_Porcentaje': round(brecha_pct, 1)
    })

df_resultados = pd.DataFrame(resultados)

# =============================================================================
# 4. MOSTRAR RESULTADOS
# =============================================================================
print("\n📊 COMPARATIVA CHILE vs OECD-ESPAÑA (2019-2022):")
print("-" * 80)
for _, row in df_resultados.iterrows():
    print(f"   {int(row['Año'])}: {row['Estadia_Promedio_Chile']}d (CHL) vs "
          f"{row['Estadia_OECD_España']}d (OECD) → "
          f"Brecha: {row['Brecha_Días']:+.1f}d ({row['Brecha_Porcentaje']:+.1f}%)")

# =============================================================================
# 5. GUARDAR TABLAS
# =============================================================================
archivo_completo = RUTA_SALIDA_TABLAS / "comparativa_oecd_chile_completa_2019_2022.csv"
df_resultados.to_csv(archivo_completo, index=False, encoding='utf-8')
print(f"\n✅ Tabla completa guardada: {archivo_completo.name}")

tabla_resumen = df_resultados[['Año', 'N_Casos_Chile', 'Estadia_Promedio_Chile',
                               'Estadia_OECD_España', 'Brecha_Días', 'Brecha_Porcentaje']].copy()
tabla_resumen['Comparativa'] = tabla_resumen.apply(
    lambda x: f"{x['Estadia_Promedio_Chile']} vs {x['Estadia_OECD_España']} ({x['Brecha_Porcentaje']:+.1f}%)",
    axis=1
)

archivo_resumen = RUTA_SALIDA_TABLAS / "tabla_resumen_paper_2019_2022.csv"
tabla_resumen.to_csv(archivo_resumen, index=False, encoding='utf-8')
print(f"✅ Tabla resumen guardada: {archivo_resumen.name}")

# =============================================================================
# 6. CÁLCULO DE DÍAS-CAMA AHORRABLES
# =============================================================================
df_resultados['Dias_Ahorrables'] = df_resultados['Brecha_Días'] * df_resultados['N_Casos_Chile']
total_ahorrable = df_resultados['Dias_Ahorrables'].sum()
print(f"\n💰 DÍAS-CAMA POTENCIALMENTE LIBERABLES (2019-2022): {total_ahorrable:,.0f} días")

brechas = df_resultados['Brecha_Porcentaje'].dropna()
print(f"\n📋 RESUMEN ESTADÍSTICO (2019-2022):")
print(f"   Brecha promedio: {brechas.mean():+.1f}%")
print(f"   Brecha máxima: {brechas.max():+.1f}%")
print(f"   Brecha mínima: {brechas.min():+.1f}%")

print("\n✅ ANÁLISIS COMPARATIVO COMPLETADO")