"""Graphique 2 — Comparaison de groupes : quel poste est le plus rapide
dans la sélection ?
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.config import COLOR_SELECTION


def build_pac_by_position_chart(sel: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(4.3, 3.2), dpi=120)
    if not sel.empty:
        order = sel.groupby("Position")["PAC"].median().sort_values(ascending=False).index
        sns.boxplot(data=sel, x="Position", y="PAC", order=order, color=COLOR_SELECTION, ax=ax)
        # Avec plus de 5-6 postes, les libellés horizontaux se chevauchent :
        # on les incline pour garder chaque poste lisible sans agrandir le graphique.
        if len(order) > 5:
            plt.setp(ax.get_xticklabels(), rotation=40, ha="right", fontsize=7)
        else:
            ax.tick_params(axis="x", labelsize=8)

    ax.set_title("PAC par poste (sélection)", fontsize=10)
    ax.set_xlabel("Poste", fontsize=8)
    ax.set_ylabel("PAC", fontsize=8)
    ax.tick_params(axis="y", labelsize=8)
    fig.tight_layout()
    return fig