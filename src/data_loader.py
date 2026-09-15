"""Chargement du dataset joueurs — une seule fonctionnalité, un seul fichier."""

import pandas as pd

from src.config import DATA_PATH


def load_players(path=DATA_PATH) -> pd.DataFrame:
    """Charge le CSV des joueurs (déjà nettoyé en amont)."""
    return pd.read_csv(path)
