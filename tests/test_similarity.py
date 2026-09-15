from src.analysis.similarity_analysis import find_similar_players


def test_similarite_gardien_isole_aux_gardiens(sample_df):
    resultat = find_similar_players(sample_df, "Dee Gardien", top_n=5)
    assert set(resultat["Position"]) == {"GK"}
    assert "Dee Gardien" not in resultat["Name"].values


def test_similarite_joueur_de_champ_exclut_les_gardiens(sample_df):
    resultat = find_similar_players(sample_df, "Ada Rapide", top_n=5)
    assert "GK" not in resultat["Position"].values
    assert "Ada Rapide" not in resultat["Name"].values


def test_similarite_nom_inconnu_renvoie_vide(sample_df):
    resultat = find_similar_players(sample_df, "Nom Qui N'existe Pas", top_n=5)
    assert resultat.empty


def test_similarite_ne_leve_pas_avec_dtype_mixte(sample_df):
    """Régression : extraire une ligne d'un DataFrame mêlant texte et nombres
    force les stats en dtype object, ce qui faisait planter np.sqrt selon la
    version de pandas/numpy installée. Ce test échoue si le cast explicite
    en float est retiré du code.
    """
    resultat = find_similar_players(sample_df, "Ada Rapide", top_n=3)
    assert not resultat.empty
    assert resultat["Distance"].dtype.kind in "fc"  # float, pas object
