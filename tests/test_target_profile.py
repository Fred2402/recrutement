from src.analysis.target_profile_analysis import find_players_matching_target


def test_profil_cible_ordre_croissant_de_distance(sample_df):
    cible = {"PAC": 90, "SHO": 70, "PAS": 65, "DRI": 85, "DEF": 30, "PHY": 60}
    resultat = find_players_matching_target(sample_df, cible, top_n=5)
    distances = resultat["Distance au profil"].tolist()
    assert distances == sorted(distances)
    # Le profil-cible est exactement celui de "Ada Rapide" : elle doit sortir en tête.
    assert resultat.iloc[0]["Name"] == "Ada Rapide"


def test_profil_cible_ignore_les_stats_non_fournies(sample_df):
    resultat = find_players_matching_target(sample_df, {"DEF": 88}, top_n=1)
    assert resultat.iloc[0]["Name"] == "Cy Defenseur"


def test_profil_cible_dict_vide_renvoie_vide(sample_df):
    assert find_players_matching_target(sample_df, {}, top_n=5).empty
