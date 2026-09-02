"""
Script 12: Figura 5 - Brecha por especialidad (2022)
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
RUTA_DATOS = RUTA_BASE / "3_resultados/tablas/analisis_por_especialidad_2019_2022.csv"
RUTA_FIGURAS = RUTA_BASE / "3_resultados/figuras"
RUTA_FIGURAS.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("FIGURA 5: BRECHA POR ESPECIALIDAD (2022)")
print("=" * 70)

df = pd.read_csv(RUTA_DATOS)
df_2022 = df[df['Año'] == 2022]

# Español
plt.figure(figsize=(10, 6))
plt.bar(df_2022['Especialidad'], df_2022['Brecha_%'], color='steelblue')
plt.xlabel('Especialidad')
plt.ylabel('Brecha porcentual (%)')
plt.title('Brecha de eficiencia por especialidad (2022)')
plt.xticks(rotation=45, ha='right')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / 'Figura5_Brecha_2022.png', dpi=300)
plt.close()

# Inglés
plt.figure(figsize=(10, 6))
plt.bar(['Cardiology', 'Cardiovascular Surgery', 'Peripheral Vascular Surgery'], 
        df_2022['Brecha_%'], color='steelblue')
plt.xlabel('Specialty')
plt.ylabel('Efficiency gap (%)')
plt.xticks(rotation=45, ha='right')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / 'Figura5_Brecha_2022_ingles.png', dpi=300)
plt.close()

print("✅ Figura 5 generada (español e inglés)")