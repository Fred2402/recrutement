"""Applique les filtres dans l'ordre : seuils, championnat, poste, genre.

Un seul point d'entrée pour main.py, chaque filtre restant testable et
remplaçable indépendamment dans son propre fichier.
"""

import pandas as pd

from src.filters.gender_filter import filter_by_gender
from src.filters.league_filter import filter_by_league
from src.filters.position_filter import filter_by_position
from src.filters.threshold_filter import filter_by_thresholds


def apply_all_filters(
    df: pd.DataFrame,
    ligues: list[str],
    postes: list[str],
    ovr_min: int,
    pac_min: int,
    dri_min: int,
    exclure_grands: bool,
    genres: list[str] = None,
) -> pd.DataFrame:
    sel = filter_by_thresholds(df, ovr_min, pac_min, dri_min)
    sel = filter_by_league(sel, ligues, exclure_grands)
    sel = filter_by_position(sel, postes)
    sel = filter_by_gender(sel, genres or [])
    return sel
