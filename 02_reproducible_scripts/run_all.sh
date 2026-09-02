#!/usr/bin/env bash
set -euo pipefail

python3 02_reproducible_scripts/01_prepare_analysis_dataset.py
python3 02_reproducible_scripts/02_caei_sensitivity.py
python3 02_reproducible_scripts/03_dea_ancillary_resource_check.py
