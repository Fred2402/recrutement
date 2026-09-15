"""Filtre optionnel sur la valeur marchande déjà consultée (PlayerElo).

Un joueur jamais recherché dans l'onglet Valeur marchande n'a pas de valeur
connue : il n'est jamais exclu par ce filtre par défaut (on ne peut pas dire
qu'il dépasse un budget qu'on ne connaît pas), sauf si l'option "uniquement
les valeurs connues" est activée.
"""

import pandas as pd


def filter_by_budget(df: pd.DataFrame, budget_max, uniquement_connues: bool) -> pd.DataFrame:
    if "Valeur marchande (€)" not in df.columns or budget_max is None:
        return df

    connue = df["Valeur marchande (€)"].notna()
    sous_budget = df["Valeur marchande (€)"] <= budget_max

    if uniquement_connues:
        return df[connue & sous_budget]
    return df[~connue | sous_budget]
