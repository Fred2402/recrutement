from src.analysis.comparison_analysis import compare_selection_vs_rest
from src.analysis.kpi_analysis import compute_kpis
from src.analysis.narrative_analysis import build_narrative
from src.analysis.reliability_analysis import SEUIL_FIABILITE, check_reliability


def test_compute_kpis_sur_selection_vide(sample_df):
    vide = sample_df.iloc[0:0]
    resultat = compute_kpis(sample_df, vide)
    assert resultat["count"] == 0
    assert resultat["moyennes"] == {}


def test_compute_kpis_calcule_les_deltas(sample_df):
    resultat = compute_kpis(sample_df, sample_df[sample_df["Position"] == "GK"])
    assert resultat["count"] == 2
    assert "PAC" in resultat["deltas"]


def test_compare_selection_vs_rest_colonnes(sample_df):
    resultat = compare_selection_vs_rest(sample_df, sample_df.head(2))
    assert set(resultat.columns) == {"Statistique", "Sélection", "Reste du dataset", "Écart"}


def test_compare_selection_vs_rest_vide(sample_df):
    vide = sample_df.iloc[0:0]
    resultat = compare_selection_vs_rest(sample_df, vide)
    assert resultat.empty


def test_build_narrative_selection_vide(sample_df):
    vide = sample_df.iloc[0:0]
    assert "Aucun joueur" in build_narrative(sample_df, vide)


def test_build_narrative_mentionne_le_nombre(sample_df):
    narration = build_narrative(sample_df, sample_df.head(2))
    assert "2 joueur" in narration


def test_reliability_sous_le_seuil_alerte(sample_df):
    petite_selection = sample_df.head(SEUIL_FIABILITE - 1)
    assert check_reliability(petite_selection) is not None


def test_reliability_selection_vide_pas_d_alerte(sample_df):
    assert check_reliability(sample_df.iloc[0:0]) is None
