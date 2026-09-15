"""Cache disque des valeurs marchandes déjà récupérées.

Le plan gratuit PlayerElo est limité à 500 requêtes/mois : ce cache évite
de reconsommer du quota pour un joueur déjà consulté lors d'une session
précédente. Fichier JSON simple, adapté au volume d'un projet étudiant.
"""

import json
from pathlib import Path

CACHE_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "market_value_cache.json"


def load_cache() -> dict:
    if CACHE_PATH.exists():
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_to_cache(cle: str, valeur: dict) -> None:
    cache = load_cache()
    cache[cle] = valeur
    CACHE_PATH.parent.mkdir(exist_ok=True)
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)
