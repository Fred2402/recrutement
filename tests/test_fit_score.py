from src.analysis.fit_score_analysis import (
    POSITION_WEIGHT_PROFILES,
    compute_fit_score,
    get_top_recommendation,
    get_weights_for_positions,
)


def test_weights_attaquant():
    assert get_weights_for_positions(["RW", "LW"]) == POSITION_WEIGHT_PROFILES["ATTAQUANT"]


def test_weights_defenseur():
    assert get_weights_for_positions(["CB"]) == POSITION_WEIGHT_PROFILES["DEFENSEUR"]


def test_weights_postes_melanges_retombe_sur_defaut():
    from src.analysis.fit_score_analysis import DEFAULT_WEIGHTS
    assert get_weights_for_positions(["RW", "CB"]) == DEFAULT_WEIGHTS


def test_weights_aucun_poste_retombe_sur_defaut():
    from src.analysis.fit_score_analysis import DEFAULT_WEIGHTS
    assert get_weights_for_positions([]) == DEFAULT_WEIGHTS


def test_compute_fit_score_exclut_les_gardiens(sample_df):
    resultat = compute_fit_score(sample_df)
    assert "GK" not in resultat["Position"].values


def test_compute_fit_score_sur_selection_vide(sample_df):
    vide = sample_df.iloc[0:0]
    resultat = compute_fit_score(vide)
    assert resultat.empty


def test_get_top_recommendation_ordre_decroissant(sample_df):
    top = get_top_recommendation(sample_df, top_n=3)
    scores = top["Score"].tolist()
    assert scores == sorted(scores, reverse=True)


def test_score_defenseur_valorise_def_phy(sample_df):
    """Avec la pondération défenseur, Cy Defenseur (DEF 88, PHY 82) doit
    dominer Ada Rapide (DEF 30) malgré un OVR/PAC plus faible."""
    poids_def = get_weights_for_positions(["CB"])
    resultat = compute_fit_score(sample_df, poids_def)
    meilleur = resultat.iloc[0]
    assert meilleur["Name"] == "Cy Defenseur"
