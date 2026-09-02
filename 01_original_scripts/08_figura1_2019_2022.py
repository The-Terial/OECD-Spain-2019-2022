"""
Script 08: Figura 1 - Evolución de la brecha (2 paneles, 2019-2022)
Panel A: Estancia 2019-2022
Panel B: CAEI 2019-2022
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
RUTA_COMPARATIVA = RUTA_BASE / "3_resultados/tablas/comparativa_oecd_chile_completa_2019_2022.csv"
RUTA_CAEI = RUTA_BASE / "3_resultados/tablas/analisis_caei_especialidad_2019_2022.csv"
RUTA_FIGURAS = RUTA_BASE / "3_resultados/figuras"
RUTA_FIGURAS.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("FIGURA 1: EVOLUCIÓN DE LA BRECHA (2019-2022)")
print("=" * 70)

# =============================================================================
# 1. CARGA DE DATOS
# =============================================================================
df_comp = pd.read_csv(RUTA_COMPARATIVA)
df_caei = pd.read_csv(RUTA_CAEI)

df_comp = df_comp[df_comp['Año'] < 2023]
df_caei = df_caei[df_caei['Año'] < 2023]

# =============================================================================
# 2. FIGURA (ESPAÑOL)
# =============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Panel A: Estancia 2019-2022
ax1.plot(df_comp['Año'], df_comp['Estadia_Promedio_Chile'], 'b-o', 
         label='Chile', linewidth=2, markersize=8)
ax1.plot(df_comp['Año'], df_comp['Estadia_OECD_España'], 'r--s', 
         label='OECD-España', linewidth=2, markersize=8)
ax1.set_xlabel('Año')
ax1.set_ylabel('Días de estancia')
ax1.set_title('A) Estancia hospitalaria 2019-2022')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_xticks([2019, 2020, 2021, 2022])

# Panel B: CAEI por especialidad 2019-2022
colores = {'CARDIOLOGÍA': 'blue', 'CIRUGÍA CARDIOVASCULAR': 'green', 
           'CIRUGÍA VASCULAR PERIFÉRICA': 'orange'}
for esp in df_caei['Especialidad'].unique():
    df_esp = df_caei[df_caei['Especialidad'] == esp]
    ax2.plot(df_esp['Año'], df_esp['CAEI_Chile'], 
             color=colores[esp], marker='o', label=esp, linewidth=2)
    ref = df_esp['CAEI_Referencia'].iloc[0]
    ax2.axhline(y=ref, color=colores[esp], linestyle='--', alpha=0.5)

ax2.set_xlabel('Año')
ax2.set_ylabel('CAEI (días / peso GRD)')
ax2.set_title('B) CAEI por especialidad 2019-2022')
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.set_xticks([2019, 2020, 2021, 2022])

plt.suptitle('Figura 1: Evolución de la eficiencia hospitalaria Chile vs OECD-España (2019-2022)', 
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / 'Figura1_2019_2022.png', dpi=300, bbox_inches='tight')
plt.close()

# =============================================================================
# 3. VERSIÓN INGLÉS
# =============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

ax1.plot(df_comp['Año'], df_comp['Estadia_Promedio_Chile'], 'b-o', 
         label='Chile', linewidth=2, markersize=8)
ax1.plot(df_comp['Año'], df_comp['Estadia_OECD_España'], 'r--s', 
         label='OECD-Spain', linewidth=2, markersize=8)
ax1.set_xlabel('Year')
ax1.set_ylabel('Length of stay (days)')
ax1.set_title('A) Length of stay 2019-2022')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_xticks([2019, 2020, 2021, 2022])

for esp in df_caei['Especialidad'].unique():
    df_esp = df_caei[df_caei['Especialidad'] == esp]
    ax2.plot(df_esp['Año'], df_esp['CAEI_Chile'], 
             color=colores[esp], marker='o', label=esp, linewidth=2)
    ref = df_esp['CAEI_Referencia'].iloc[0]
    ax2.axhline(y=ref, color=colores[esp], linestyle='--', alpha=0.5)

ax2.set_xlabel('Year')
ax2.set_ylabel('CAEI (days / GRD weight)')
ax2.set_title('B) CAEI by specialty 2019-2022')
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.set_xticks([2019, 2020, 2021, 2022])

plt.tight_layout()
plt.savefig(RUTA_FIGURAS / 'Figura1_2019_2022_ingles.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ Figura 1 generada (español e inglés)")