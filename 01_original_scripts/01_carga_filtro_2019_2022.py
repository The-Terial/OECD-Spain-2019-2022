"""
Script 01: Carga y Filtro de Datos GRD (2019-2022)
Paper 4 - Chile vs OECD-España
Excluye 2023 por ser atípico
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
RUTA_DATOS = RUTA_BASE / "1_datos/0_raw/GRD_Consolidado_v2.csv"
RUTA_SALIDA = RUTA_BASE / "3_resultados"
RUTA_SALIDA.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("CARGA Y FILTRO DE DATOS - PAPER 4 (2019-2022)")
print("=" * 70)

# =============================================================================
# 1. CARGA DE DATOS
# =============================================================================
try:
    df = pd.read_csv(RUTA_DATOS, delimiter='|', encoding='latin-1', low_memory=False)
    print(f"✅ Datos cargados: {df.shape[0]:,} filas × {df.shape[1]} columnas")
except Exception as e:
    raise SystemExit(f"❌ Error al cargar datos: {e}")

# =============================================================================
# 2. DETECCIÓN DE COLUMNA DE AÑO
# =============================================================================
anio_col = None
for cand in ["aÃ±o", "año", "AÑO", "ANIO"]:
    if cand in df.columns:
        anio_col = cand
        break

if anio_col is None:
    raise SystemExit("❌ No se encontró columna de año")

print(f"✅ Columna de año detectada: '{anio_col}'")

# =============================================================================
# 3. FILTRAR 2019-2022 (EXCLUIR 2023)
# =============================================================================
df[anio_col] = pd.to_numeric(df[anio_col], errors='coerce')
df = df[df[anio_col].between(2019, 2022)]
print(f"✅ Años incluidos (2019-2022): {sorted(df[anio_col].dropna().unique())}")

# =============================================================================
# 4. FUNCIONES DE FILTRO DE ESPECIALIDADES CIRCULATORIAS
# =============================================================================
def corregir_encoding_especialidad(especialidad):
    if pd.isna(especialidad):
        return None
    correcciones = {
        'CIRUGÃA': 'CIRUGÍA',
        'CARDIOLOGÃA': 'CARDIOLOGÍA',
        'PERIFÃRICA': 'PERIFÉRICA',
        'CARDIOVASCULAR': 'CARDIOVASCULAR',
        'CIRUGIA': 'CIRUGÍA',
        'CARDIOLOGIA': 'CARDIOLOGÍA'
    }
    s = str(especialidad).upper()
    for a, b in correcciones.items():
        s = s.replace(a, b)
    return s.strip()

def es_especialidad_circulatoria(especialidad):
    if pd.isna(especialidad):
        return False
    s = corregir_encoding_especialidad(especialidad)
    circulatorias = [
        'CIRUGÍA CARDIOVASCULAR',
        'CARDIOLOGÍA',
        'CIRUGÍA VASCULAR PERIFÉRICA',
        'ANGIOLOGÍA',
        'HEMODINAMIA'
    ]
    return any(c in s for c in circulatorias)

# =============================================================================
# 5. APLICAR FILTRO
# =============================================================================
df['es_circulatorio'] = df['ESPECIALIDAD_MEDICA'].apply(es_especialidad_circulatoria)
df_circ = df[df['es_circulatorio']].copy()

print(f"\n✅ Registros sistema circulatorio (2019-2022): {len(df_circ):,}")
print(f"✅ Porcentaje del total en período: {len(df_circ)/len(df)*100:.1f}%")

# =============================================================================
# 6. GUARDAR DATOS FILTRADOS
# =============================================================================
output_file = RUTA_SALIDA / "datos_circulatorio_filtrados_2019_2022.csv"
df_circ.to_csv(output_file, index=False, encoding='utf-8')
print(f"✅ Datos filtrados guardados: {output_file.name}")

print("\n✅ EXPLORACIÓN COMPLETADA")
print("\n🔍 VERIFICACIÓN DE ESPECIALIDADES:")
print(df_circ['ESPECIALIDAD_MEDICA'].value_counts())