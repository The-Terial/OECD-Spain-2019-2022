"""
Script 11: Figura 4 - Distribución de estancias (2019 vs 2022)
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
RUTA_DATOS = RUTA_BASE / "3_resultados/datos_circulatorio_filtrados_2019_2022.csv"
RUTA_FIGURAS = RUTA_BASE / "3_resultados/figuras"
RUTA_FIGURAS.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("FIGURA 4: DISTRIBUCIÓN DE ESTANCIAS (2019 vs 2022)")
print("=" * 70)

df = pd.read_csv(RUTA_DATOS)
anio_col = 'aÃ±o' if 'aÃ±o' in df.columns else 'año'

df_2019 = df[df[anio_col] == 2019]['dias_cama']
df_2022 = df[df[anio_col] == 2022]['dias_cama']

# Español
plt.figure(figsize=(12, 5))
plt.hist(df_2019, bins=30, alpha=0.7, label='2019', color='blue', edgecolor='black')
plt.hist(df_2022, bins=30, alpha=0.7, label='2022', color='red', edgecolor='black')
plt.xlabel('Días de estancia')
plt.ylabel('Frecuencia')
plt.title('Distribución de estancias: 2019 vs 2022')
plt.legend()
plt.xlim(0, 400)
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / 'Figura4_Distribucion_2019_2022.png', dpi=300)
plt.close()

# Inglés
plt.figure(figsize=(12, 5))
plt.hist(df_2019, bins=30, alpha=0.7, label='2019', color='blue', edgecolor='black')
plt.hist(df_2022, bins=30, alpha=0.7, label='2022', color='red', edgecolor='black')
plt.xlabel('Length of stay (days)')
plt.ylabel('Frequency')
plt.legend()
plt.xlim(0, 400)
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / 'Figura4_Distribucion_2019_2022_ingles.png', dpi=300)
plt.close()

print("✅ Figura 4 generada (español e inglés)")