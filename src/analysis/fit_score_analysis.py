"""Score composite de correspondance au profil recherché.

Transforme un tableau de chiffres en un classement actionnable : au lieu de
lire six colonnes, le recruteur voit un score unique sur 100. La
pondération s'adapte au(x) poste(s) filtré(s) — un score qui valorise la
vitesse et le dribble n'a aucun sens pour évaluer un défenseur central.
"""

import pandas as pd

# --- Profils de pondération par famille de poste ---
POSITION_WEIGHT_PROFILES = {
    "ATTAQUANT": {"PAC": 0.30, "SHO": 0.30, "DRI": 0.25, "PAS": 0.15},
    "MILIEU": {"PAS": 0.30, "DRI": 0.30, "SHO": 0.20, "DEF": 0.20},
    "DEFENSEUR": {"DEF": 0.40, "PHY": 0.30, "PAC": 0.20, "PAS": 0.10},
}

# Un gardien ne peut pas être évalué avec des poids pensés pour un joueur de
# champ (voir aussi similarity_analysis, qui les isole pour la même raison).
POSITION_TO_GROUP = {
    "ST": "ATTAQUANT", "LW": "ATTAQUANT", "RW": "ATTAQUANT",
    "CAM": "MILIEU", "CM": "MILIEU", "CDM": "MILIEU", "LM": "MILIEU", "RM": "MILIEU",
    "CB": "DEFENSEUR", "LB": "DEFENSEUR", "RB": "DEFENSEUR",
    "GK": "GARDIEN",
}

# Pondération par défaut : le profil "ailier" de la question métier d'origine,
# utilisé quand aucun poste n'est filtré ou que plusieurs familles sont mélangées.
DEFAULT_WEIGHTS = POSITION_WEIGHT_PROFILES["ATTAQUANT"]


def get_weights_for_positions(postes: list[str]) -> dict:
    """Choisit la pondération du score selon les postes actuellement filtrés.

    Si les postes filtrés couvrent plusieurs familles à la fois (ex. ailiers
    ET défenseurs), retombe sur le profil par défaut plutôt que de mélanger
    des pondérations qui n'auraient pas de sens ensemble.
    """
    groupes = {POSITION_TO_GROUP.get(p) for p in postes}
    groupes.discard(None)
    groupes.discard("GARDIEN")  # les gardiens ont leur propre traitement, jamais ce score

    if len(groupes) == 1:
        return POSITION_WEIGHT_PROFILES[groupes.pop()]
    return DEFAULT_WEIGHTS


def compute_fit_score(sel: pd.DataFrame, weights: dict = None) -> pd.DataFrame:
    """Ajoute une colonne 'Score' (0-100) pondérant les statistiques fournies.

    Les gardiens sont exclus du calcul : leurs statistiques de champ ne sont
    pas comparables à celles d'un joueur de champ (voir README, limite connue).
    """
    sel = sel[sel.get("Position") != "GK"] if "Position" in sel.columns else sel

    if sel.empty:
        resultat = sel.copy()
        resultat["Score"] = pd.Series(dtype=float)
        return resultat

    weights = weights or DEFAULT_WEIGHTS
    total_poids = sum(weights.values())
    score = sum(sel[stat] * poids for stat, poids in weights.items()) / total_poids

    resultat = sel.copy()
    resultat["Score"] = score.round(1)
    return resultat.sort_values("Score", ascending=False)


def get_top_recommendation(sel: pd.DataFrame, weights: dict = None, top_n: int = 3) -> pd.DataFrame:
    """Retourne les `top_n` meilleurs profils selon le score composite."""
    return compute_fit_score(sel, weights).head(top_n)
