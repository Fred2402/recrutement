"""Graphique 5 — Classement : quel championnat porte les meilleurs profils
de la sélection ? Barres en dégradé, triées, jamais tronquées à zéro.

Filet de sécurité : même si `sel` a déjà été filtrée en amont, les
championnats de `excluded_leagues` sont explicitement retirés ici avant
tout calcul, et une note en bas du graphique confirme lesquels ont été
exclus — pour que l'exclusion reste visible même sur un export PNG/PDF
détaché de l'application.
"""

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

from src.config import COLOR_SELECTION

_GRAD = LinearSegmentedColormap.from_list("grad", ["#eef3fa", COLOR_SELECTION])


def build_league_ranking_chart(
    sel: pd.DataFrame,
    stat: str = "OVR",
    top_n: int = 10,
    excluded_leagues: list[str] = None,
) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(6, 5))

    excluded_leagues = excluded_leagues or []
    if excluded_leagues:
        sel = sel[~sel["League"].isin(excluded_leagues)]

    if sel.empty:
        ax.set_title(f"Aucun joueur pour classer par {stat}")
        return fig

    classement = sel.groupby("League")[stat].mean().sort_values(ascending=False).head(top_n)
    norm = (classement.values - classement.values.min()) / (
        classement.values.max() - classement.values.min() + 1e-9
    )
    couleurs = [_GRAD(0.3 + 0.7 * v) for v in norm]

    bars = ax.barh(classement.index[::-1], classement.values[::-1], color=couleurs[::-1])
    ax.bar_label(bars, fmt="%.1f", padding=3)
    ax.set_xticks([])
    ax.set_title(f"{stat} moyen par championnat (sélection)")

    if excluded_leagues:
        note = "Exclus de ce classement : " + ", ".join(excluded_leagues)
        fig.text(0.01, -0.02, note, fontsize=7.5, color="#888888", style="italic", wrap=True)

    fig.tight_layout()
    return fig
