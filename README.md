# Global Climate Change and Extreme Weather Impact

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange)
![License](https://img.shields.io/badge/License-MIT-green)

This project presents a detailed climate data analysis built around a Jupyter notebook and a reusable Python analysis package. Using a 5,000-record global dataset, the project examines climate risk patterns through descriptive statistics, visual exploration, regional comparison, hazard profiling, hotspot detection, and statistical testing.

## Overview

The notebook is designed as a structured analytical report. It begins with dataset validation, moves through exploratory and comparative analysis, and concludes with region-level interpretation supported by statistical evidence.

Core goals of the project:

- understand the structure and quality of the dataset
- compare key climate indicators across regions
- investigate how climate risk relates to other variables
- identify notable countries and multi-hazard records
- present results through clear plots, tables, and interpretation notes

## Key Findings

- The dataset is clean, with no missing values and no duplicate rows.
- Climate risk is broadly distributed across regions rather than concentrated in a single geography.
- Individual variables show only weak direct relationships with climate risk score, suggesting a multi-factor pattern.
- Regional comparisons reveal subtle profile differences, but statistical tests do not show strong between-region significance.
- Hotspot and ranking views remain useful for identifying standout countries and extreme records.

## Main Files

- Notebook with saved outputs: [ClimateChangeAnalysis.ipynb](./ClimateChangeAnalysis.ipynb)
- Pre-executed copy: [ClimateChangeAnalysis_Executed.ipynb](./ClimateChangeAnalysis_Executed.ipynb)
- Dataset: [dataset.csv](./dataset.csv)

## Screenshots And Viewing

- Open [ClimateChangeAnalysis_Executed.ipynb](./ClimateChangeAnalysis_Executed.ipynb) if you want to review the notebook with saved outputs already included.
- Open [ClimateChangeAnalysis.ipynb](./ClimateChangeAnalysis.ipynb) if you want the main editable notebook version.
- The notebook uses dark-themed visual styling, so it looks best in a notebook viewer that supports rendered outputs clearly.

## Analysis Areas

- Dataset overview and schema inspection
- Data quality assessment
- Descriptive statistics
- Correlation analysis and risk-driver ranking
- Distribution analysis of key variables
- Regional comparison and climate-risk profiling
- CO2 emissions and temperature-change relationship
- Flood and drought co-occurrence analysis
- Heatwave and sea-level regional comparison
- Exposure segmentation by risk tier
- Top-country ranking and hotspot detection
- Regional summary table with companion visualization
- Statistical significance testing across regions

## Visual Features

The notebook includes:

- executive-style summary cards
- styled tables for cleaner tabular presentation
- dark-themed analytical plots
- donut, pie, bar, heatmap, scatter, violin, box, stacked, and radar-style comparisons
- explanatory callouts after major analysis sections

## Project Structure

```text
Notebook project/
|-- ClimateChangeAnalysis.ipynb
|-- ClimateChangeAnalysis_Executed.ipynb
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

## Python Package Modules

- `config.py`: shared plotting theme and console section formatting
- `data_loader.py`: dataset loading helpers
- `notebook_utils.py`: notebook-specific styled display components
- `plots.py`: reusable visualization functions
- `statistics.py`: regression and hypothesis-testing helpers
- `summaries.py`: tabular summaries and grouped analytical views
- `pipeline.py`: end-to-end reusable workflow outside the notebook

## Setup

Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

To open the notebook:

```bash
jupyter lab
```

To run the reusable pipeline directly:

```bash
python -c "from climate_analysis import run_analysis; run_analysis('dataset.csv')"
```

## Validation

The notebook and analysis pipeline were executed successfully after the final update. Validation confirmed that:

- imports resolve correctly
- notebook cells execute without errors
- plots render and save into notebook outputs
- tables and styled callouts display correctly
- statistical tests complete as expected

## Author

- Author: MdAsifuzzamanAsif9

## License

This project is released under the MIT License. See [LICENSE](./LICENSE).
