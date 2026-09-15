"""Filtre sur le genre (colonne `gender` : "M" ou "F")."""

import pandas as pd


def filter_by_gender(df: pd.DataFrame, genres: list[str]) -> pd.DataFrame:
    """Filtre par genre(s). Aucune sélection = les deux."""
    if not genres:
        return df
    return df[df["gender"].isin(genres)]
