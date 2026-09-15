"""Graphique 2 — Comparaison de groupes : quel poste est le plus rapide
dans la sélection ?
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.config import COLOR_SELECTION


def build_pac_by_position_chart(sel: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(4, 2.9), dpi=120)
    if not sel.empty:
        order = sel.groupby("Position")["PAC"].median().sort_values(ascending=False).index
        sns.boxplot(data=sel, x="Position", y="PAC", order=order, color=COLOR_SELECTION, ax=ax)
    ax.set_title("PAC par poste (sélection)")
    ax.set_xlabel("Poste")
    ax.set_ylabel("PAC")
    fig.tight_layout()
    return fig
