"""Filtre sur le poste (Position)."""

import pandas as pd


def filter_by_position(df: pd.DataFrame, postes: list[str]) -> pd.DataFrame:
    """Filtre par poste(s). Aucune sélection = tous les postes."""
    if not postes:
        return df
    return df[df["Position"].isin(postes)]
