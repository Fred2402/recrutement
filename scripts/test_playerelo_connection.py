"""Vérifie la connexion à l'API PlayerElo : quota, puis nom du paramètre
de recherche par nom (en vérifiant la pertinence du résultat, pas juste
sa présence), puis champ de valeur marchande.

Espace les appels de 7s pour rester sous la limite de 10 req/min du plan
gratuit. Le script prend donc un peu plus d'une minute à tourner.

Usage : python scripts/test_playerelo_connection.py
"""

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.api.playerelo_client import PlayerEloError, get
from src.api.playerelo_config import API_KEY

DELAI_SECONDES = 7  # marge sous la limite de 10 req/min


def appel_espace(path, params=None):
    time.sleep(DELAI_SECONDES)
    return get(path, params=params)


print("Clé détectée :", "oui" if API_KEY else "NON — vérifier le fichier .env")
print()

print("--- GET /v1/usage ---")
try:
    print(json.dumps(get("/v1/usage"), indent=2, ensure_ascii=False))
except PlayerEloError as erreur:
    print("ERREUR :", erreur)
print()

print("--- GET /v1/players?limit=3 ---")
try:
    reponse = appel_espace("/v1/players", {"limit": 3})
    print(json.dumps(reponse, indent=2, ensure_ascii=False)[:1000])
except PlayerEloError as erreur:
    print("ERREUR :", erreur)
print()

NOMS_TEST = ["Haaland", "Mbappe", "Mbappé"]
CANDIDATS_PARAM = ["search", "q", "name"]

bon_parametre = None
premier_resultat_pertinent = None

for parametre in CANDIDATS_PARAM:
    for nom_test in NOMS_TEST:
        try:
            reponse = appel_espace("/v1/players", {parametre: nom_test, "limit": 5})
            liste = reponse if isinstance(reponse, list) else reponse.get("data", [])
            pertinent = [j for j in liste if nom_test.lower().replace("é", "e")
                        in j.get("player_name", "").lower().replace("é", "e")]
            print(f"  {parametre!r:10} + {nom_test!r:10} -> {len(liste)} résultat(s), "
                  f"{len(pertinent)} pertinent(s)"
                  + (f" : {pertinent[0]['player_name']}" if pertinent else ""))
            if pertinent and bon_parametre is None:
                bon_parametre = parametre
                premier_resultat_pertinent = pertinent[0]
        except PlayerEloError as erreur:
            print(f"  {parametre!r:10} + {nom_test!r:10} -> ERREUR : {erreur}")

print()
if bon_parametre:
    print(f"=> Paramètre qui fonctionne vraiment : '{bon_parametre}'")
    print(f"   Mettre SEARCH_PARAM_NAME = \"{bon_parametre}\" dans src/api/playerelo_config.py")
else:
    print("=> Aucun des noms testés n'a renvoyé de résultat pertinent.")

print()

print("--- GET /v1/players/{id}/value ---")
if premier_resultat_pertinent:
    try:
        player_id = premier_resultat_pertinent.get("player_id")
        reponse = appel_espace(f"/v1/players/{player_id}/value")
        print(json.dumps(reponse, indent=2, ensure_ascii=False))
    except PlayerEloError as erreur:
        print("ERREUR :", erreur)
else:
    print("Pas de joueur pertinent trouvé à l'étape 2 — rien à tester ici pour l'instant.")
