"""Résout un nom saisi librement vers l'orthographe exacte du dataset local
(avec les bons accents), avant d'interroger PlayerElo — dont la recherche
s'est révélée sensible aux accents lors des tests ("Mbappe" : 0 résultat,
"Mbappé" : 2 résultats).
"""

import unicodedata
from difflib import get_close_matches

import pandas as pd


def _sans_accents(texte: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFKD", texte) if not unicodedata.combining(c)
    ).lower()


def resolve_canonical_name(nom_saisi: str, df: pd.DataFrame) -> str:
    """Retourne l'orthographe exacte présente dans `df["Name"]` pour un nom
    saisi sans accent, partiel (nom de famille seul) ou approximatif ;
    renvoie `nom_saisi` tel quel si rien d'assez proche n'est trouvé
    (l'appel à l'API se fera alors tel quel).
    """
    noms = df["Name"].dropna().unique().tolist()
    cible = _sans_accents(nom_saisi)
    noms_normalises = {n: _sans_accents(n) for n in noms}

    # 1. Nom complet identique (aux accents/casse près)
    for nom, normalise in noms_normalises.items():
        if normalise == cible:
            return nom

    # 2. Nom saisi retrouvé comme sous-chaîne (ex. "Mbappe" dans "Kylian Mbappé")
    correspondances_partielles = [
        nom for nom, normalise in noms_normalises.items() if cible in normalise
    ]
    if len(correspondances_partielles) == 1:
        return correspondances_partielles[0]
    if len(correspondances_partielles) > 1:
        # Plusieurs homonymes possibles : on garde le nom saisi tel quel
        # plutôt que de deviner lequel — l'API tranchera ou renverra une liste.
        return nom_saisi

    # 3. Sinon, le nom le plus proche au sens de la distance d'édition
    proches = get_close_matches(cible, noms_normalises.values(), n=1, cutoff=0.8)
    if proches:
        for nom, normalise in noms_normalises.items():
            if normalise == proches[0]:
                return nom

    return nom_saisi
