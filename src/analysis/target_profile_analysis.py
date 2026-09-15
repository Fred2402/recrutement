"""Recherche inversée : à partir d'un profil-cible défini par curseurs
(sans partir d'un joueur existant), trouve qui s'en rapproche le plus dans
tout le dataset.
"""

import numpy as np
import pandas as pd

from src.config import STATS_SIMILARITE


def find_players_matching_target(df: pd.DataFrame, target: dict, top_n: int = 10) -> pd.DataFrame:
    """`target` : dict {statistique: valeur souhaitée} sur STATS_SIMILARITE."""
    stats_utilisees = [s for s in STATS_SIMILARITE if s in target]
    if not stats_utilisees:
        return pd.DataFrame()

    cible = pd.Series({s: target[s] for s in stats_utilisees}, dtype=float)
    distances = np.sqrt(((df[stats_utilisees].astype(float) - cible) ** 2).sum(axis=1))

    resultat = df.copy()
    resultat["Distance au profil"] = distances.round(2)
    return resultat.sort_values("Distance au profil").head(top_n)
