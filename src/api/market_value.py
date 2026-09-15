"""Valeur marchande calculée par PlayerElo pour un joueur donné
(GET /v1/players/{id}/value)."""

from src.api.playerelo_client import get

# Noms de champ possibles pour la valeur, la documentation publique ne
# donnant pas d'exemple de payload exact pour cet endpoint.
_CLES_VALEUR_POSSIBLES = ("market_value", "value", "value_eur", "estimated_value")


def get_market_value(player_id: str) -> dict:
    """Retourne la réponse brute PlayerElo pour la valeur marchande."""
    return get(f"/v1/players/{player_id}/value")


def extract_value_eur(reponse: dict):
    """Isole le montant en euros quel que soit le nom de champ utilisé par
    l'API, pour ne pas casser le reste du code si le nom exact diffère.
    """
    for cle in _CLES_VALEUR_POSSIBLES:
        if cle in reponse:
            return reponse[cle]
    return None
