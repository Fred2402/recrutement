"""Génère les graphiques principaux en PNG, avec les filtres par défaut,
sans lancer Streamlit.

Usage : python scripts/generate_graphiques.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.charts.correlation_heatmap_chart import build_correlation_heatmap_chart
from src.charts.league_ranking_chart import build_league_ranking_chart
from src.charts.ovr_distribution_chart import build_ovr_distribution_chart
from src.charts.pac_by_position_chart import build_pac_by_position_chart
from src.charts.pac_dri_scatter_chart import build_pac_dri_scatter_chart
from src.config import DEFAULT_DRI_MIN, DEFAULT_OVR_MIN, DEFAULT_PAC_MIN, DEFAULT_POSITIONS, build_league_palette
from src.data_loader import load_players
from src.export.graph_exporter import save_figure
from src.filters.apply_filters import apply_all_filters

df = load_players()
palette = build_league_palette(df)

sel = apply_all_filters(
    df,
    ligues=[],
    postes=DEFAULT_POSITIONS,
    ovr_min=DEFAULT_OVR_MIN,
    pac_min=DEFAULT_PAC_MIN,
    dri_min=DEFAULT_DRI_MIN,
    exclure_grands=True,
)

save_figure(build_ovr_distribution_chart(df, sel), "1_distribution_ovr.png")
save_figure(build_pac_by_position_chart(sel), "2_pac_par_poste.png")
save_figure(build_pac_dri_scatter_chart(sel, palette), "3_pac_vs_dri.png")
save_figure(build_league_ranking_chart(sel), "4_classement_championnats.png")
save_figure(build_correlation_heatmap_chart(sel), "5_correlations.png")

print(f"{len(sel)} joueurs sélectionnés — 5 graphiques exportés dans graphique/")
