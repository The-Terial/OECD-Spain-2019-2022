"""
Script 09: Figura 2 - Evolución del CAEI por especialidad (2019-2022)
Paper 4 - Chile vs OECD-España
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
RUTA_DATOS = RUTA_BASE / "3_resultados/tablas/analisis_caei_especialidad_2019_2022.csv"
RUTA_FIGURAS = RUTA_BASE / "3_resultados/figuras"
RUTA_FIGURAS.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("FIGURA 2: EVOLUCIÓN DEL CAEI POR ESPECIALIDAD")
print("=" * 70)

df = pd.read_csv(RUTA_DATOS)
df = df[df['Año'] < 2023]

nombres_ing = {
    'CARDIOLOGÍA': 'Cardiology',
    'CIRUGÍA CARDIOVASCULAR': 'Cardiovascular Surgery',
    'CIRUGÍA VASCULAR PERIFÉRICA': 'Vascular Surgery'
}
colores = {
    'CARDIOLOGÍA': 'blue',
    'CIRUGÍA CARDIOVASCULAR': 'green',
    'CIRUGÍA VASCULAR PERIFÉRICA': 'orange'
}

# Español
plt.figure(figsize=(12, 6))
for esp in df['Especialidad'].unique():
    df_esp = df[df['Especialidad'] == esp]
    plt.plot(df_esp['Año'], df_esp['CAEI_Chile'], 
             color=colores[esp], marker='o', label=esp, linewidth=2)
    ref = df_esp['CAEI_Referencia'].iloc[0]
    plt.axhline(y=ref, color=colores[esp], linestyle='--', alpha=0.5)

plt.xlabel('Año')
plt.ylabel('CAEI (días / peso GRD)')
plt.title('Figura 2: Evolución del CAEI por especialidad (2019-2022)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / 'Figura2_CAEI_2019_2022.png', dpi=300, bbox_inches='tight')
plt.close()

# Inglés
plt.figure(figsize=(12, 6))
for esp in df['Especialidad'].unique():
    df_esp = df[df['Especialidad'] == esp]
    plt.plot(df_esp['Año'], df_esp['CAEI_Chile'], 
             color=colores[esp], marker='o', label=nombres_ing[esp], linewidth=2)
    ref = df_esp['CAEI_Referencia'].iloc[0]
    plt.axhline(y=ref, color=colores[esp], linestyle='--', alpha=0.5)

plt.xlabel('Year')
plt.ylabel('CAEI (days / GRD weight)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / 'Figura2_CAEI_2019_2022_ingles.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ Figura 2 generada (español e inglés)")