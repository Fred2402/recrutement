"""Recherche de joueurs PlayerElo par nom — filtre "par nom" demandé.

Résout un nom de joueur vers un player_id PlayerElo, réutilisable ensuite
pour interroger la valeur marchande, l'historique, etc.
"""

from src.api.playerelo_client import get
from src.api.playerelo_config import SEARCH_PARAM_NAME


def search_players_by_name(nom: str, limit: int = 10) -> list[dict]:
    """Retourne les joueurs PlayerElo dont le nom correspond à `nom`."""
    resultat = get("/v1/players", params={SEARCH_PARAM_NAME: nom, "limit": limit})
    return resultat if isinstance(resultat, list) else resultat.get("data", [])
