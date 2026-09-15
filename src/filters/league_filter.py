"""Filtre sur le championnat (League)."""

import pandas as pd

from src.config import GRANDS_CHAMPIONNATS


def filter_by_league(df: pd.DataFrame, ligues: list[str], exclure_grands: bool) -> pd.DataFrame:
    """Filtre par ligues explicites, ou exclut les 5 grands championnats.

    Priorité : une sélection explicite de ligues prime toujours sur l'option
    "exclure les 5 grands" (voir get_active_exclusions ci-dessous pour
    afficher cette priorité à l'utilisateur plutôt que de la laisser
    silencieuse).
    """
    if ligues:
        return df[df["League"].isin(ligues)]
    if exclure_grands:
        return df[~df["League"].isin(GRANDS_CHAMPIONNATS)]
    return df


def get_active_exclusions(ligues: list[str], exclure_grands: bool) -> list[str]:
    """Retourne la liste des championnats réellement exclus de la sélection.

    Renvoie une liste vide si une sélection explicite de ligues est en cours
    (elle prime et neutralise la case "exclure les 5 grands") ou si la case
    n'est pas cochée — pour que l'interface puisse le dire clairement au
    lieu de laisser deviner.
    """
    if ligues:
        return []
    if exclure_grands:
        return list(GRANDS_CHAMPIONNATS)
    return []

