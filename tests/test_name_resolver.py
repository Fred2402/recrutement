from src.analysis.name_resolver import resolve_canonical_name


def test_resolve_nom_complet_exact(sample_df):
    assert resolve_canonical_name("Ada Rapide", sample_df) == "Ada Rapide"


def test_resolve_insensible_a_la_casse_et_aux_accents(sample_df):
    assert resolve_canonical_name("ada rapide", sample_df) == "Ada Rapide"


def test_resolve_nom_partiel_unique(sample_df):
    assert resolve_canonical_name("Defenseur", sample_df) == "Cy Defenseur"


def test_resolve_nom_ambigu_reste_inchange(sample_df):
    # "Rapide" correspond à deux joueuses (Ada et Elle) : on ne devine pas.
    assert resolve_canonical_name("Rapide", sample_df) == "Rapide"


def test_resolve_nom_inconnu_reste_inchange(sample_df):
    assert resolve_canonical_name("Zzz Inexistant", sample_df) == "Zzz Inexistant"
