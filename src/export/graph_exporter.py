"""Sauvegarde une figure matplotlib dans graphique/, en PNG haute
résolution — utilisé par le script CLI et par le bouton d'export de l'app.
"""

import matplotlib.pyplot as plt

from src.config import GRAPHIQUE_DIR


def save_figure(fig: plt.Figure, filename: str) -> str:
    GRAPHIQUE_DIR.mkdir(exist_ok=True)
    chemin = GRAPHIQUE_DIR / filename
    fig.savefig(chemin, dpi=150, bbox_inches="tight")
    return str(chemin)
