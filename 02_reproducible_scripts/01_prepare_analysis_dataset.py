from pathlib import Path
import json
import hashlib

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "00_raw_data" / "GRD_Consolidado_v2.csv"
PROCESSED = ROOT / "03_processed"
TABLES = ROOT / "04_outputs" / "tables"
PROCESSED.mkdir(parents=True, exist_ok=True)
TABLES.mkdir(parents=True, exist_ok=True)


TARGET_SPECIALTIES = {
    "CARDIOLOGIA",
    "CARDIOLOGÍA",
    "CIRUGIA CARDIOVASCULAR",
    "CIRUGÍA CARDIOVASCULAR",
    "CIRUGIA VASCULAR PERIFERICA",
    "CIRUGÍA VASCULAR PERIFÉRICA",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_specialty(value):
    if pd.isna(value):
        return value
    s = str(value).upper()
    if "CARDIOLOG" in s and "CIRUG" not in s:
        return "CARDIOLOGIA"
    if "CARDIOVASCULAR" in s and "CIRUG" in s:
        return "CIRUGIA CARDIOVASCULAR"
    if "VASCULAR" in s and "PERIF" in s:
        return "CIRUGIA VASCULAR PERIFERICA"
    return s


def count_transfers(df: pd.DataFrame) -> pd.Series:
    transfer_cols = [
        c for c in df.columns
        if c.upper().startswith("FECHATRASLADO")
    ]
    if not transfer_cols:
        return pd.Series(0, index=df.index)
    return df[transfer_cols].notna().sum(axis=1)


def main():
    df = pd.read_csv(RAW, sep="|", low_memory=False)
    raw_columns = len(df.columns)
    df["specialty_norm"] = df["ESPECIALIDAD_MEDICA"].map(normalize_specialty)
    df["year"] = pd.to_numeric(df["año"], errors="coerce").astype("Int64")
    df["los_days"] = pd.to_numeric(df["dias_cama"], errors="coerce")
    df["drg_weight"] = pd.to_numeric(df["IR_29301_PESO"], errors="coerce")
    df["n_transfers"] = count_transfers(df)

    df["primary_circulatory_icd"] = (
        df["DIAGNOSTICO1"].astype(str).str.upper().str.match(r"^I[0-9]{2}")
    )
    diag_cols = [c for c in df.columns if c.upper().startswith("DIAGNOSTICO")]
    df["any_circulatory_icd"] = df[diag_cols].astype(str).apply(
        lambda row: any(str(v).upper().startswith("I") and len(str(v)) >= 3 and str(v)[1:3].isdigit() for v in row),
        axis=1,
    )

    analysis = df[df["year"].isin([2019, 2020, 2021, 2022])].copy()
    analysis.to_csv(PROCESSED / "analysis_dataset_2019_2022.csv", index=False)

    complete_los = analysis[analysis["los_days"].notna()].copy()
    complete_los.to_csv(PROCESSED / "analysis_dataset_complete_los_2019_2022.csv", index=False)

    dq = {
        "raw_file": str(RAW.relative_to(ROOT)),
        "raw_sha256": sha256(RAW),
        "raw_rows": int(len(df)),
        "raw_columns": int(raw_columns),
        "year_counts": {str(k): int(v) for k, v in df["year"].value_counts(dropna=False).sort_index().items()},
        "analysis_rows_2019_2022": int(len(analysis)),
        "missing_los_2019_2022": int(analysis["los_days"].isna().sum()),
        "complete_los_rows_2019_2022": int(len(complete_los)),
        "zero_or_missing_drg_weight_2019_2022": int((analysis["drg_weight"].isna() | (analysis["drg_weight"] <= 0)).sum()),
        "unique_hospitals_2019_2022": int(analysis["COD_HOSPITAL"].nunique()),
        "specialty_counts_2019_2022": {str(k): int(v) for k, v in analysis["specialty_norm"].value_counts().items()},
        "notes": [
            "Raw data are copied unchanged from the PI-provided zip.",
            "CSV delimiter is a vertical bar: sep='|'.",
            "Derived columns are added only in processed files.",
        ],
    }
    (TABLES / "data_quality_report.json").write_text(json.dumps(dq, indent=2))

    print(json.dumps(dq, indent=2))


if __name__ == "__main__":
    main()
