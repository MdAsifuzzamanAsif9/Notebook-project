"""Plotting helpers for the climate analysis workflow."""

from __future__ import annotations

from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from IPython.display import Image, display

from .config import ACCENT5, BORDER, CARD_BG, DARK_BG, PALETTE, TEXT_PRI, TEXT_SEC


def _render_plot(fig: plt.Figure) -> None:
    """Render plots in notebooks and preserve outputs for headless notebook execution."""
    if "agg" in plt.get_backend().lower():
        buffer = BytesIO()
        fig.savefig(buffer, format="png", bbox_inches="tight", facecolor=fig.get_facecolor(), dpi=160)
        buffer.seek(0)
        display(Image(data=buffer.getvalue()))
        buffer.close()
        plt.close(fig)
        return
    plt.show()


def plot_correlation_heatmap(correlation: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(CARD_BG)
    mask = np.triu(np.ones_like(correlation, dtype=bool))
    cmap = sns.diverging_palette(220, 20, as_cmap=True)
    sns.heatmap(
        correlation,
        mask=mask,
        cmap=cmap,
        vmax=1,
        vmin=-1,
        center=0,
        annot=True,
        fmt=".2f",
        linewidths=0.5,
        linecolor=BORDER,
        annot_kws={"size": 8, "color": TEXT_PRI},
        cbar_kws={"shrink": 0.8},
        ax=ax,
    )
    ax.set_title("Feature Correlation Heatmap", fontsize=14, fontweight="bold", color=TEXT_PRI, pad=15)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    _render_plot(fig)


def plot_distributions(df: pd.DataFrame, columns: list[str]) -> None:
    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    fig.patch.set_facecolor(DARK_BG)
    fig.suptitle(
        "Distribution of Key Climate Variables",
        fontsize=15,
        fontweight="bold",
        color=TEXT_PRI,
        y=1.01,
    )
    for index, (column, ax) in enumerate(zip(columns, axes.flat)):
        ax.set_facecolor(CARD_BG)
        ax.hist(
            df[column].dropna(),
            bins=40,
            color=PALETTE[index % len(PALETTE)],
            edgecolor=DARK_BG,
            alpha=0.85,
        )
        ax.set_title(column.replace("_", " ").title(), color=TEXT_PRI, fontsize=11)
    plt.tight_layout()
    _render_plot(fig)


def plot_region_risk(region_stats: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(11, 6))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(CARD_BG)
    bars = ax.barh(
        region_stats["region"],
        region_stats["mean_risk"],
        color=PALETTE[: len(region_stats)],
        edgecolor=DARK_BG,
        height=0.55,
    )
    ax.errorbar(
        region_stats["mean_risk"],
        region_stats["region"],
        xerr=region_stats["std_risk"],
        fmt="none",
        color=TEXT_SEC,
        capsize=4,
    )
    ax.set_xlabel("Mean Climate Risk Score", color=TEXT_PRI, fontsize=12)
    ax.set_title(
        "Mean Climate Risk Score by Region (with Std Dev)",
        fontsize=13,
        fontweight="bold",
        color=TEXT_PRI,
        pad=12,
    )
    ax.xaxis.grid(True, linestyle="--", alpha=0.4)
    for bar, value in zip(bars, region_stats["mean_risk"]):
        ax.text(value + 0.8, bar.get_y() + bar.get_height() / 2, f"{value:.1f}", va="center", color=TEXT_PRI, fontsize=10)
    plt.tight_layout()
    _render_plot(fig)


def plot_co2_vs_temperature(df: pd.DataFrame, regression: dict[str, float]) -> None:
    fig, ax = plt.subplots(figsize=(11, 7))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(CARD_BG)
    for index, region in enumerate(df["region"].unique()):
        subset = df[df["region"] == region]
        ax.scatter(
            subset["co2_emissions_mt"],
            subset["temperature_change_c"],
            color=PALETTE[index % len(PALETTE)],
            alpha=0.5,
            s=18,
            label=region,
        )
    x_values = np.linspace(df["co2_emissions_mt"].min(), df["co2_emissions_mt"].max(), 300)
    ax.plot(
        x_values,
        regression["slope"] * x_values + regression["intercept"],
        color=ACCENT5,
        linewidth=2,
        linestyle="--",
        label=f"Regression (r={regression['r_value']:.3f})",
    )
    ax.set_xlabel("CO2 Emissions (MT)", fontsize=12)
    ax.set_ylabel("Temperature Change (C)", fontsize=12)
    ax.set_title(
        "CO2 Emissions vs. Temperature Change by Region",
        fontsize=13,
        fontweight="bold",
        color=TEXT_PRI,
        pad=12,
    )
    ax.legend(facecolor=CARD_BG, edgecolor=BORDER, labelcolor=TEXT_PRI, fontsize=9, ncol=2)
    plt.tight_layout()
    _render_plot(fig)


def plot_flood_drought_heatmap(risk_table: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(CARD_BG)
    sns.heatmap(
        risk_table,
        annot=True,
        fmt="d",
        cmap="YlOrRd",
        linewidths=0.5,
        linecolor=BORDER,
        ax=ax,
        annot_kws={"size": 12, "fontweight": "bold"},
    )
    ax.set_title("Flood Risk vs. Drought Risk Record Count", fontsize=13, fontweight="bold", color=TEXT_PRI, pad=12)
    ax.set_xlabel("Drought Risk", fontsize=11)
    ax.set_ylabel("Flood Risk", fontsize=11)
    plt.tight_layout()
    _render_plot(fig)


def plot_heatwave_boxplot(df: pd.DataFrame, region_order: list[str]) -> None:
    data_by_region = [df[df["region"] == region]["heatwave_days"].values for region in region_order]
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(CARD_BG)
    boxplot = ax.boxplot(
        data_by_region,
        patch_artist=True,
        notch=False,
        medianprops={"color": ACCENT5, "linewidth": 2.5},
        whiskerprops={"color": TEXT_SEC},
        capprops={"color": TEXT_SEC},
        flierprops={"marker": "o", "markerfacecolor": TEXT_SEC, "markersize": 4, "alpha": 0.5},
    )
    for patch, color in zip(boxplot["boxes"], PALETTE):
        patch.set_facecolor(color)
        patch.set_alpha(0.75)
    ax.set_xticklabels(region_order, color=TEXT_PRI, fontsize=10, rotation=20, ha="right")
    ax.set_ylabel("Heatwave Days", fontsize=12)
    ax.set_title("Distribution of Heatwave Days by Region", fontsize=13, fontweight="bold", color=TEXT_PRI, pad=12)
    ax.yaxis.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()
    _render_plot(fig)


def plot_top_countries(top_countries: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(11, 6))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(CARD_BG)
    bars = ax.bar(
        top_countries["country"],
        top_countries["climate_risk_score"],
        color=[PALETTE[index % len(PALETTE)] for index in range(len(top_countries))],
        edgecolor=DARK_BG,
        width=0.6,
    )
    ax.set_ylabel("Mean Climate Risk Score", fontsize=12)
    ax.set_title("Top 10 Countries by Mean Climate Risk Score", fontsize=13, fontweight="bold", color=TEXT_PRI, pad=12)
    ax.set_xticks(range(len(top_countries["country"])))
    ax.set_xticklabels(top_countries["country"], rotation=30, ha="right")
    for bar, value in zip(bars, top_countries["climate_risk_score"]):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.5, f"{value:.1f}", ha="center", va="bottom", fontsize=9)
    ax.yaxis.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()
    _render_plot(fig)


def plot_sea_level_violin(df: pd.DataFrame, region_order: list[str]) -> None:
    violin_data = [df[df["region"] == region]["sea_level_rise_mm"].values for region in region_order]
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(CARD_BG)
    violin = ax.violinplot(violin_data, positions=range(1, len(region_order) + 1), showmedians=True, showextrema=True)
    for patch, color in zip(violin["bodies"], PALETTE):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
    violin["cmedians"].set_color(ACCENT5)
    violin["cmedians"].set_linewidth(2)
    ax.set_xticks(range(1, len(region_order) + 1))
    ax.set_xticklabels(region_order, rotation=20, ha="right", fontsize=10)
    ax.set_ylabel("Sea Level Rise (mm)", fontsize=12)
    ax.set_title("Sea Level Rise Distribution by Region", fontsize=13, fontweight="bold", color=TEXT_PRI, pad=12)
    ax.yaxis.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()
    _render_plot(fig)


def plot_risk_driver_rankings(rankings: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(CARD_BG)
    colors = [ACCENT5 if value >= 0 else "#f87171" for value in rankings["correlation"]]
    ax.barh(rankings["feature"], rankings["correlation"], color=colors, edgecolor=DARK_BG)
    ax.axvline(0, color=TEXT_SEC, linewidth=1.2)
    ax.set_xlabel("Pearson Correlation with Climate Risk Score", fontsize=12)
    ax.set_title("Risk Driver Ranking", fontsize=13, fontweight="bold", color=TEXT_PRI, pad=12)
    ax.xaxis.grid(True, linestyle="--", alpha=0.3)
    ax.invert_yaxis()
    plt.tight_layout()
    _render_plot(fig)


def plot_regional_profile_heatmap(profile: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(CARD_BG)
    sns.heatmap(
        profile,
        cmap=sns.diverging_palette(145, 10, as_cmap=True),
        center=0,
        annot=True,
        fmt=".2f",
        linewidths=0.5,
        linecolor=BORDER,
        cbar_kws={"label": "Standard Deviations from Global Mean"},
        annot_kws={"size": 8},
        ax=ax,
    )
    ax.set_title("Standardized Regional Climate Profile", fontsize=13, fontweight="bold", color=TEXT_PRI, pad=12)
    ax.set_xlabel("")
    ax.set_ylabel("")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    _render_plot(fig)


def plot_vulnerability_scatter(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(11, 7))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(CARD_BG)
    scatter = ax.scatter(
        df["sea_level_rise_mm"],
        df["population_affected_m"],
        c=df["climate_risk_score"],
        s=df["heatwave_days"] * 2.2,
        cmap="magma",
        alpha=0.65,
        edgecolors="none",
    )
    ax.set_xlabel("Sea Level Rise (mm)", fontsize=12)
    ax.set_ylabel("Population Affected (millions)", fontsize=12)
    ax.set_title(
        "Exposure Landscape: Sea Level Rise vs. Population Affected",
        fontsize=13,
        fontweight="bold",
        color=TEXT_PRI,
        pad=12,
    )
    ax.grid(True, linestyle="--", alpha=0.25)
    cbar = fig.colorbar(scatter, ax=ax, shrink=0.85)
    cbar.set_label("Climate Risk Score", color=TEXT_PRI)
    cbar.ax.yaxis.set_tick_params(color=TEXT_SEC)
    plt.tight_layout()
    _render_plot(fig)


def plot_risk_tier_profiles(summary: pd.DataFrame) -> None:
    metrics = ["temperature_change_c", "sea_level_rise_mm", "population_affected_m", "heatwave_days"]
    fig, ax = plt.subplots(figsize=(11, 6))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(CARD_BG)
    x = np.arange(len(summary["risk_tier"]))
    width = 0.18
    for index, metric in enumerate(metrics):
        ax.bar(
            x + (index - 1.5) * width,
            summary[metric],
            width=width,
            color=PALETTE[index],
            label=metric.replace("_", " ").title(),
            alpha=0.9,
        )
    ax.set_xticks(x)
    ax.set_xticklabels(summary["risk_tier"])
    ax.set_title("Average Exposure by Climate Risk Tier", fontsize=13, fontweight="bold", color=TEXT_PRI, pad=12)
    ax.legend(facecolor=CARD_BG, edgecolor=BORDER, labelcolor=TEXT_PRI, fontsize=9)
    ax.yaxis.grid(True, linestyle="--", alpha=0.25)
    plt.tight_layout()
    _render_plot(fig)
