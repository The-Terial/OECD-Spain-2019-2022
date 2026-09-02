from pathlib import Path
import warnings

import numpy as np
import pandas as pd
from scipy.optimize import linprog


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "03_processed"
TABLES = ROOT / "04_outputs" / "tables"
TABLES.mkdir(parents=True, exist_ok=True)


def dea_input_vrs(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    """Input-oriented VRS DEA.

    Inputs are resources to contract. Outputs are services/production to preserve.
    This implementation is intended as an ancillary management screen, not as
    confirmatory evidence for causal hospital efficiency.
    """
    X = np.asarray(X, dtype=float)
    Y = np.asarray(Y, dtype=float)
    eps = 1e-9
    X = np.maximum(X, eps)
    Y = np.maximum(Y, eps)

    n, m = X.shape
    _, s = Y.shape
    scores = np.full(n, np.nan)

    for i in range(n):
        c = np.zeros(1 + n)
        c[0] = 1.0

        A_ub = []
        b_ub = []

        for k in range(m):
            row = np.zeros(1 + n)
            row[0] = -X[i, k]
            row[1:] = X[:, k]
            A_ub.append(row)
            b_ub.append(0.0)

        for r in range(s):
            row = np.zeros(1 + n)
            row[1:] = -Y[:, r]
            A_ub.append(row)
            b_ub.append(-Y[i, r])

        A_eq = np.zeros((1, 1 + n))
        A_eq[0, 1:] = 1.0
        b_eq = np.array([1.0])
        bounds = [(0.0, 1.0)] + [(0.0, None)] * n

        res = linprog(
            c,
            A_ub=np.asarray(A_ub),
            b_ub=np.asarray(b_ub),
            A_eq=A_eq,
            b_eq=b_eq,
            bounds=bounds,
            method="highs",
        )
        if res.success:
            scores[i] = min(max(res.x[0], 0.0), 1.0)

    return scores


def build_dmu_dataset(df: pd.DataFrame) -> pd.DataFrame:
    d = df[(df["los_days"].notna()) & (df["drg_weight"] > 0)].copy()
    agg = d.groupby(["COD_HOSPITAL", "year"]).agg(
        n_cases=("los_days", "size"),
        total_bed_days=("los_days", "sum"),
        mean_los=("los_days", "mean"),
        mean_drg_weight=("drg_weight", "mean"),
        complexity_weighted_cases=("drg_weight", "sum"),
        total_transfers=("n_transfers", "sum"),
    ).reset_index()
    agg["aggregate_caei"] = agg["mean_los"] / agg["mean_drg_weight"]
    agg["episode_caei_mean"] = d.assign(
        episode_caei=d["los_days"] / d["drg_weight"]
    ).groupby(["COD_HOSPITAL", "year"])["episode_caei"].mean().values
    return agg[agg["n_cases"] >= 10].copy()


def main():
    warnings.filterwarnings("ignore")
    df = pd.read_csv(PROCESSED / "analysis_dataset_2019_2022.csv", low_memory=False)
    dmu = build_dmu_dataset(df)
    dmu.to_csv(TABLES / "dea_dmu_dataset_hospital_year.csv", index=False)

    results = []
    for year, g in dmu.groupby("year"):
        # Methodological correction relative to the original exploratory script:
        # CAEI is not modeled as a favorable output. Resource use is represented
        # as input; service volume and case-mix burden are modeled as outputs.
        X = g[["total_bed_days", "total_transfers"]].to_numpy()
        Y = g[["n_cases", "complexity_weighted_cases"]].to_numpy()
        scores = dea_input_vrs(X, Y)
        tmp = g[["COD_HOSPITAL", "year", "n_cases", "mean_los", "mean_drg_weight", "aggregate_caei"]].copy()
        tmp["dea_input_vrs_score"] = scores
        tmp["dea_model"] = "input_vrs_inputs_bed_days_transfers_outputs_cases_complexity"
        results.append(tmp)

    out = pd.concat(results, ignore_index=True)
    out.to_csv(TABLES / "dea_ancillary_scores.csv", index=False)

    summary = out.groupby("year").agg(
        dmus=("COD_HOSPITAL", "size"),
        mean_score=("dea_input_vrs_score", "mean"),
        median_score=("dea_input_vrs_score", "median"),
        min_score=("dea_input_vrs_score", "min"),
        efficient_dmus=("dea_input_vrs_score", lambda x: int((x >= 0.9999).sum())),
    ).reset_index()
    summary.to_csv(TABLES / "dea_ancillary_summary.csv", index=False)

    corr = out[["aggregate_caei", "dea_input_vrs_score"]].corr(method="spearman").iloc[0, 1]
    (TABLES / "dea_caei_method_note.txt").write_text(
        "DEA is an ancillary resource-utilization screen. CAEI is not treated as a favorable DEA output. "
        "The preferred ancillary DEA specification uses total bed-days and total transfers as inputs, "
        "and case volume plus complexity-weighted cases as outputs. "
        f"Spearman correlation between aggregate CAEI and DEA score: {corr:.4f}. "
        "This correlation is descriptive and should not be used to validate CAEI."
    )

    print(summary.to_string(index=False))
    print(f"Spearman aggregate CAEI vs DEA score: {corr:.4f}")


if __name__ == "__main__":
    main()
