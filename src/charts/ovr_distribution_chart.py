"""Graphique 1 — Distribution : où se place la sélection sur OVR ?

Sélection en couleur d'accent, reste du dataset en gris — même code couleur
que partout ailleurs dans l'application (voir src/config.py).
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.config import COLOR_BACKGROUND, COLOR_SELECTION


def build_ovr_distribution_chart(df_all: pd.DataFrame, sel: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(4, 2.9), dpi=120)
    sns.kdeplot(df_all["OVR"], color=COLOR_BACKGROUND, fill=True, label="Ensemble du dataset", ax=ax)
    if not sel.empty:
        sns.kdeplot(sel["OVR"], color=COLOR_SELECTION, fill=True, label="Sélection", ax=ax)
    ax.set_title("Distribution de OVR — sélection vs ensemble")
    ax.set_xlabel("OVR")
    ax.legend()
    fig.tight_layout()
    return fig
