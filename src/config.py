"""Configuration centrale du projet.

Une seule source de vérité pour les chemins, les valeurs par défaut du
formulaire, et la palette : chaque championnat garde la même couleur sur
TOUS les graphiques de l'application (cf. cours, piège n°5 — « des couleurs
différentes d'un graphique à l'autre »).
"""

from pathlib import Path

import pandas as pd

# --- Chemins ---
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "all_players_clean.csv"
GRAPHIQUE_DIR = BASE_DIR / "graphique"

# --- Rôles de couleur fixes (jamais liés à un rang/classement) ---
COLOR_SELECTION = "#2a78d6"    # la sélection courante, partout
COLOR_BACKGROUND = "#c9c9c9"   # le reste du dataset, toujours gris
COLOR_ACCENT = "#e63946"       # mise en avant ponctuelle / alerte

# --- Métier ---
GRANDS_CHAMPIONNATS = [
    "Premier League",
    "LALIGA EA SPORTS",
    "Bundesliga",
    "Serie A Enilive",
    "Ligue 1 McDonald's",
]

# --- Valeurs par défaut du formulaire (question du directeur sportif) ---
DEFAULT_OVR_MIN = 75
DEFAULT_PAC_MIN = 80
DEFAULT_DRI_MIN = 75
DEFAULT_POSITIONS = ["LW", "RW"]

# --- Colonnes affichées dans les tableaux ---
COLONNES_TABLE = ["Name", "Team", "League", "Position", "Age", "OVR", "PAC", "DRI", "SHO", "PAS"]

# --- Statistiques clés utilisées pour les comparaisons / la similarité ---
STATS_CLES = ["OVR", "PAC", "SHO", "PAS", "DRI", "DEF", "PHY"]
STATS_SIMILARITE = ["PAC", "SHO", "PAS", "DRI", "DEF", "PHY"]

# Palette qualitative de secours pour les championnats (10 teintes distinctes)
_PALETTE_QUALITATIVE = [
    "#2a78d6", "#e63946", "#40916c", "#e0a458", "#6a4c93",
    "#457b9d", "#bc6c25", "#588157", "#9e2a2b", "#3a5a40",
]


def build_league_palette(df: pd.DataFrame, top_n: int = 10) -> dict:
    """Construit UNE correspondance ligue -> couleur, fixe pour toute la session.

    Les `top_n` championnats les plus fréquents du dataset complet reçoivent
    une couleur distincte ; tous les autres partagent le gris "Autres".
    Cette correspondance est calculée une seule fois (sur le dataset complet,
    pas sur la sélection filtrée) pour ne jamais changer en cours de session.
    """
    top_leagues = df["League"].value_counts().head(top_n).index.tolist()
    palette = {lg: _PALETTE_QUALITATIVE[i % len(_PALETTE_QUALITATIVE)] for i, lg in enumerate(top_leagues)}
    palette["Autres"] = COLOR_BACKGROUND
    return palette
