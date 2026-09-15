"""Recherche de joueurs au profil statistique proche d'un joueur de
référence — aide à trouver des alternatives moins chères ou moins connues
au profil recherché (distance euclidienne sur les stats clés).
"""

import numpy as np
import pandas as pd

from src.config import STATS_SIMILARITE


def find_similar_players(df: pd.DataFrame, reference_name: str, top_n: int = 5) -> pd.DataFrame:
    """Retourne les `top_n` joueurs les plus proches du joueur `reference_name`
    sur les statistiques clés (vitesse, tir, passe, dribble, défense, physique).

    Un gardien n'est comparé qu'à d'autres gardiens, et un joueur de champ
    qu'à d'autres joueurs de champ : leurs statistiques de champ ne sont pas
    sur la même échelle (un gardien n'est jamais vraiment évalué sur son
    tir ou son dribble), les mélanger produisait des rapprochements absurdes.
    """
    if reference_name not in df["Name"].values:
        return pd.DataFrame()

    ligne_reference = df.loc[df["Name"] == reference_name].iloc[0]
    # .iloc[0] sur une ligne qui mélange texte et nombres force les valeurs
    # numériques en dtype "object" : sans ce cast explicite en float, le
    # calcul de distance plante plus loin (np.sqrt refuse un Series object).
    reference = ligne_reference[STATS_SIMILARITE].astype(float)

    est_gardien = ligne_reference.get("Position") == "GK"
    bassin = df[df["Position"] == "GK"] if est_gardien else df[df["Position"] != "GK"]

    distances = np.sqrt(((bassin[STATS_SIMILARITE].astype(float) - reference) ** 2).sum(axis=1))

    resultat = bassin.copy()
    resultat["Distance"] = distances.round(2)
    resultat = resultat[resultat["Name"] != reference_name]

    return resultat.sort_values("Distance").head(top_n)
