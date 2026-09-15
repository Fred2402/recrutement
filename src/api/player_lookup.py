"""Recherche d'un joueur PlayerElo par identifiant — filtre "par id" demandé."""

from src.api.playerelo_client import get


def get_player_by_id(player_id: str) -> dict:
    """Fiche complète PlayerElo (Elo, EAR, rang) pour un identifiant donné."""
    return get(f"/v1/players/{player_id}")
