"""Construit la phrase d'interprétation qui se réécrit avec les filtres.

Canal "être expliqué" du cours : un chiffre seul ne dit rien, une phrase
qui réagit aux filtres et donne une référence, si.
"""

import pandas as pd


def build_narrative(df_all: pd.DataFrame, sel: pd.DataFrame) -> str:
    if sel.empty:
        return "Aucun joueur ne correspond aux critères actuels."

    n = len(sel)
    pct = round(100 * n / len(df_all), 1)
    pac_delta = round(sel["PAC"].mean() - df_all["PAC"].mean(), 1)
    dri_delta = round(sel["DRI"].mean() - df_all["DRI"].mean(), 1)

    sens_pac = "plus" if pac_delta >= 0 else "moins"
    sens_dri = "meilleurs" if dri_delta >= 0 else "moins bons"

    return (
        f"{n} joueur{'s' if n > 1 else ''} correspond{'ent' if n > 1 else ''} aux critères "
        f"({pct} % du dataset). En moyenne, ils sont {abs(pac_delta):.1f} points {sens_pac} rapides "
        f"et {abs(dri_delta):.1f} points {sens_dri} dribbleurs que l'ensemble du dataset."
    )
