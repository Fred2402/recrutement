"""Graphique 3 — Relation : existe-t-il un profil rapide ET bon dribbleur ?

Chaque championnat de la palette fixe (src/config.py::build_league_palette)
garde toujours la même couleur ; tous les autres sont regroupés sous
"Autres" en gris — sinon la légende explose au-delà de 10 catégories
(piège n°4 du cours). Les meilleurs profils (`top_names`) sont cerclés et
étiquetés pour ne pas se noyer dans le nuage.
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.config import COLOR_ACCENT, COLOR_BACKGROUND


def build_pac_dri_scatter_chart(sel: pd.DataFrame, league_palette: dict, top_names: list[str] = None) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(4, 2.9), dpi=120)
    if not sel.empty:
        sel = sel.copy()
        sel["Championnat"] = sel["League"].where(sel["League"].isin(league_palette), "Autres")

        ordre = [lg for lg in league_palette if lg in sel["Championnat"].unique()]
        sns.scatterplot(data=sel, x="PAC", y="DRI", hue="Championnat", hue_order=ordre,
                        palette=league_palette, s=60, alpha=0.85, ax=ax)

        if top_names:
            top = sel[sel["Name"].isin(top_names)]
            ax.scatter(top["PAC"], top["DRI"], s=160, facecolors="none",
                       edgecolors=COLOR_ACCENT, linewidths=2, zorder=5)
            for _, row in top.iterrows():
                ax.annotate(row["Name"], (row["PAC"], row["DRI"]), xytext=(6, 6),
                           textcoords="offset points", fontsize=8, fontweight="bold", color=COLOR_ACCENT)

        ax.legend(fontsize=7, bbox_to_anchor=(1.02, 1), loc="upper left")
    ax.set_title("Vitesse (PAC) vs Dribble (DRI)")
    fig.tight_layout()
    return fig
