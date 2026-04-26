"""Statistical computations for the climate analysis workflow."""

from __future__ import annotations

from scipy import stats
import pandas as pd


def linear_regression_results(df: pd.DataFrame) -> dict[str, float]:
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        df["co2_emissions_mt"], df["temperature_change_c"]
    )
    return {
        "slope": slope,
        "intercept": intercept,
        "r_value": r_value,
        "p_value": p_value,
        "std_err": std_err,
    }


def one_way_anova(groups: list[pd.Series]) -> dict[str, float | str]:
    f_stat, p_value = stats.f_oneway(*groups)
    conclusion = "Significant (p < 0.05)" if p_value < 0.05 else "Not Significant"
    return {"f_statistic": f_stat, "p_value": p_value, "conclusion": conclusion}


def kruskal_wallis(groups: list[pd.Series]) -> dict[str, float | str]:
    h_stat, p_value = stats.kruskal(*groups)
    conclusion = "Significant (p < 0.05)" if p_value < 0.05 else "Not Significant"
    return {"h_statistic": h_stat, "p_value": p_value, "conclusion": conclusion}


def spearman_correlation(df: pd.DataFrame, x_column: str, y_column: str) -> dict[str, float | str]:
    coefficient, p_value = stats.spearmanr(df[x_column], df[y_column])
    conclusion = "Monotonic relationship detected" if p_value < 0.05 else "No significant monotonic relationship"
    return {
        "coefficient": coefficient,
        "p_value": p_value,
        "conclusion": conclusion,
    }


def zscore_outliers(df: pd.DataFrame, columns: list[str], threshold: float = 3.0) -> pd.DataFrame:
    numeric = df[columns].astype(float)
    zscores = pd.DataFrame(stats.zscore(numeric, nan_policy="omit"), columns=columns, index=df.index)
    mask = zscores.abs().max(axis=1) >= threshold
    outliers = df.loc[mask, ["country", "region", *columns]].copy()
    outliers["max_abs_zscore"] = zscores.loc[mask].abs().max(axis=1).round(2)
    return outliers.sort_values("max_abs_zscore", ascending=False).reset_index(drop=True)
