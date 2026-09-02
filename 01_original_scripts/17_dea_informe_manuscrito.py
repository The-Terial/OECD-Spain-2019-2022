"""
Script 17: Informe DEA para el manuscrito (2019-2022)
Paper 4 - Chile vs OECD-España
Genera tabla de resultados DEA para incluir en el manuscrito
Autor: José Rodríguez López
Fecha: 2026-06-24
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

# =============================================================================
# CONFIGURACIÓN
# =============================================================================
RUTA_BASE = Path("C:/Users/joser/Documents/DOCTORADO_2026/P4_Spain_vs_Chile")
RUTA_DEA = RUTA_BASE / "3_resultados/tablas/resultados_dea_2019_2022.csv"
RUTA_DATOS_DEA = RUTA_BASE / "3_resultados/tablas/datos_dea_hospital_2019_2022.csv"
RUTA_CORR = RUTA_BASE / "3_resultados/tablas/correlacion_dea_caei_2019_2022.csv"
RUTA_SALIDA_TABLAS = RUTA_BASE / "3_resultados/tablas"
RUTA_SALIDA_TABLAS.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("SCRIPT 17: INFORME DEA PARA EL MANUSCRITO (2019-2022)")
print("=" * 70)

# =============================================================================
# 1. CARGA DE DATOS
# =============================================================================
df_dea = pd.read_csv(RUTA_DEA, encoding='utf-8')
df_datos = pd.read_csv(RUTA_DATOS_DEA, encoding='utf-8')
df_corr = pd.read_csv(RUTA_CORR, encoding='utf-8')

# Unir para informe
df_merged = df_datos.merge(df_dea, on=['COD_HOSPITAL', 'Año'], how='inner')

# =============================================================================
# 2. TABLA RESUMEN DE EFICIENCIA POR AÑO
# =============================================================================
print("\n📋 TABLA 1: EFICIENCIA DEA POR AÑO")
print("-" * 60)

tabla_eficiencia = df_merged.groupby('Año').agg({
    'Eficiencia_DEA': ['mean', 'median', 'std', 'min', 'max'],
    'COD_HOSPITAL': 'count'
}).round(4)

tabla_eficiencia.columns = ['Media', 'Mediana', 'Desv_Std', 'Mínimo', 'Máximo', 'N_Hospitales']
tabla_eficiencia = tabla_eficiencia.reset_index()

print(tabla_eficiencia.to_string(index=False))

# =============================================================================
# 3. TABLA: HOSPITALES MÁS EFICIENTES Y MENOS EFICIENTES (2022)
# =============================================================================
print("\n📋 TABLA 2: TOP 5 Y BOTTOM 5 HOSPITALES (2022)")
print("-" * 60)

df_2022 = df_merged[df_merged['Año'] == 2022].copy()

# Top 5 más eficientes
top5 = df_2022.nlargest(5, 'Eficiencia_DEA')[['COD_HOSPITAL', 'Eficiencia_DEA', 'CAEI', 'N_Casos']]
print("\n🏆 Top 5 más eficientes:")
print(top5.to_string(index=False))

# Bottom 5 menos eficientes
bottom5 = df_2022.nsmallest(5, 'Eficiencia_DEA')[['COD_HOSPITAL', 'Eficiencia_DEA', 'CAEI', 'N_Casos']]
print("\n⚠️  Bottom 5 menos eficientes:")
print(bottom5.to_string(index=False))

# =============================================================================
# 4. INFORME PARA EL MANUSCRITO
# =============================================================================
fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
archivo_informe = RUTA_SALIDA_TABLAS / f"informe_dea_manuscrito_{fecha}.txt"

contenido = f"""
{'='*80}
INFORME DEA PARA EL MANUSCRITO - PAPER 4 (2019-2022)
{'='*80}

Fecha: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}

{'='*80}
1. MODELO DEA
{'='*80}

Modelo: Data Envelopment Analysis (DEA)
Orientación: Input-oriented (minimizar recursos)
Rendimientos a escala: Variables (VRS)

Inputs:
- dias_cama_promedio: promedio de días de estancia por hospital/año
- IR_29301_PESO_promedio: promedio de complejidad GRD por hospital/año
- n_traslados_promedio: promedio de traslados por episodio

Outputs:
- N_Casos: número de altas hospitalarias por hospital/año
- CAEI: Complexity-Adjusted Efficiency Indicator (días / peso GRD)

{'='*80}
2. RESULTADOS DE EFICIENCIA POR AÑO
{'='*80}

{tabla_eficiencia.to_string(index=False)}

Número total de hospitales analizados: {df_merged['COD_HOSPITAL'].nunique()}
Observaciones totales: {len(df_merged)}

{'='*80}
3. CORRELACIÓN DEA vs CAEI
{'='*80}

{df_corr.to_string(index=False)}

Interpretación:
- Correlación negativa entre DEA y CAEI indica que hospitales con menor CAEI
  (mayor eficiencia) tienden a tener mayor eficiencia DEA.
- El signo esperado es positivo si se usa -CAEI.

{'='*80}
4. HALLAZGOS PRINCIPALES
{'='*80}

1. La eficiencia DEA promedio en el período 2019-2022 es de {df_merged['Eficiencia_DEA'].mean():.3f}.
2. El porcentaje de hospitales eficientes (eficiencia = 1) varía entre
   {df_merged.groupby('Año')['Eficiente'].sum().min()} y {df_merged.groupby('Año')['Eficiente'].sum().max()} hospitales por año.
3. La correlación entre DEA y CAEI sugiere que CAEI es un buen proxy de eficiencia
   ({df_corr[df_corr['Año']=='Global']['Correlación_DEA_vs_CAEI'].values[0]:.3f}, p={df_corr[df_corr['Año']=='Global']['p_valor'].values[0]:.4f}).

{'='*80}
5. IMPLICACIONES PARA POLÍTICA PÚBLICA
{'='*80}

1. Los hospitales identificados como eficientes pueden servir como referentes
   para programas de mejora de eficiencia.
2. La brecha entre hospitales eficientes e ineficientes sugiere oportunidades
   de optimización de recursos.
3. CAEI se valida como un indicador de eficiencia consistente con el DEA,
   respaldando su uso como métrica de monitoreo continuo.

{'='*80}
FIN DEL INFORME
{'='*80}
"""

with open(archivo_informe, 'w', encoding='utf-8') as f:
    f.write(contenido)

print(f"\n✅ Informe DEA para manuscrito guardado: {archivo_informe.name}")

print("\n✅ SCRIPT 17 COMPLETADO")