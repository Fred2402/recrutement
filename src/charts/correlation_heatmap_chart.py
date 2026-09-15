"""Graphique 6 — Toutes les relations d'un coup : corrélations entre les
statistiques clés, au sein de la sélection courante.
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

from src.config import STATS_CLES

_DIV_CMAP = LinearSegmentedColormap.from_list("div", ["#e63946", "#f6f3ea", "#2a78d6"])


def build_correlation_heatmap_chart(sel: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(4.2, 3.6), dpi=120)
    if len(sel) < 3:
        ax.set_title("Sélection trop petite pour calculer des corrélations")
        return fig

    corr = sel[STATS_CLES].corr()
    sns.heatmap(corr, cmap=_DIV_CMAP, center=0, annot=True, fmt=".2f",
                annot_kws={"size": 8}, square=True, ax=ax, linewidths=0.5, linecolor="white")
    ax.set_title("Corrélations entre statistiques (sélection)")
    fig.tight_layout()
    return fig
