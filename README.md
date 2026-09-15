# Cellule de recrutement — Tableau de bord

## Question métier
Trouver un ailier rapide et bon dribbleur, hors des cinq grands championnats,
avec une note générale (OVR) supérieure à 75.

## Fonctionnalités
- **Filtres** (championnat, poste, genre, seuils OVR/PAC/DRI, budget valeur marchande) agissant sur toutes les vues.
- **Chiffres clés** avec écart par rapport à l'ensemble du dataset (pas de chiffre sans référence).
- **Score composite adaptatif** : la pondération (vitesse/dribble/tir/passe/défense/physique) s'ajuste automatiquement au(x) poste(s) filtré(s) — un défenseur n'est pas noté avec les mêmes critères qu'un ailier. Les gardiens en sont exclus (stats non comparables).
- **Vue d'ensemble** : distribution OVR sélection vs ensemble, tableau comparatif sélection/reste, meilleurs profils.
- **Visualisations** : PAC par poste, vitesse vs dribble par championnat, corrélations entre statistiques.
- **Classements** : championnat le mieux placé sur la statistique de son choix.
- **Comparateur de joueurs** : radar de scouting pour 2-3 joueurs de la sélection.
- **Fiche joueur + alternatives** : profil détaillé et joueurs au profil proche (les gardiens ne sont comparés qu'entre eux).
- **Profil-cible** : recherche par curseurs, sans partir d'un joueur existant.
- **Valeur marchande (PlayerElo)** : recherche par nom (avec filtres poste/championnat/club/agent libre appliqués localement) ou par identifiant, croisée avec le budget dans la sidebar.
- **Export** : CSV de la sélection ; rapport PDF multi-pages (vue d'ensemble puis ventilation Hommes/Femmes, avec valeur marchande) ; script CLI pour les graphiques en PNG.

## Structure du projet
```
miniprojet_recrutement/
├── main.py                          # point d'entrée Streamlit (assemble tout, en onglets)
├── requirements.txt
├── requirements-dev.txt             # pytest, pour lancer les tests
├── pytest.ini
├── data/
│   └── all_players_clean.csv
├── doc/
│   └── README.md
├── graphique/                       # PNG/PDF exportés
├── scripts/
│   ├── generate_graphiques.py       # export CLI, sans lancer Streamlit
│   └── test_playerelo_connection.py # vérifie la clé API et les endpoints
├── tests/                           # 47 tests, aucun appel réseau
│   ├── conftest.py                  # dataset synthétique partagé
│   └── test_*.py                    # un fichier de test par module de src/
└── src/
    ├── config.py                    # chemins, seuils par défaut, palette fixe par championnat
    ├── data_loader.py               # chargement du CSV
    ├── filters/
    │   ├── league_filter.py         # filtre championnat (+ get_active_exclusions)
    │   ├── position_filter.py       # filtre poste
    │   ├── gender_filter.py         # filtre genre (M/F)
    │   ├── threshold_filter.py      # filtre OVR/PAC/DRI minimums
    │   ├── budget_filter.py         # filtre valeur marchande (PlayerElo)
    │   └── apply_filters.py         # orchestrateur
    ├── analysis/
    │   ├── kpi_analysis.py          # chiffres clés + écart vs dataset
    │   ├── comparison_analysis.py   # sélection vs reste du dataset
    │   ├── fit_score_analysis.py    # score composite adaptatif par poste
    │   ├── similarity_analysis.py   # joueurs au profil proche (gardiens isolés)
    │   ├── target_profile_analysis.py  # recherche par profil-cible
    │   ├── narrative_analysis.py    # phrase d'interprétation dynamique
    │   ├── reliability_analysis.py  # alerte petit effectif
    │   ├── name_resolver.py         # résout un nom saisi vers l'orthographe exacte du CSV
    │   └── market_value_analysis.py # pont dataset <-> PlayerElo (valeur, cache)
    ├── charts/                      # un fichier par graphique
    │   ├── ovr_distribution_chart.py
    │   ├── pac_by_position_chart.py
    │   ├── pac_dri_scatter_chart.py
    │   ├── radar_comparison_chart.py
    │   ├── league_ranking_chart.py
    │   └── correlation_heatmap_chart.py
    ├── tables/
    │   └── ranking_table.py         # tableau trié, dégradé OVR, colonne valeur marchande si connue
    ├── export/
    │   ├── csv_exporter.py          # export de la sélection en CSV
    │   ├── report_exporter.py       # rapport PDF multi-pages (ensemble + par genre)
    │   └── graph_exporter.py        # sauvegarde d'une figure en PNG
    └── api/                         # intégration API PlayerElo (externe au dataset CSV)
        ├── playerelo_config.py      # clé API (variable d'environnement), URL de base
        ├── playerelo_client.py      # requêtes HTTP authentifiées, retry réseau, erreurs lisibles
        ├── player_search.py         # recherche par nom
        ├── player_lookup.py         # recherche par identifiant
        ├── market_value.py          # valeur marchande calculée par PlayerElo
        ├── usage.py                 # suivi du quota (500 requêtes/mois en gratuit)
        └── value_cache.py           # cache disque pour ne pas re-consommer de quota
```

## Choix des graphiques
- **Distribution OVR (sélection vs ensemble)** : répond à « ces joueurs sortent-ils vraiment du lot ? ».
- **Boxplot PAC par poste** : répond à « quel poste est le plus rapide dans la sélection ? ».
- **Scatterplot PAC vs DRI, coloré par championnat** : répond à « existe-t-il un profil rapide ET bon dribbleur ? ». Chaque championnat garde la même couleur sur tous les graphiques (voir `config.build_league_palette`).
- **Heatmap de corrélation** : répond à « quelles qualités vont ensemble dans cette sélection ? ».
- **Classement par championnat** : répond à « où chercher en priorité ? ».
- **Radar de comparaison** : la carte de scouting classique, limitée à 3 joueurs (au-delà, illisible).

## Filtres et état vide
Championnat (avec option d'exclure les 5 grands), poste, seuils minimums sur
OVR, PAC et DRI. Si aucun joueur ne correspond, un message l'indique au lieu
d'afficher des graphiques vides.

## Limite du dataset
Les statistiques (OVR, PAC, DRI…) sont des notes de jeu vidéo (EA Sports FC),
pas des mesures physiques réelles. Certains gardiens affichent par exemple des
stats de champ (PAC, DRI…) élevées bien qu'ils ne les pratiquent jamais en
match — un artefact de la notation du jeu. Le score composite et la
recherche de joueurs similaires isolent désormais les gardiens (jamais
comparés à un joueur de champ), mais le biais reste visible si vous
consultez leurs statistiques brutes dans un tableau.

## Lancer l'application
```bash
pip install -r requirements.txt
streamlit run main.py
```

## Exporter les graphiques en PNG (sans Streamlit)
```bash
python scripts/generate_graphiques.py
```

## Lancer les tests automatisés
```bash
pip install -r requirements-dev.txt
pytest
```
47 tests, aucun appel réseau (la valeur marchande est testée via un cache
isolé, jamais l'API réelle). Couvrent notamment le score composite adaptatif
par poste, l'isolation des gardiens dans la similarité, le résolveur de
noms, et une régression explicite sur le bug de dtype qui cassait le calcul
de distance selon la version de pandas/numpy installée.

## Intégration API PlayerElo (valeur marchande)

L'onglet **Valeur marchande** interroge l'API externe [PlayerElo](https://playerelo.football/api-access)
(78K+ joueurs, indépendante du dataset CSV utilisé partout ailleurs) pour
récupérer une valeur marchande calculée, par nom ou par identifiant PlayerElo.

**Obtenir une clé (gratuite) :**
1. Créer un compte sur https://playerelo.football/api-access (plan Free : 500 requêtes/mois, 10/min).
2. Copier `.env.example` en `.env` à la racine du projet.
3. Coller la clé : `PLAYERELO_API_KEY=pe_live_...`

Sans clé configurée, l'onglet affiche un message d'erreur clair plutôt que
de planter — le reste de l'application fonctionne normalement.

**Pourquoi un cache disque (`data/market_value_cache.json`) :** le plan
gratuit est limité à 500 requêtes/mois. Chaque joueur consulté n'est
interrogé qu'une fois ; les recherches suivantes relisent le cache. Seuls
les succès sont mis en cache — une erreur réseau ou une clé invalide n'est
jamais figée dans le cache, pour qu'une clé corrigée reprenne effet
immédiatement.

**Limite connue :** le rapprochement entre le dataset CSV (statistiques de
jeu EA Sports FC) et PlayerElo (données réelles) se fait par correspondance
de nom, pas par un identifiant partagé — deux joueurs homonymes ou une
orthographe différente peuvent ne pas se recouper correctement. Le filtre
par valeur marchande ne porte que sur les joueurs déjà recherchés dans cet
onglet, pas sur l'ensemble du dataset (interroger les 17 000+ lignes du CSV
dépasserait le quota gratuit en une seule session).

