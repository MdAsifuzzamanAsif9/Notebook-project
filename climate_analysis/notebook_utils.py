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
    border-left:5px solid #0ea5e9;
    background: linear-gradient(180deg, #f8fbff, #eef6ff);
    color:#0f172a;
    border-radius:16px;
    padding:16px 18px;
    margin:14px 0;
    box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08);
    border-top:1px solid rgba(14, 165, 233, 0.18);
    border-right:1px solid rgba(14, 165, 233, 0.18);
    border-bottom:1px solid rgba(14, 165, 233, 0.18);
}
@media (prefers-color-scheme: dark) {
    .cc-callout {
        background: linear-gradient(180deg, #0f172a, #132238);
        color:#e2e8f0;
        box-shadow: 0 14px 30px rgba(2, 6, 23, 0.28);
        border-top:1px solid rgba(125, 211, 252, 0.16);
        border-right:1px solid rgba(125, 211, 252, 0.16);
        border-bottom:1px solid rgba(125, 211, 252, 0.16);
    }
}
.cc-grid-title {
    margin: 8px 0 12px 0;
    font-size: 18px;
    font-weight: 700;
    color: #f8fafc;
}
.cc-insight-grid {
    display:grid;
    grid-template-columns:repeat(auto-fit, minmax(220px, 1fr));
    gap:14px;
    margin:10px 0 24px 0;
}
.cc-insight-card {
    background: linear-gradient(180deg, rgba(15,23,42,0.94), rgba(17,24,39,0.98));
    border:1px solid rgba(148,163,184,0.16);
    border-radius:18px;
    padding:18px 18px 16px 18px;
    min-height: 148px;
}
.cc-insight-tag {
    display:inline-block;
    padding:4px 9px;
    border-radius:999px;
    background:rgba(56,189,248,0.12);
    color:#93c5fd;
    font-size:11px;
    letter-spacing:0.06em;
    text-transform:uppercase;
    margin-bottom:10px;
}
.cc-insight-title {
    font-size:16px;
    font-weight:700;
    color:#f8fafc;
    margin-bottom:8px;
}
.cc-insight-body {
    font-size:13px;
    line-height:1.65;
    color:#cbd5e1;
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
        <div style="font-weight:700; color:inherit; margin-bottom:6px; font-size:15px;">{title}</div>
        <div style="line-height:1.7; color:inherit; opacity:0.95; font-size:14px;">{body}</div>
      </div>
    </div>
    """
    display(HTML(html))


def display_insight_grid(title: str, cards: list[dict[str, str]]) -> None:
    blocks = "".join(
        f"""
        <div class="cc-insight-card">
          <div class="cc-insight-tag">{card["tag"]}</div>
          <div class="cc-insight-title">{card["title"]}</div>
          <div class="cc-insight-body">{card["body"]}</div>
        </div>
        """
        for card in cards
    )
    html = f"""
    {DATAFRAME_CSS}
    <div class="cc-shell">
      <div class="cc-grid-title">{title}</div>
      <div class="cc-insight-grid">{blocks}</div>
    </div>
    """
    display(HTML(html))
