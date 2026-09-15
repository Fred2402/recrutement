"""Graphique 6 — Toutes les relations d'un coup : corrélations entre les
statistiques clés, au sein de la sélection courante.
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

from src.config import COLOR_ACCENT, COLOR_SELECTION, STATS_CLES

_DIV_CMAP = LinearSegmentedColormap.from_list("div", [COLOR_ACCENT, "#F8FAFC", COLOR_SELECTION])


def build_correlation_heatmap_chart(sel: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(4.6, 4.1), dpi=120)
    if len(sel) < 3:
        ax.set_title("Sélection trop petite pour calculer des corrélations", fontsize=9)
        return fig

    corr = sel[STATS_CLES].corr()
    sns.heatmap(corr, cmap=_DIV_CMAP, center=0, annot=True, fmt=".2f",
                annot_kws={"size": 6.5}, square=True, ax=ax, linewidths=0.5, linecolor="white",
                cbar_kws={"shrink": 0.75})
    ax.set_title("Corrélations entre statistiques (sélection)", fontsize=10)
    ax.tick_params(labelsize=7)
    fig.tight_layout()
    return fig