# Global Climate Change and Extreme Weather Impact

A polished data analysis project built around a submission-ready Jupyter notebook and a small reusable Python analysis package. The project explores a 5,000-record global climate dataset through descriptive analysis, correlation diagnostics, regional comparison, vulnerability profiling, hotspot detection, and statistical testing.

## Highlights

- Professional notebook presentation with KPI cards, styled tables, interpretation notes, and section-by-section conclusions
- Reusable analysis modules for plotting, summaries, statistics, data loading, and notebook display helpers
- Additional analysis depth including risk-driver rankings, standardized regional profiles, exposure segmentation, and multi-hazard hotspot detection
- Validation-ready workflow with data quality checks and hypothesis tests

## Main Notebook

- Notebook: [ClimateChangeAnalysis.ipynb](./ClimateChangeAnalysis.ipynb)
- Dataset: [dataset.csv](./dataset.csv)

## Project Structure

```text
Notebook project/
|-- ClimateChangeAnalysis.ipynb
|-- climate_analysis/
|   |-- __init__.py
|   |-- config.py
|   |-- data_loader.py
|   |-- notebook_utils.py
|   |-- pipeline.py
|   |-- plots.py
|   |-- statistics.py
|   `-- summaries.py
|-- dataset.csv
|-- requirements.txt
|-- README.md
`-- LICENSE
```

## Analyses Included

- Dataset structure and data quality assessment
- Descriptive statistics for key climate indicators
- Correlation heatmap and climate risk driver ranking
- Distribution analysis for major numerical features
- Regional climate risk comparison and standardized regional profile heatmap
- CO2 emissions vs. temperature change regression and Spearman correlation
- Flood-drought co-occurrence, heatwave spread, and sea-level rise distribution
- Exposure segmentation by climate risk tier
- Top countries by average climate risk and multi-hazard hotspot detection
- One-way ANOVA and Kruskal-Wallis regional significance testing

## Setup

```bash
pip install -r requirements.txt
```

## How To Run

Open the notebook in Jupyter:

```bash
jupyter lab
```

If you want to run the reusable Python pipeline outside the notebook:

```bash
python -c "from climate_analysis import run_analysis; run_analysis('dataset.csv')"
```

## Validation

The notebook and analysis pipeline were executed successfully after the final project cleanup to confirm that:

- imports resolve correctly
- all analysis sections run without errors
- charts render cleanly
- statistical tests execute as expected

## License

This project is released under the MIT License. See [LICENSE](./LICENSE).
