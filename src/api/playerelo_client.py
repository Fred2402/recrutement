"""Client HTTP bas niveau pour l'API PlayerElo.

Un seul point d'entrée pour tous les appels authentifiés : gère l'en-tête
Authorization, le timeout, quelques tentatives en cas de blip réseau/DNS,
et transforme les erreurs en messages lisibles plutôt que de laisser
remonter une exception `requests` brute jusqu'à l'interface Streamlit.
"""

import time

import requests

from src.api.playerelo_config import API_KEY, BASE_URL, TIMEOUT_SECONDS


class PlayerEloError(Exception):
    """Erreur renvoyée par l'API PlayerElo (clé manquante, quota, réseau...)."""


def get(path: str, params: dict = None, tentatives: int = 3) -> dict:
    if not API_KEY:
        raise PlayerEloError(
            "Aucune clé API PlayerElo configurée. Définissez la variable "
            "d'environnement PLAYERELO_API_KEY (clé gratuite sur "
            "https://playerelo.football/api-access)."
        )

    derniere_erreur = None
    reponse = None
    for tentative in range(1, tentatives + 1):
        try:
            reponse = requests.get(
                f"{BASE_URL}{path}",
                headers={"Authorization": f"Bearer {API_KEY}"},
                params=params or {},
                timeout=TIMEOUT_SECONDS,
            )
            break
        except requests.RequestException as erreur:
            derniere_erreur = erreur
            if tentative < tentatives:
                time.sleep(2 * tentative)  # 2s, puis 4s : laisse passer un blip DNS/réseau
            continue
    else:
        raise PlayerEloError(
            f"Erreur réseau vers PlayerElo après {tentatives} tentatives : {derniere_erreur}"
        ) from derniere_erreur

    if reponse.status_code == 401:
        raise PlayerEloError("Clé API PlayerElo invalide ou expirée.")
    if reponse.status_code == 429:
        # 429 couvre deux limites différentes chez PlayerElo (quota mensuel
        # ET limite par minute) : on remonte le corps de la réponse plutôt
        # que de deviner laquelle, pour ne pas afficher un message trompeur.
        raise PlayerEloError(
            f"Limite de requêtes PlayerElo atteinte (429) — quota mensuel ou "
            f"limite par minute (10/min en gratuit) : {reponse.text[:200]}"
        )
    if not reponse.ok:
        raise PlayerEloError(f"PlayerElo a répondu {reponse.status_code} : {reponse.text[:200]}")

    return reponse.json()
