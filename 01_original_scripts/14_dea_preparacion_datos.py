"""
Script 14: Preparación de datos para DEA (2019-2022) - CORREGIDO
Paper 4 - Chile vs OECD-España
Agrega datos por hospital y año para el modelo DEA
Autor: José Rodríguez López
Fecha: 2026-06-24
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

print("=" * 70)
print("SCRIPT 14: PREPARACIÓN DE DATOS PARA DEA (2019-2022) - CORREGIDO")
print("=" * 70)

# =============================================================================
# 1. CARGA DE DATOS
# =============================================================================
df = pd.read_csv(RUTA_DATOS, encoding='utf-8', low_memory=False)  # <-- SE AGREGÓ low_memory=False
print(f"✅ Datos cargados: {len(df):,} registros (2019-2022)")

anio_col = 'aÃ±o' if 'aÃ±o' in df.columns else 'año'

# =============================================================================
# 2. VARIABLES PARA DEA (TODAS EXISTEN EN LA BD)
# =============================================================================
# DMU: COD_HOSPITAL (identificador único del hospital)
# Inputs: dias_cama, IR_29301_PESO, n_traslados
# Outputs: N_Casos (count), CAEI (dias_cama / IR_29301_PESO)
# =============================================================================

# Verificar columnas necesarias
req = ['COD_HOSPITAL', 'dias_cama', 'IR_29301_PESO', anio_col]
if 'n_traslados' not in df.columns:
    print("\n⚠️  Columna 'n_traslados' no encontrada. Calculando desde FECHATRASLADO...")
    traslado_cols = [c for c in df.columns if 'FECHATRASLADO' in c and c.endswith(tuple(['1','2','3','4','5','6','7','8','9']))]
    df['n_traslados'] = df[traslado_cols].notna().sum(axis=1)
    print(f"   ✅ 'n_traslados' calculada a partir de {len(traslado_cols)} columnas de traslado")
else:
    df['n_traslados'] = pd.to_numeric(df['n_traslados'], errors='coerce').fillna(0)

# =============================================================================
# 3. AGREGACIÓN POR HOSPITAL Y AÑO - CORREGIDO
# =============================================================================
print("\n📊 AGREGANDO DATOS POR HOSPITAL Y AÑO:")
print("-" * 60)

# Usar nombres diferentes para evitar conflicto
df_dea = df.groupby(['COD_HOSPITAL', df[anio_col].astype(int)]).agg(
    dias_cama_promedio=('dias_cama', 'mean'),
    IR_29301_PESO_promedio=('IR_29301_PESO', 'mean'),
    n_traslados_promedio=('n_traslados', 'mean'),
    N_Casos=('dias_cama', 'count')
).reset_index()

# Renombrar columna de año
df_dea = df_dea.rename(columns={anio_col: 'Año'})

# Verificar que tenemos las columnas correctas
print(f"✅ Columnas generadas: {df_dea.columns.tolist()}")
print(f"✅ Dimensiones: {df_dea.shape}")

# =============================================================================
# 4. CALCULAR CAEI (Output 2)
# =============================================================================
df_dea['CAEI'] = df_dea['dias_cama_promedio'] / df_dea['IR_29301_PESO_promedio']

# =============================================================================
# 5. FILTRAR HOSPITALES CON DATOS SUFICIENTES
# =============================================================================
# Mínimo 10 casos por año para tener una estimación confiable
df_dea = df_dea[df_dea['N_Casos'] >= 10].copy()

print(f"\n✅ Hospitales con ≥10 casos por año: {len(df_dea)} observaciones")
print(f"   Años incluidos: {sorted(df_dea['Año'].unique())}")
print(f"   Hospitales únicos: {df_dea['COD_HOSPITAL'].nunique()}")

# =============================================================================
# 6. ESTADÍSTICAS DESCRIPTIVAS DE LAS VARIABLES DEA
# =============================================================================
print("\n📊 ESTADÍSTICAS DESCRIPTIVAS DE VARIABLES DEA:")
print("-" * 60)
print(df_dea[['dias_cama_promedio', 'IR_29301_PESO_promedio', 
              'n_traslados_promedio', 'N_Casos', 'CAEI']].describe().round(2))

# =============================================================================
# 7. GUARDAR DATOS PREPARADOS PARA DEA
# =============================================================================
archivo_salida = RUTA_SALIDA_TABLAS / "datos_dea_hospital_2019_2022.csv"
df_dea.to_csv(archivo_salida, index=False, encoding='utf-8')
print(f"\n✅ Datos DEA guardados: {archivo_salida.name}")

print("\n✅ SCRIPT 14 COMPLETADO")