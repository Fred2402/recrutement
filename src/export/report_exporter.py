"""Génère un rapport PDF : verdict d'ensemble, puis ventilation Hommes /
Femmes, avec la valeur marchande PlayerElo pour les profils déjà consultés.
Autonome (matplotlib uniquement), pensé pour être transmis au directeur
sportif sans qu'il ait à relancer l'application.
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages

from src.analysis.fit_score_analysis import get_top_recommendation
from src.analysis.market_value_analysis import attach_market_value
from src.analysis.narrative_analysis import build_narrative
from src.config import COLOR_BACKGROUND, COLOR_SELECTION, GRAPHIQUE_DIR


def _ligne_top(ax, ligne, rang, y):
    valeur = ligne.get("Valeur marchande (€)")
    valeur_txt = f" · valeur marchande {valeur:,.0f} €" if pd.notna(valeur) else ""
    ax.text(0, y, f"{rang}. {ligne['Name']} — {ligne['Team']} ({ligne['League']})",
            fontsize=10, fontweight="bold")
    ax.text(0.02, y - 0.09, f"Score {ligne['Score']}/100 · OVR {ligne['OVR']} · "
                            f"PAC {ligne['PAC']} · DRI {ligne['DRI']}{valeur_txt}",
            fontsize=8.5, color="#555555")


def _page_ensemble(pdf, df_all: pd.DataFrame, sel: pd.DataFrame, league_palette: dict, weights: dict):
    narrative = build_narrative(df_all, sel)
    top3 = get_top_recommendation(sel, weights, top_n=3)

    fig = plt.figure(figsize=(8.27, 11.69))
    grille = fig.add_gridspec(4, 1, height_ratios=[0.5, 0.9, 1.3, 1.3], hspace=0.55)

    ax_titre = fig.add_subplot(grille[0])
    ax_titre.axis("off")
    ax_titre.text(0, 0.85, "Rapport de recrutement — vue d'ensemble", fontsize=17, fontweight="bold")
    ax_titre.text(0, 0.35, narrative, fontsize=10, wrap=True)

    ax_top3 = fig.add_subplot(grille[1])
    ax_top3.axis("off")
    ax_top3.text(0, 0.95, "Top 3 recommandé (tous genres confondus)", fontsize=12, fontweight="bold")
    if top3.empty:
        ax_top3.text(0, 0.55, "Aucun profil ne correspond aux critères actuels.", fontsize=10)
    else:
        for i, ligne in enumerate(top3.to_dict("records")):
            _ligne_top(ax_top3, ligne, i + 1, 0.7 - i * 0.28)

    ax_dist = fig.add_subplot(grille[2])
    sns.kdeplot(df_all["OVR"], color=COLOR_BACKGROUND, fill=True, label="Ensemble du dataset", ax=ax_dist)
    if not sel.empty:
        sns.kdeplot(sel["OVR"], color=COLOR_SELECTION, fill=True, label="Sélection", ax=ax_dist)
    ax_dist.set_title("Distribution de OVR — sélection vs ensemble", fontsize=11)
    ax_dist.legend(fontsize=8)

    ax_scatter = fig.add_subplot(grille[3])
    if not sel.empty:
        sel_scatter = sel.copy()
        sel_scatter["Championnat"] = sel_scatter["League"].where(sel_scatter["League"].isin(league_palette), "Autres")
        ordre = [lg for lg in league_palette if lg in sel_scatter["Championnat"].unique()]
        sns.scatterplot(data=sel_scatter, x="PAC", y="DRI", hue="Championnat", hue_order=ordre,
                        palette=league_palette, s=50, alpha=0.85, ax=ax_scatter)
        ax_scatter.legend(fontsize=7, bbox_to_anchor=(1.02, 1), loc="upper left")
    ax_scatter.set_title("Vitesse (PAC) vs Dribble (DRI)", fontsize=11)

    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def _page_par_genre(pdf, sel_hommes: pd.DataFrame, sel_femmes: pd.DataFrame, weights: dict):
    fig = plt.figure(figsize=(8.27, 11.69))
    grille = fig.add_gridspec(3, 1, height_ratios=[0.3, 1, 1], hspace=0.5)

    ax_titre = fig.add_subplot(grille[0])
    ax_titre.axis("off")
    ax_titre.text(0, 0.7, "Ventilation par genre", fontsize=17, fontweight="bold")
    ax_titre.text(0, 0.2, f"{len(sel_hommes)} homme(s) · {len(sel_femmes)} femme(s) dans la sélection actuelle",
                  fontsize=10, color="#555555")

    for ax_slot, sel_genre, titre in [
        (grille[1], sel_hommes, "Top 3 — Hommes"),
        (grille[2], sel_femmes, "Top 3 — Femmes"),
    ]:
        ax = fig.add_subplot(ax_slot)
        ax.axis("off")
        ax.text(0, 0.95, titre, fontsize=12, fontweight="bold")

        if sel_genre.empty:
            ax.text(0, 0.6, "Aucun joueur ne correspond aux critères actuels pour ce groupe.", fontsize=10)
            continue

        top3_genre = get_top_recommendation(sel_genre, weights, top_n=3)
        if top3_genre.empty:
            ax.text(0, 0.6, "Aucun profil évaluable (gardiens exclus du score composite).", fontsize=10)
        else:
            for i, ligne in enumerate(top3_genre.to_dict("records")):
                _ligne_top(ax, ligne, i + 1, 0.72 - i * 0.28)

    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def export_report_pdf(
    df_all: pd.DataFrame,
    sel: pd.DataFrame,
    league_palette: dict,
    weights: dict = None,
    filename: str = "rapport_recrutement.pdf",
) -> str:
    GRAPHIQUE_DIR.mkdir(exist_ok=True)
    chemin = GRAPHIQUE_DIR / filename

    sel_avec_valeur = attach_market_value(sel)
    sel_hommes = sel_avec_valeur[sel_avec_valeur.get("gender") == "M"]
    sel_femmes = sel_avec_valeur[sel_avec_valeur.get("gender") == "F"]

    with PdfPages(chemin) as pdf:
        _page_ensemble(pdf, df_all, sel_avec_valeur, league_palette, weights)
        _page_par_genre(pdf, sel_hommes, sel_femmes, weights)

    return str(chemin)
