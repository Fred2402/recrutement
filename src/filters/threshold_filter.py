"""Filtres sur les seuils numériques (OVR, PAC, DRI minimums)."""

import pandas as pd


def filter_by_thresholds(df: pd.DataFrame, ovr_min: int, pac_min: int, dri_min: int) -> pd.DataFrame:
    """Ne garde que les joueurs au-dessus des trois seuils fournis."""
    return df.query("OVR >= @ovr_min and PAC >= @pac_min and DRI >= @dri_min")
