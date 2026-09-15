"""Signale quand la sélection est trop petite pour que ses moyennes et
corrélations soient fiables — le piège des petits effectifs, identifié
dans le TP (questions 13 et 18), reporté ici dans l'application.
"""

import pandas as pd

SEUIL_FIABILITE = 10


def check_reliability(sel: pd.DataFrame) -> str | None:
    """Retourne un message d'avertissement si l'effectif est trop faible, sinon None."""
    if 0 < len(sel) < SEUIL_FIABILITE:
        return (
            f"Échantillon réduit ({len(sel)} joueur{'s' if len(sel) > 1 else ''}) : "
            "les moyennes et corrélations affichées sont à interpréter avec prudence."
        )
    return None
