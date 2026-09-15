import pandas as pd


def test_attach_market_value_avec_cache(monkeypatch, tmp_path, sample_df):
    cache_file = tmp_path / "cache_test.json"
    monkeypatch.setattr("src.api.value_cache.CACHE_PATH", cache_file)

    from src.api.value_cache import save_to_cache
    save_to_cache("recherche libre", {"nom_playerelo": "Ada Rapide", "valeur_eur": 12_000_000})

    from src.analysis.market_value_analysis import attach_market_value
    resultat = attach_market_value(sample_df)

    ligne_connue = resultat[resultat["Name"] == "Ada Rapide"].iloc[0]
    assert ligne_connue["Valeur marchande (€)"] == 12_000_000

    ligne_inconnue = resultat[resultat["Name"] == "Bo Milieu"].iloc[0]
    assert pd.isna(ligne_inconnue["Valeur marchande (€)"])


def test_attach_market_value_cache_vide(monkeypatch, tmp_path, sample_df):
    cache_file = tmp_path / "cache_vide.json"
    monkeypatch.setattr("src.api.value_cache.CACHE_PATH", cache_file)

    from src.analysis.market_value_analysis import attach_market_value
    resultat = attach_market_value(sample_df)
    assert resultat["Valeur marchande (€)"].isna().all()


def test_lookup_ignore_les_entrees_en_erreur(monkeypatch, tmp_path):
    cache_file = tmp_path / "cache_erreurs.json"
    monkeypatch.setattr("src.api.value_cache.CACHE_PATH", cache_file)

    from src.api.value_cache import save_to_cache
    save_to_cache("echec", {"erreur": "Clé invalide"})

    from src.analysis.market_value_analysis import build_market_value_lookup
    assert build_market_value_lookup() == {}
