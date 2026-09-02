"""
Script 13: Informe complementario (2019-2022)
Paper 4 - Chile vs OECD-España
Autor: José Rodríguez López
Fecha: 2026-06-23
"""

from pathlib import Path
from datetime import datetime

# =============================================================================
# CONFIGURACIÓN
# =============================================================================
RUTA_BASE = Path("C:/Users/joser/Documents/DOCTORADO_2026/P4_Spain_vs_Chile")
RUTA_INFORME = RUTA_BASE / "3_resultados"
RUTA_INFORME.mkdir(parents=True, exist_ok=True)

fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
archivo = RUTA_INFORME / f"informe_complementario_{fecha}_2019_2022.txt"

contenido = f"""
{'='*80}
INFORME COMPLEMENTARIO - ANÁLISIS ADICIONALES PAPER 4 (2019-2022)
{'='*80}

Fecha: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}

{'='*80}
1. ANÁLISIS POR ESPECIALIDAD (DESAGREGADO)
{'='*80}
- Se generó tabla con medias, medianas y brechas por especialidad/año
- Archivo: tablas/analisis_por_especialidad_2019_2022.csv

{'='*80}
2. ANÁLISIS DE CAEI POR ESPECIALIDAD
{'='*80}
- Se calculó CAEI = Estadia/Complejidad para cada especialidad
- Comparación con referencia España (estimada)
- Archivo: tablas/analisis_caei_especialidad_2019_2022.csv
- Figura: figuras/evolucion_caei_especialidad_2019_2022.png

{'='*80}
3. REGRESIÓN DE TENDENCIA
{'='*80}
- Se estimó pendiente de cambio en días/año por especialidad
- Se evaluó significancia estadística
- Archivo: tablas/tendencias_regresion_2019_2022.csv

{'='*80}
4. OUTLIERS POR HOSPITAL
{'='*80}
- Se identificaron hospitales con mayor concentración de outliers (3×IQR)
- Archivo: tablas/outliers_por_hospital_3IQR_2019_2022.csv

{'='*80}
ARCHIVOS GENERADOS EN ESTA SESIÓN:
{'='*80}
📁 3_resultados/
├── 📁 tablas/
│   ├── analisis_por_especialidad_2019_2022.csv
│   ├── analisis_caei_especialidad_2019_2022.csv
│   ├── tendencias_regresion_2019_2022.csv
│   └── outliers_por_hospital_3IQR_2019_2022.csv
└── 📁 figuras/
    └── evolucion_caei_especialidad_2019_2022.png

Nota: El año 2023 ha sido excluido del análisis principal por ser atípico.
Los resultados presentados corresponden exclusivamente al período 2019-2022.

{'='*80}
FIN DEL INFORME COMPLEMENTARIO
{'='*80}
"""

with open(archivo, 'w', encoding='utf-8') as f:
    f.write(contenido)

print(f"✅ Informe complementario generado: {archivo}")