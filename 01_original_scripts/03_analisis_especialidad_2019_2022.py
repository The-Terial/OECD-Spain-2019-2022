"""
Script 03: Análisis desagregado por especialidad (2019-2022)
Paper 4 - Chile vs OECD-España
Especialidades: Cardiología, Cirugía Cardiovascular, Cirugía Vascular Periférica
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

# =============================================================================
# 1. ESTÁNDARES OECD-ESPAÑA POR ESPECIALIDAD
# =============================================================================
oecd_por_especialidad = {
    'CARDIOLOGÍA': 5.8,
    'CIRUGÍA CARDIOVASCULAR': 7.2,
    'CIRUGÍA VASCULAR PERIFÉRICA': 4.5
}

print("=" * 70)
print("ANÁLISIS DESAGREGADO POR ESPECIALIDAD (2019-2022)")
print("=" * 70)

# =============================================================================
# 2. CARGA DE DATOS
# =============================================================================
df = pd.read_csv(RUTA_DATOS, encoding='utf-8')
print(f"✅ Datos cargados: {len(df):,} registros")

def normalizar_especialidad(esp):
    esp = esp.upper()
    if 'CARDIOLOG' in esp:
        return 'CARDIOLOGÍA'
    elif 'CARDIOVASCULAR' in esp and 'CIRUG' in esp:
        return 'CIRUGÍA CARDIOVASCULAR'
    elif 'VASCULAR PERIF' in esp:
        return 'CIRUGÍA VASCULAR PERIFÉRICA'
    else:
        return esp

df['especialidad_norm'] = df['ESPECIALIDAD_MEDICA'].apply(normalizar_especialidad)

# =============================================================================
# 3. CÁLCULO DE MÉTRICAS POR ESPECIALIDAD Y AÑO
# =============================================================================
resultados = []
for especialidad in oecd_por_especialidad.keys():
    df_esp = df[df['especialidad_norm'] == especialidad]
    print(f"\n📌 {especialidad} (total: {len(df_esp):,} casos)")
    for año in [2019, 2020, 2021, 2022]:
        df_año = df_esp[df_esp['aÃ±o'] == año]
        if len(df_año) == 0:
            continue
        media = df_año['dias_cama'].mean()
        std = df_año['dias_cama'].std()
        mediana = df_año['dias_cama'].median()
        comp = df_año['IR_29301_PESO'].mean()
        caei = media / comp if comp > 0 else None
        ref = oecd_por_especialidad[especialidad]
        brecha = media - ref
        brecha_pct = (brecha / ref) * 100

        resultados.append({
            'Año': año,
            'Especialidad': especialidad,
            'N_Casos': len(df_año),
            'Estadia_Media': round(media, 2),
            'Estadia_Mediana': round(mediana, 1),
            'Desv_Est': round(std, 2),
            'Complejidad': round(comp, 2),
            'CAEI_Chile': round(caei, 2) if caei else None,
            'OECD_Referencia': ref,
            'Brecha_Dias': round(brecha, 2),
            'Brecha_%': round(brecha_pct, 1)
        })
        print(f"   {año}: N={len(df_año):,} | Media={media:.2f} | OECD={ref} | Brecha={brecha_pct:+.1f}%")

# =============================================================================
# 4. GUARDAR RESULTADOS
# =============================================================================
df_result = pd.DataFrame(resultados)
archivo = RUTA_SALIDA_TABLAS / "analisis_por_especialidad_2019_2022.csv"
df_result.to_csv(archivo, index=False, encoding='utf-8')
print(f"\n✅ Resultados guardados: {archivo.name}")

print("\n📊 TABLA RESUMEN POR ESPECIALIDAD:")
print(df_result.to_string(index=False))

print("\n✅ ANÁLISIS POR ESPECIALIDAD COMPLETADO")