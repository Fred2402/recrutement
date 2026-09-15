"""Suivi du quota PlayerElo (GET /v1/usage) — pour voir venir la limite du
plan gratuit (500 requêtes/mois) avant de la dépasser. Cet appel ne compte
pas lui-même dans le quota, d'après la documentation PlayerElo.
"""

from src.api.playerelo_client import get


def get_usage() -> dict:
    return get("/v1/usage")
