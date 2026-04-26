"""Top-level analysis pipeline built from reusable modules."""

from __future__ import annotations

from pathlib import Path

from .config import configure_theme, print_section
from .data_loader import load_dataset
from .plots import (
    plot_co2_vs_temperature,
    plot_correlation_heatmap,
    plot_distributions,
    plot_flood_drought_heatmap,
    plot_heatwave_boxplot,
    plot_regional_profile_heatmap,
    plot_region_risk,
    plot_risk_driver_rankings,
    plot_risk_tier_profiles,
    plot_sea_level_violin,
    plot_top_countries,
    plot_vulnerability_scatter,
)
from .statistics import kruskal_wallis, linear_regression_results, one_way_anova, spearman_correlation
from .summaries import (
    DISTRIBUTION_COLUMNS,
    climate_risk_groups,
    correlation_matrix,
    dataframe_head,
    descriptive_statistics,
    duplicate_count,
    flood_drought_crosstab,
    heatwave_region_order,
    risk_driver_rankings,
    risk_tier_summary,
    missing_values,
    region_risk_statistics,
    regional_summary,
    standardized_regional_profile,
    multi_hazard_hotspots,
    top_countries_by_risk,
    top_climate_hotspots,
)


def run_analysis(dataset_path: str | Path = "dataset.csv") -> None:
    """Run the complete climate analysis workflow."""
    configure_theme()
    print("Libraries loaded and theme configured.")

    df = load_dataset(dataset_path)

    print_section("Dataset Overview")
    print(f"Dataset shape: {df.shape}\n")
    print(df.dtypes)

    print_section("First 10 Rows")
    print(dataframe_head(df).to_string(index=False))

    print_section("Data Quality")
    missing = missing_values(df)
    print("Missing values per column:")
    print(missing.to_string())
    print(f"\nTotal missing: {missing.sum()}")
    print(f"Duplicate rows: {duplicate_count(df)}")

    print_section("Descriptive Statistics")
    print(descriptive_statistics(df).to_string())

    print_section("Correlation Heatmap")
    plot_correlation_heatmap(correlation_matrix(df))

    print_section("Distributions")
    plot_distributions(df, DISTRIBUTION_COLUMNS)

    print_section("Regional Risk Statistics")
    region_stats = region_risk_statistics(df)
    print(region_stats.round(2).to_string(index=False))
    plot_region_risk(region_stats)

    print_section("CO2 vs Temperature")
    regression = linear_regression_results(df)
    print(f"slope     = {regression['slope']:.6f}")
    print(f"intercept = {regression['intercept']:.4f}")
    print(f"r         = {regression['r_value']:.4f}")
    print(f"p-value   = {regression['p_value']:.6f}")
    print(f"std err   = {regression['std_err']:.6f}")
    plot_co2_vs_temperature(df, regression)
    spearman = spearman_correlation(df, "co2_emissions_mt", "temperature_change_c")
    print(f"Spearman rho = {spearman['coefficient']:.4f}")
    print(f"Spearman p   = {spearman['p_value']:.6f}")

    print_section("Flood and Drought Risk")
    risk_table = flood_drought_crosstab(df)
    print(risk_table.to_string())
    plot_flood_drought_heatmap(risk_table)

    print_section("Heatwave Days by Region")
    region_order = heatwave_region_order(df)
    plot_heatwave_boxplot(df, region_order)

    print_section("Top Countries by Risk")
    top_countries = top_countries_by_risk(df)
    print(top_countries.round(2).to_string(index=False))
    plot_top_countries(top_countries)

    print_section("Sea Level Rise by Region")
    plot_sea_level_violin(df, region_order)

    print_section("Risk Driver Ranking")
    plot_risk_driver_rankings(risk_driver_rankings(df))

    print_section("Regional Climate Profile")
    plot_regional_profile_heatmap(standardized_regional_profile(df))

    print_section("Exposure Landscape")
    plot_vulnerability_scatter(df)

    print_section("Risk Tier Profile")
    tier_summary = risk_tier_summary(df)
    print(tier_summary.to_string(index=False))
    plot_risk_tier_profiles(tier_summary)

    print_section("Extreme Climate Hotspots")
    print(top_climate_hotspots(df).to_string(index=False))

    print_section("Multi-Hazard Hotspots")
    print(multi_hazard_hotspots(df).to_string(index=False))

    print_section("Statistical Tests")
    groups = climate_risk_groups(df)
    anova = one_way_anova(groups)
    print(f"F-statistic = {anova['f_statistic']:.4f}")
    print(f"p-value     = {anova['p_value']:.6f}")
    print(f"Conclusion  = {anova['conclusion']}")

    kruskal = kruskal_wallis(groups)
    print(f"H-statistic = {kruskal['h_statistic']:.4f}")
    print(f"p-value     = {kruskal['p_value']:.6f}")
    print(f"Conclusion  = {kruskal['conclusion']}")

    print_section("Regional Summary")
    print(regional_summary(df).to_string())
