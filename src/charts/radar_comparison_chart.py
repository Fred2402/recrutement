"""Graphique 4 — Comparateur de joueurs (radar) : la carte de scouting
classique, pour 2 ou 3 joueurs maximum (au-delà, illisible — cf. cours).

La légende est placée SOUS le radar plutôt qu'en biais à l'extérieur : sur
un petit format, un décalage type bbox_to_anchor=(1.3, 1.1) sort largement
du canevas et se fait couper ou chevaucher le titre.
"""

from math import pi

import matplotlib.pyplot as plt
import pandas as pd

from src.config import COLOR_ACCENT, COLOR_SELECTION
from src.config import STATS_CLES as RADAR_STATS


def build_radar_comparison_chart(df: pd.DataFrame, noms_joueurs: list[str]) -> plt.Figure:
    """Superpose le profil de 2 ou 3 joueurs sur les mêmes axes (STATS_CLES)."""
    angles = [n / float(len(RADAR_STATS)) * 2 * pi for n in range(len(RADAR_STATS))]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(4.3, 4.6), dpi=120, subplot_kw=dict(polar=True))
    palette = [COLOR_SELECTION, COLOR_ACCENT, "#10B981"]

    for nom, couleur in zip(noms_joueurs[:3], palette):
        ligne = df[df["Name"] == nom]
        if ligne.empty:
            continue
        valeurs = ligne.iloc[0][RADAR_STATS].tolist()
        valeurs += valeurs[:1]
        ax.plot(angles, valeurs, label=nom, color=couleur, linewidth=2)
        ax.fill(angles, valeurs, alpha=0.1, color=couleur)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(RADAR_STATS, fontsize=8)
    ax.tick_params(axis="y", labelsize=6)
    ax.set_title("Comparateur de joueurs", pad=14, fontsize=10)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.08), ncol=3, fontsize=7,
              frameon=False, handletextpad=0.3, columnspacing=0.8)
    fig.tight_layout()
    return fig