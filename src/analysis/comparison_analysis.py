"""Compare la sélection filtrée au reste du dataset, statistique par
statistique — répond à « en quoi ces joueurs sortent-ils du lot ? ».
"""

import pandas as pd

from src.config import STATS_CLES


def compare_selection_vs_rest(df_all: pd.DataFrame, sel: pd.DataFrame) -> pd.DataFrame:
    if sel.empty:
        return pd.DataFrame(columns=["Statistique", "Sélection", "Reste du dataset", "Écart"])

    rest = df_all.drop(sel.index)
    rows = []
    for stat in STATS_CLES:
        sel_mean = round(sel[stat].mean(), 1)
        rest_mean = round(rest[stat].mean(), 1)
        rows.append({
            "Statistique": stat,
            "Sélection": sel_mean,
            "Reste du dataset": rest_mean,
            "Écart": round(sel_mean - rest_mean, 1),
        })
    return pd.DataFrame(rows)
