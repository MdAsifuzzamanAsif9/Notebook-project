"""Notebook-specific display helpers."""

from __future__ import annotations

from IPython.display import HTML, display
import pandas as pd

DATAFRAME_CSS = """
<style>
.dataframe {border-collapse:collapse; font-family:'Segoe UI',sans-serif;
            font-size:12px; width:100%; border-radius:14px; overflow:hidden;}
.dataframe th {background:#1f2937; color:#8ec5ff; padding:10px 12px;
               border:1px solid #30363d; text-align:left;}
.dataframe td {color:#e6edf3; padding:8px 12px; border:1px solid #30363d;}
.dataframe tr:nth-child(even) td {background:#111827;}
.dataframe tr:hover td {background:#172033;}

.cc-shell {font-family:'Segoe UI',sans-serif; color:#e6edf3;}
.cc-hero {
    background: radial-gradient(circle at top left, rgba(56,189,248,0.25), transparent 30%),
                linear-gradient(135deg, #0f172a, #111827 45%, #1d4ed8);
    border: 1px solid rgba(148,163,184,0.25);
    border-radius: 24px;
    padding: 28px 30px;
    margin: 8px 0 24px 0;
    box-shadow: 0 20px 45px rgba(15, 23, 42, 0.35);
}
.cc-kpi-grid {
    display:grid;
    grid-template-columns:repeat(auto-fit, minmax(180px, 1fr));
    gap:14px;
    margin:18px 0 24px 0;
}
.cc-kpi {
    background: linear-gradient(180deg, rgba(15,23,42,0.92), rgba(30,41,59,0.95));
    border:1px solid rgba(148,163,184,0.18);
    border-radius:18px;
    padding:18px 20px;
}
.cc-kpi-label {font-size:12px; text-transform:uppercase; letter-spacing:0.08em; color:#93c5fd;}
.cc-kpi-value {font-size:28px; font-weight:700; margin-top:8px; color:#f8fafc;}
.cc-kpi-note {font-size:12px; color:#cbd5e1; margin-top:6px;}
.cc-callout {
    border-left:4px solid #38bdf8;
    background:#0f172a;
    border-radius:14px;
    padding:16px 18px;
    margin:14px 0;
}
</style>
"""


def display_styled_table(dataframe: pd.DataFrame, *, index: bool = True) -> None:
    """Render a DataFrame in the notebook with the shared dark-table styling."""
    html = dataframe.to_html(index=index, border=0, classes="dataframe")
    display(HTML(DATAFRAME_CSS + html))


def display_hero(title: str, subtitle: str, details: str) -> None:
    html = f"""
    {DATAFRAME_CSS}
    <div class="cc-shell">
      <div class="cc-hero">
        <div style="font-size:13px; letter-spacing:0.18em; text-transform:uppercase; color:#bfdbfe;">Climate Intelligence Notebook</div>
        <h1 style="margin:10px 0 12px 0; font-size:34px;">{title}</h1>
        <p style="margin:0 0 10px 0; font-size:16px; line-height:1.6; max-width:880px;">{subtitle}</p>
        <p style="margin:0; color:#dbeafe; font-size:13px;">{details}</p>
      </div>
    </div>
    """
    display(HTML(html))


def display_kpis(cards: list[dict[str, str]]) -> None:
    blocks = "".join(
        f"""
        <div class="cc-kpi">
          <div class="cc-kpi-label">{card["label"]}</div>
          <div class="cc-kpi-value">{card["value"]}</div>
          <div class="cc-kpi-note">{card["note"]}</div>
        </div>
        """
        for card in cards
    )
    display(HTML(f"{DATAFRAME_CSS}<div class='cc-shell'><div class='cc-kpi-grid'>{blocks}</div></div>"))


def display_callout(title: str, body: str) -> None:
    html = f"""
    {DATAFRAME_CSS}
    <div class="cc-shell">
      <div class="cc-callout">
        <div style="font-weight:700; color:#e0f2fe; margin-bottom:6px;">{title}</div>
        <div style="line-height:1.6; color:#cbd5e1;">{body}</div>
      </div>
    </div>
    """
    display(HTML(html))
