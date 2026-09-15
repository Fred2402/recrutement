"""Calcul des chiffres clés (KPI) de la sélection, avec écart vs l'ensemble
du dataset — la référence est ce qui donne du sens à un chiffre isolé
(cf. cours, chapitre "Cohérence et message" : un chiffre clé a toujours
besoin d'une référence).
"""

import pandas as pd

from src.config import STATS_CLES


def compute_kpis(df_all: pd.DataFrame, sel: pd.DataFrame) -> dict:
    if sel.empty:
        return {"count": 0, "pct_dataset": 0.0, "moyennes": {}, "deltas": {}}

    moyennes = {stat: round(sel[stat].mean(), 1) for stat in STATS_CLES}
    deltas = {stat: round(sel[stat].mean() - df_all[stat].mean(), 1) for stat in STATS_CLES}

    return {
        "count": len(sel),
        "pct_dataset": round(100 * len(sel) / len(df_all), 1),
        "moyennes": moyennes,
        "deltas": deltas,
    }
