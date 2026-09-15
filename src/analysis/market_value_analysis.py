"""Relie un joueur du dataset (nom ou identifiant PlayerElo) à sa valeur
marchande complète (nom, club, ligue, poste, Elo), en passant par le cache
disque avant tout appel réseau.
"""

import pandas as pd

from src.analysis.name_resolver import _sans_accents
from src.api.market_value import extract_value_eur, get_market_value
from src.api.player_lookup import get_player_by_id
from src.api.playerelo_client import PlayerEloError
from src.api.value_cache import load_cache, save_to_cache


def fetch_value_by_id(player_id: str) -> dict:
    """Valeur marchande + fiche complète pour un identifiant PlayerElo.

    Combine deux endpoints : /value (montant, mais sans club/ligue) et la
    fiche joueur (club/ligue, mais sans montant) — ni l'un ni l'autre seul
    ne suffit.
    """
    cle_cache = f"id:{player_id}"
    cache = load_cache()
    if cle_cache in cache:
        return cache[cle_cache]

    try:
        reponse_valeur = get_market_value(player_id)
    except PlayerEloError as erreur:
        return {"erreur": str(erreur)}

    try:
        fiche = get_player_by_id(player_id)
    except PlayerEloError:
        fiche = {}  # la fiche est un bonus : sans elle, on garde au moins la valeur

    resultat = {
        "valeur_eur": extract_value_eur(reponse_valeur),
        "player_id": player_id,
        "nom_playerelo": fiche.get("player_name") or fiche.get("name") or reponse_valeur.get("name"),
        "elo": fiche.get("elo", reponse_valeur.get("elo")),
        "poste": fiche.get("position", reponse_valeur.get("position")),
        "age": fiche.get("age", reponse_valeur.get("age")),
        "club": fiche.get("current_team"),
        "ligue": fiche.get("current_league"),
    }
    save_to_cache(cle_cache, resultat)
    return resultat


def get_cached_values_table() -> pd.DataFrame:
    """Tableau des valeurs marchandes déjà consultées, avec le contexte
    PlayerElo (nom exact, Elo, poste, club, ligue)."""
    cache = load_cache()
    lignes = []
    for cle, valeur in cache.items():
        if "erreur" in valeur:
            continue
        lignes.append({
            "Recherche": cle,
            "Nom (PlayerElo)": valeur.get("nom_playerelo"),
            "player_id": valeur.get("player_id"),
            "Elo": valeur.get("elo"),
            "Poste": valeur.get("poste"),
            "Club": valeur.get("club"),
            "Ligue": valeur.get("ligue"),
            "Valeur marchande (€)": valeur.get("valeur_eur"),
        })
    return pd.DataFrame(lignes)


def build_market_value_lookup() -> dict:
    """Retourne {nom_normalisé: valeur_eur} à partir du cache disque, pour
    croiser les valeurs déjà consultées avec n'importe quel dataset local.
    """
    cache = load_cache()
    lookup = {}
    for valeur in cache.values():
        if "erreur" in valeur or not valeur.get("nom_playerelo") or valeur.get("valeur_eur") is None:
            continue
        lookup[_sans_accents(valeur["nom_playerelo"])] = valeur["valeur_eur"]
    return lookup


def attach_market_value(df: pd.DataFrame) -> pd.DataFrame:
    """Ajoute la colonne 'Valeur marchande (€)' à partir du cache PlayerElo ;
    NaN pour un joueur jamais recherché dans l'onglet Valeur marchande.
    """
    lookup = build_market_value_lookup()
    resultat = df.copy()
    resultat["Valeur marchande (€)"] = resultat["Name"].apply(lambda n: lookup.get(_sans_accents(n)))
    return resultat
