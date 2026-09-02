"""
Script 04: Análisis de CAEI por especialidad (2019-2022)
Paper 4 - Chile vs OECD-España
CAEI = Estadia / Complejidad (IR_29301_PESO)
Autor: José Rodríguez López
Fecha: 2026-06-23
"""

import pandas as pd
import matplotlib.pyplot as plt
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

# =============================================================================
# 1. VALORES DE REFERENCIA CAEI (ESPAÑA ESTIMADO)
# =============================================================================
caei_referencia = {
    'CARDIOLOGÍA': 3.22,
    'CIRUGÍA CARDIOVASCULAR': 2.57,
    'CIRUGÍA VASCULAR PERIFÉRICA': 2.81
}

print("=" * 70)
print("ANÁLISIS DE CAEI POR ESPECIALIDAD (2019-2022)")
print("=" * 70)

# =============================================================================
# 2. CARGA DE DATOS
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
# 3. CÁLCULO DE CAEI POR ESPECIALIDAD Y AÑO
# =============================================================================
resultados = []
for especialidad in caei_referencia.keys():
    df_esp = df[df['especialidad_norm'] == especialidad]
    print(f"\n📌 {especialidad}")
    for año in [2019, 2020, 2021, 2022]:
        df_año = df_esp[df_esp['aÃ±o'] == año]
        if len(df_año) < 10:
            continue
        media = df_año['dias_cama'].mean()
        comp = df_año['IR_29301_PESO'].mean()
        caei = media / comp if comp > 0 else None
        ref = caei_referencia[especialidad]
        brecha = caei - ref if caei else None
        brecha_pct = (brecha / ref) * 100 if ref and brecha else None

        resultados.append({
            'Año': año,
            'Especialidad': especialidad,
            'N_Casos': len(df_año),
            'Estadia': round(media, 2),
            'Complejidad': round(comp, 2),
            'CAEI_Chile': round(caei, 2) if caei else None,
            'CAEI_Referencia': ref,
            'Brecha_Abs': round(brecha, 2) if brecha else None,
            'Brecha_%': round(brecha_pct, 1) if brecha_pct else None
        })
        if caei:
            print(f"   {año}: CAEI={caei:.2f} | Ref={ref} | Brecha={brecha:+.2f} ({brecha_pct:+.1f}%)")

# =============================================================================
# 4. GUARDAR TABLA
# =============================================================================
df_result = pd.DataFrame(resultados)
archivo_tabla = RUTA_SALIDA_TABLAS / "analisis_caei_especialidad_2019_2022.csv"
df_result.to_csv(archivo_tabla, index=False, encoding='utf-8')
print(f"\n✅ Tabla guardada: {archivo_tabla.name}")

# =============================================================================
# 5. GRÁFICO DE EVOLUCIÓN DEL CAEI
# =============================================================================
plt.figure(figsize=(12, 6))
colores = {'CARDIOLOGÍA': 'blue', 'CIRUGÍA CARDIOVASCULAR': 'green', 'CIRUGÍA VASCULAR PERIFÉRICA': 'orange'}
for especialidad in caei_referencia.keys():
    df_esp = df_result[df_result['Especialidad'] == especialidad]
    plt.plot(df_esp['Año'], df_esp['CAEI_Chile'], 
             color=colores[especialidad], marker='o', label=especialidad, linewidth=2)
    plt.axhline(y=caei_referencia[especialidad], color=colores[especialidad], 
                linestyle='--', alpha=0.5)

plt.xlabel('Año')
plt.ylabel('CAEI (días / peso GRD)')
plt.title('Evolución del CAEI por Especialidad en Chile (2019-2022)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
archivo_fig = RUTA_SALIDA_FIGURAS / "evolucion_caei_especialidad_2019_2022.png"
plt.savefig(archivo_fig, dpi=300, bbox_inches='tight')
plt.close()
print(f"✅ Gráfico guardado: {archivo_fig.name}")

print("\n✅ ANÁLISIS DE CAEI COMPLETADO")