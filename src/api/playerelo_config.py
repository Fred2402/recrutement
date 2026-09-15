"""Configuration d'accès à l'API PlayerElo.

La clé n'est JAMAIS codée en dur dans le projet : elle est lue depuis la
variable d'environnement PLAYERELO_API_KEY, elle-même chargée depuis un
fichier .env local (non versionné — voir .env.example à la racine).

Récupérer une clé gratuite (500 requêtes/mois, 10/min) :
https://playerelo.football/api-access
"""

import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass  # python-dotenv est optionnel : la clé peut aussi être exportée directement dans l'environnement


def _lire_cle_api() -> str:
    valeur = os.environ.get("PLAYERELO_API_KEY", "")
    if valeur:
        return valeur

    # En local, la clé vient du .env. Une fois déployé sur Streamlit
    # Community Cloud, elle est définie dans les "Secrets" de l'app plutôt
    # que dans un fichier — on va la chercher là si elle est absente de
    # l'environnement, sans planter si aucun secret n'est configuré.
    try:
        import streamlit as st

        return st.secrets.get("PLAYERELO_API_KEY", "")
    except Exception:
        return ""


BASE_URL = "https://data-api.playerelo.football"
API_KEY = _lire_cle_api()
TIMEOUT_SECONDS = 8

# Nom du paramètre de recherche par nom sur GET /v1/players. Confirmé
# empiriquement (non documenté officiellement) : "search" fonctionne,
# "q" et "name" sont ignorés silencieusement par l'API (elle renvoie alors
# la liste par défaut au lieu d'une erreur, d'où l'importance de vérifier
# la pertinence du résultat, pas seulement sa présence).
SEARCH_PARAM_NAME = "search"
