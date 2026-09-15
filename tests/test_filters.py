import pandas as pd

from src.filters.apply_filters import apply_all_filters
from src.filters.budget_filter import filter_by_budget
from src.filters.gender_filter import filter_by_gender
from src.filters.league_filter import filter_by_league, get_active_exclusions
from src.filters.position_filter import filter_by_position
from src.filters.threshold_filter import filter_by_thresholds


def test_filter_by_thresholds(sample_df):
    resultat = filter_by_thresholds(sample_df, ovr_min=78, pac_min=0, dri_min=0)
    assert set(resultat["Name"]) == {"Ada Rapide", "Bo Milieu", "Dee Gardien", "Elle Rapide"}


def test_filter_by_position_vide_retourne_tout(sample_df):
    assert len(filter_by_position(sample_df, [])) == len(sample_df)


def test_filter_by_position_filtre(sample_df):
    resultat = filter_by_position(sample_df, ["GK"])
    assert set(resultat["Position"]) == {"GK"}


def test_filter_by_gender(sample_df):
    hommes = filter_by_gender(sample_df, ["M"])
    femmes = filter_by_gender(sample_df, ["F"])
    assert len(hommes) + len(femmes) == len(sample_df)
    assert set(hommes["gender"]) == {"M"}
    assert set(femmes["gender"]) == {"F"}


def test_filter_by_league_exclusion(sample_df):
    resultat = filter_by_league(sample_df, ligues=[], exclure_grands=True)
    # Premier League, Bundesliga, LALIGA EA SPORTS, Serie A Enilive, Ligue 1 McDonald's
    # sont les 5 grands : il ne doit rester que Liga F.
    assert set(resultat["League"]) == {"Liga F"}


def test_filter_by_league_selection_explicite_prime(sample_df):
    resultat = filter_by_league(sample_df, ligues=["Premier League"], exclure_grands=True)
    assert set(resultat["League"]) == {"Premier League"}


def test_get_active_exclusions():
    assert get_active_exclusions(ligues=[], exclure_grands=True) != []
    assert get_active_exclusions(ligues=["Premier League"], exclure_grands=True) == []
    assert get_active_exclusions(ligues=[], exclure_grands=False) == []


def test_apply_all_filters_combine_tout(sample_df):
    resultat = apply_all_filters(
        sample_df, ligues=[], postes=["RW", "LW"], ovr_min=0, pac_min=0, dri_min=0,
        exclure_grands=False, genres=["F"],
    )
    assert set(resultat["Name"]) == {"Elle Rapide"}


def test_filter_by_budget_sans_colonne_ne_filtre_rien(sample_df):
    assert len(filter_by_budget(sample_df, budget_max=1000, uniquement_connues=False)) == len(sample_df)


def test_filter_by_budget_avec_colonne():
    df = pd.DataFrame({
        "Name": ["A", "B", "C"],
        "Valeur marchande (€)": [1_000_000, 50_000_000, None],
    })
    # Par défaut, une valeur inconnue n'est jamais exclue.
    resultat = filter_by_budget(df, budget_max=10_000_000, uniquement_connues=False)
    assert set(resultat["Name"]) == {"A", "C"}

    # Avec l'option activée, seules les valeurs connues ET sous le budget restent.
    resultat_strict = filter_by_budget(df, budget_max=10_000_000, uniquement_connues=True)
    assert set(resultat_strict["Name"]) == {"A"}
