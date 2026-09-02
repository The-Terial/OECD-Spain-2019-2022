from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "03_processed"
TABLES = ROOT / "04_outputs" / "tables"
TABLES.mkdir(parents=True, exist_ok=True)

SPAIN_OECD_ALOS = {
    2019: 9.1,
    2020: 8.6,
    2021: 8.5,
    2022: 8.9,
}


def summarize_scenario(df: pd.DataFrame, name: str) -> pd.DataFrame:
    d = df.copy()
    d = d[d["los_days"].notna()].copy()
    d["episode_caei"] = d["los_days"] / d["drg_weight"]
    d.loc[d["drg_weight"] <= 0, "episode_caei"] = pd.NA

    out = d.groupby("year").agg(
        analytic_n=("los_days", "size"),
        mean_los=("los_days", "mean"),
        median_los=("los_days", "median"),
        mean_drg_weight=("drg_weight", "mean"),
        aggregate_caei=("los_days", lambda x: x.mean()),
        mean_episode_caei=("episode_caei", "mean"),
        median_episode_caei=("episode_caei", "median"),
        q1_episode_caei=("episode_caei", lambda x: x.quantile(0.25)),
        q3_episode_caei=("episode_caei", lambda x: x.quantile(0.75)),
    ).reset_index()
    out["aggregate_caei"] = out["mean_los"] / out["mean_drg_weight"]
    out["spain_oecd_alos"] = out["year"].map(SPAIN_OECD_ALOS)
    out["gap_days"] = out["mean_los"] - out["spain_oecd_alos"]
    out["gap_percent"] = out["gap_days"] / out["spain_oecd_alos"] * 100
    out.insert(0, "scenario", name)
    return out


def main():
    df = pd.read_csv(PROCESSED / "analysis_dataset_2019_2022.csv", low_memory=False)

    scenarios = {
        "main_specialty_proxy_complete_los": df,
        "los_le_60_days": df[df["los_days"] <= 60],
        "primary_diagnosis_I00_I99": df[df["primary_circulatory_icd"] == True],
        "any_diagnosis_I00_I99": df[df["any_circulatory_icd"] == True],
    }

    results = pd.concat(
        [summarize_scenario(d, name) for name, d in scenarios.items()],
        ignore_index=True,
    )
    numeric_cols = results.select_dtypes("number").columns
    results[numeric_cols] = results[numeric_cols].round(4)
    results.to_csv(TABLES / "caei_sensitivity_results.csv", index=False)

    manuscript_table = results.pivot_table(
        index="scenario",
        columns="year",
        values="gap_percent",
        aggfunc="first",
    ).reset_index()
    manuscript_table.to_csv(TABLES / "table_sensitivity_gap_percent.csv", index=False)

    print(results.to_string(index=False))


if __name__ == "__main__":
    main()
