"""
Script 10: Figura 3 - Top 10 hospitales con más outliers (2019-2022)
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
RUTA_DATOS = RUTA_BASE / "3_resultados/tablas/outliers_por_hospital_3IQR_2019_2022.csv"
RUTA_FIGURAS = RUTA_BASE / "3_resultados/figuras"
RUTA_FIGURAS.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("FIGURA 3: TOP 10 HOSPITALES CON MÁS OUTLIERS")
print("=" * 70)

df = pd.read_csv(RUTA_DATOS)
top10 = df.head(10)

# Español
plt.figure(figsize=(12, 6))
plt.barh(range(len(top10)), top10['N_Outliers_3IQR'], color='coral')
plt.yticks(range(len(top10)), top10['COD_HOSPITAL'].astype(str))
plt.xlabel('Número de outliers')
plt.title('Figura 3: Top 10 hospitales con más outliers (3×IQR, 2019-2022)')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / 'Figura3_Outliers_2019_2022.png', dpi=300, bbox_inches='tight')
plt.close()

# Inglés
plt.figure(figsize=(12, 6))
plt.barh(range(len(top10)), top10['N_Outliers_3IQR'], color='coral')
plt.yticks(range(len(top10)), top10['COD_HOSPITAL'].astype(str))
plt.xlabel('Number of outliers')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / 'Figura3_Outliers_2019_2022_ingles.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ Figura 3 generada (español e inglés)")