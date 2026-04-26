"""Tabular summaries for the climate analysis workflow."""

from __future__ import annotations

import pandas as pd


CORRELATION_COLUMNS = [
    "avg_temperature_c",
    "temperature_change_c",
    "co2_emissions_mt",
    "sea_level_rise_mm",
    "heatwave_days",
    "wildfire_incidents",
    "rainfall_change_mm",
    "air_quality_index",
    "climate_risk_score",
    "population_affected_m",
]

DISTRIBUTION_COLUMNS = [
    "avg_temperature_c",
    "co2_emissions_mt",
    "climate_risk_score",
    "sea_level_rise_mm",
    "heatwave_days",
    "temperature_change_c",
]

SUMMARY_COLUMNS = [
    "avg_temperature_c",
    "co2_emissions_mt",
    "sea_level_rise_mm",
    "heatwave_days",
    "climate_risk_score",
]

PROFILE_COLUMNS = [
    "avg_temperature_c",
    "temperature_change_c",
    "co2_emissions_mt",
    "sea_level_rise_mm",
    "heatwave_days",
    "wildfire_incidents",
    "air_quality_index",
    "climate_risk_score",
    "population_affected_m",
]


def dataframe_head(df: pd.DataFrame, rows: int = 10) -> pd.DataFrame:
    return df.head(rows)


def missing_values(df: pd.DataFrame) -> pd.Series:
    return df.isnull().sum()


def duplicate_count(df: pd.DataFrame) -> int:
    return int(df.duplicated().sum())


def descriptive_statistics(df: pd.DataFrame) -> pd.DataFrame:
    return df.describe().round(2)


def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    return df[CORRELATION_COLUMNS].corr()


def region_risk_statistics(df: pd.DataFrame) -> pd.DataFrame:
    region_stats = (
        df.groupby("region")["climate_risk_score"]
        .agg(["mean", "std", "count"])
        .reset_index()
    )
    region_stats.columns = ["region", "mean_risk", "std_risk", "count"]
    return region_stats.sort_values("mean_risk", ascending=False)


def flood_drought_crosstab(df: pd.DataFrame) -> pd.DataFrame:
    return pd.crosstab(df["flood_risk"], df["drought_risk"])


def heatwave_region_order(df: pd.DataFrame) -> list[str]:
    return (
        df.groupby("region")["heatwave_days"]
        .median()
        .sort_values(ascending=False)
        .index.tolist()
    )


def top_countries_by_risk(df: pd.DataFrame, limit: int = 10) -> pd.DataFrame:
    return (
        df.groupby("country")["climate_risk_score"]
        .mean()
        .sort_values(ascending=False)
        .head(limit)
        .reset_index()
    )


def regional_summary(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("region")[SUMMARY_COLUMNS].mean().round(2)


def climate_risk_groups(df: pd.DataFrame) -> list[pd.Series]:
    return [df[df["region"] == region]["climate_risk_score"].values for region in df["region"].unique()]


def risk_driver_rankings(df: pd.DataFrame) -> pd.DataFrame:
    correlations = (
        df[CORRELATION_COLUMNS]
        .corr(numeric_only=True)["climate_risk_score"]
        .drop("climate_risk_score")
        .sort_values(key=lambda series: series.abs(), ascending=False)
        .reset_index()
    )
    correlations.columns = ["feature", "correlation"]
    correlations["abs_correlation"] = correlations["correlation"].abs()
    correlations["direction"] = correlations["correlation"].map(
        lambda value: "Positive" if value >= 0 else "Negative"
    )
    return correlations


def regional_profile(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("region")[PROFILE_COLUMNS].mean().round(2)


def standardized_regional_profile(df: pd.DataFrame) -> pd.DataFrame:
    profile = regional_profile(df)
    standardized = (profile - profile.mean()) / profile.std(ddof=0)
    return standardized.round(2)


def risk_tiers(df: pd.DataFrame) -> pd.Series:
    return pd.qcut(
        df["climate_risk_score"],
        q=4,
        labels=["Low", "Moderate", "High", "Extreme"],
        duplicates="drop",
    )


def risk_tier_summary(df: pd.DataFrame) -> pd.DataFrame:
    tiered = df.assign(risk_tier=risk_tiers(df))
    summary = (
        tiered.groupby("risk_tier", observed=False)[
            ["temperature_change_c", "sea_level_rise_mm", "population_affected_m", "heatwave_days"]
        ]
        .mean()
        .round(2)
    )
    summary["records"] = tiered["risk_tier"].value_counts().reindex(summary.index).astype(int)
    return summary.reset_index()


def top_climate_hotspots(df: pd.DataFrame, limit: int = 12) -> pd.DataFrame:
    columns = [
        "country",
        "region",
        "climate_risk_score",
        "population_affected_m",
        "temperature_change_c",
        "sea_level_rise_mm",
        "heatwave_days",
        "wildfire_incidents",
    ]
    return df.nlargest(limit, "climate_risk_score")[columns].reset_index(drop=True)


def multi_hazard_hotspots(df: pd.DataFrame, quantile: float = 0.95, limit: int = 15) -> pd.DataFrame:
    hazard_columns = [
        "temperature_change_c",
        "sea_level_rise_mm",
        "heatwave_days",
        "wildfire_incidents",
        "population_affected_m",
    ]
    thresholds = df[hazard_columns].quantile(quantile)
    flags = df[hazard_columns].ge(thresholds, axis=1)
    hotspot_frame = df.loc[flags.any(axis=1), ["country", "region", "climate_risk_score", *hazard_columns]].copy()
    hotspot_frame["extreme_indicator_count"] = flags.sum(axis=1).loc[hotspot_frame.index]
    return hotspot_frame.sort_values(
        ["extreme_indicator_count", "climate_risk_score"],
        ascending=[False, False],
    ).head(limit).reset_index(drop=True)
