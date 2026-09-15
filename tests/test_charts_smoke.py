import matplotlib
matplotlib.use("Agg")  # aucun affichage : les tests tournent sans écran

import matplotlib.pyplot as plt

from src.charts.correlation_heatmap_chart import build_correlation_heatmap_chart
from src.charts.league_ranking_chart import build_league_ranking_chart
from src.charts.ovr_distribution_chart import build_ovr_distribution_chart
from src.charts.pac_by_position_chart import build_pac_by_position_chart
from src.charts.pac_dri_scatter_chart import build_pac_dri_scatter_chart
from src.charts.radar_comparison_chart import build_radar_comparison_chart
from src.config import build_league_palette


def test_ovr_distribution_chart_ne_plante_pas(sample_df):
    fig = build_ovr_distribution_chart(sample_df, sample_df.head(3))
    assert isinstance(fig, plt.Figure)


def test_pac_by_position_chart_selection_vide(sample_df):
    fig = build_pac_by_position_chart(sample_df.iloc[0:0])
    assert isinstance(fig, plt.Figure)


def test_pac_dri_scatter_chart_avec_top_names(sample_df):
    palette = build_league_palette(sample_df)
    fig = build_pac_dri_scatter_chart(sample_df, palette, top_names=["Ada Rapide"])
    assert isinstance(fig, plt.Figure)


def test_radar_comparison_chart_un_seul_joueur(sample_df):
    fig = build_radar_comparison_chart(sample_df, ["Ada Rapide"])
    assert isinstance(fig, plt.Figure)


def test_league_ranking_chart_avec_exclusions(sample_df):
    fig = build_league_ranking_chart(sample_df, stat="OVR", excluded_leagues=["Premier League"])
    assert isinstance(fig, plt.Figure)


def test_correlation_heatmap_petite_selection_ne_plante_pas(sample_df):
    fig = build_correlation_heatmap_chart(sample_df.head(2))
    assert isinstance(fig, plt.Figure)
