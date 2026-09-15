"""Tableau des meilleurs profils, trié, avec dégradé de couleur sur OVR et
mise en avant des meilleurs profils identifiés (`top_names`). La colonne
valeur marchande n'apparaît que si elle a été attachée en amont
(src.analysis.market_value_analysis.attach_market_value).

Le texte est toujours forcé en noir sur les cellules colorées (dégradé et
surlignage) : sans ça, un thème Streamlit sombre affiche du texte blanc sur
fond clair, illisible.
"""

import pandas as pd

from src.config import COLONNES_TABLE


def build_ranking_table(sel: pd.DataFrame, top_names: list[str] = None):
    """Retourne un pandas Styler prêt pour st.dataframe / st.write."""
    if sel.empty:
        return sel

    colonnes = list(COLONNES_TABLE)
    if "Valeur marchande (€)" in sel.columns:
        colonnes = colonnes + ["Valeur marchande (€)"]
    colonnes = [c for c in colonnes if c in sel.columns]

    tableau = sel.sort_values("OVR", ascending=False)[colonnes].reset_index(drop=True)
    style = tableau.style.background_gradient(subset=["OVR"], cmap="Blues")
    style = style.set_properties(subset=["OVR"], **{"color": "black"})

    if top_names:
        def surligner(ligne):
            if ligne["Name"] in top_names:
                return ["background-color: #fff3cd; font-weight: 600; color: black;"] * len(ligne)
            return [""] * len(ligne)

        style = style.apply(surligner, axis=1)

    return style