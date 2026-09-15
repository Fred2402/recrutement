"""Cellule de recrutement — tableau de bord complet.

streamlit run main.py
"""

import streamlit as st

from src.analysis.comparison_analysis import compare_selection_vs_rest
from src.analysis.fit_score_analysis import get_top_recommendation, get_weights_for_positions
from src.analysis.kpi_analysis import compute_kpis
from src.analysis.market_value_analysis import (
    attach_market_value,
    build_market_value_lookup,
    fetch_value_by_id,
    get_cached_values_table,
)
from src.analysis.name_resolver import resolve_canonical_name
from src.analysis.narrative_analysis import build_narrative
from src.analysis.reliability_analysis import check_reliability
from src.analysis.similarity_analysis import find_similar_players
from src.analysis.target_profile_analysis import find_players_matching_target
from src.api.player_search import search_players_by_name
from src.api.playerelo_client import PlayerEloError
from src.charts.correlation_heatmap_chart import build_correlation_heatmap_chart
from src.charts.league_ranking_chart import build_league_ranking_chart
from src.charts.ovr_distribution_chart import build_ovr_distribution_chart
from src.charts.pac_by_position_chart import build_pac_by_position_chart
from src.charts.pac_dri_scatter_chart import build_pac_dri_scatter_chart
from src.charts.radar_comparison_chart import build_radar_comparison_chart
from src.config import (
    DEFAULT_DRI_MIN,
    DEFAULT_OVR_MIN,
    DEFAULT_PAC_MIN,
    DEFAULT_POSITIONS,
    STATS_CLES,
    STATS_SIMILARITE,
    build_league_palette,
)
from src.data_loader import load_players
from src.export.csv_exporter import export_selection_to_csv
from src.export.report_exporter import export_report_pdf
from src.filters.apply_filters import apply_all_filters
from src.filters.budget_filter import filter_by_budget
from src.filters.league_filter import get_active_exclusions
from src.tables.ranking_table import build_ranking_table

st.set_page_config(page_title="Cellule de recrutement", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Sora:wght@600;700;800&display=swap');

    :root {
        --accent: #4F46E5;
        --accent-dark: #4338CA;
        --accent-soft: #EEF2FF;
        --gold: #F59E0B;
        --gold-soft: #FFFBEB;
        --ink: #1E1B2E;
        --muted: #64748B;
        --card-bg: #FFFFFF;
        --page-bg: #F6F7FB;
        --border: #E5E7EB;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: var(--page-bg);
    }

    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 1200px;}

    h1, h2, h3 {
        font-family: 'Sora', sans-serif;
        color: var(--ink);
        letter-spacing: -0.02em;
    }
    h1 {font-weight: 800; font-size: 2.1rem;}

    p, .stMarkdown, .stCaption {color: var(--ink);}
    .stCaption, [data-testid="stCaptionContainer"] {color: var(--muted) !important;}

    /* --- Sidebar --- */
    section[data-testid="stSidebar"] {
        background: var(--card-bg);
        border-right: 1px solid var(--border);
    }
    section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] label {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: var(--ink);
    }

    /* --- Chiffres clés (st.metric) en cartes --- */
    div[data-testid="stMetric"] {
        background: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1rem 1.1rem;
        box-shadow: 0 1px 3px rgba(30, 27, 46, 0.04);
    }
    div[data-testid="stMetricLabel"] {
        font-weight: 600; color: var(--muted); text-transform: uppercase;
        font-size: 0.72rem; letter-spacing: 0.04em;
    }
    div[data-testid="stMetricValue"] {
        font-family: 'Sora', sans-serif; font-size: 1.65rem; color: var(--ink);
    }

    /* --- Carte verdict --- */
    .verdict-card {
        background: linear-gradient(135deg, var(--accent-soft) 0%, #FFFFFF 100%);
        border: 1px solid #DDD6FE;
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        margin: 0.5rem 0 1.3rem 0;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.08);
        position: relative;
        overflow: hidden;
    }
    .verdict-card::before {
        content: "";
        position: absolute; top: 0; left: 0; bottom: 0; width: 5px;
        background: linear-gradient(180deg, var(--accent), var(--gold));
    }
    .verdict-card .meta {font-size: 0.82rem; color: var(--muted); font-weight: 500; letter-spacing: 0.02em;}
    .verdict-card .name {font-family: 'Sora', sans-serif; font-size: 1.3rem; font-weight: 700; color: var(--ink); margin: 0.15rem 0;}
    .verdict-card .score {
        font-family: 'Sora', sans-serif; font-size: 1.6rem; font-weight: 800;
        color: var(--accent-dark); margin: 0.3rem 0;
    }

    /* --- Onglets --- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px; background: var(--card-bg); padding: 6px; border-radius: 12px;
        border: 1px solid var(--border);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px; padding: 8px 16px; font-weight: 600; color: var(--muted);
    }
    .stTabs [aria-selected="true"] {
        background: var(--accent) !important; color: white !important;
    }

    /* --- Boutons --- */
    .stButton > button, .stDownloadButton > button {
        border-radius: 10px; font-weight: 600; border: 1px solid var(--accent);
        color: var(--accent); background: white; transition: all 0.15s ease;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background: var(--accent); color: white;
    }

    /* --- Cartes (data editor / dataframe) --- */
    div[data-testid="stDataFrame"] {
        border: 1px solid var(--border); border-radius: 12px; overflow: hidden;
    }

    /* --- Champs de saisie --- */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        border-radius: 8px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def get_data():
    return load_players()


df = get_data()
league_palette = build_league_palette(df)

st.title("Cellule de recrutement — Tableau de bord")
st.caption(
    "Question métier : trouver un ailier rapide et bon dribbleur, "
    "hors des cinq grands championnats, note générale supérieure à 75."
)

# --- Filtres (sidebar, agissent sur toutes les vues) ---
st.sidebar.header("Filtres")

ligues_dispo = sorted(df["League"].unique())
ligues = st.sidebar.multiselect("Championnat", ligues_dispo)
exclure_grands = st.sidebar.checkbox("Exclure les 5 grands championnats", value=True)

postes_dispo = sorted(df["Position"].unique())
defaut_postes = [p for p in DEFAULT_POSITIONS if p in postes_dispo]
postes = st.sidebar.multiselect("Poste", postes_dispo, default=defaut_postes)

genres_dispo = sorted(df["gender"].unique())
libelles_genre = {"M": "Hommes", "F": "Femmes"}
genres = st.sidebar.multiselect(
    "Genre", genres_dispo, format_func=lambda g: libelles_genre.get(g, g)
)

ovr_min = st.sidebar.slider("OVR minimum", 40, 99, DEFAULT_OVR_MIN)
pac_min = st.sidebar.slider("PAC minimum (vitesse)", 20, 99, DEFAULT_PAC_MIN)
dri_min = st.sidebar.slider("DRI minimum (dribble)", 20, 99, DEFAULT_DRI_MIN)

exclusions_actives = get_active_exclusions(ligues, exclure_grands)
if ligues and exclure_grands:
    st.sidebar.caption(
        "Championnat(s) choisi(s) explicitement : la case \"exclure les 5 grands\" "
        "est ignorée tant qu'un championnat est sélectionné ci-dessus."
    )
elif exclusions_actives:
    st.sidebar.caption("Championnats exclus : " + ", ".join(exclusions_actives))
else:
    st.sidebar.caption("Aucun championnat exclu.")

sel = apply_all_filters(df, ligues, postes, ovr_min, pac_min, dri_min, exclure_grands, genres)
sel = attach_market_value(sel)

valeurs_connues = build_market_value_lookup()
if valeurs_connues:
    budget_max = st.sidebar.number_input(
        "Budget max — valeur marchande PlayerElo (€)",
        min_value=0, value=200_000_000, step=1_000_000,
    )
    uniquement_valeurs_connues = st.sidebar.checkbox(
        "Ne garder que les joueurs avec valeur marchande connue", value=False
    )
    sel = filter_by_budget(sel, budget_max, uniquement_valeurs_connues)
    st.sidebar.caption(
        f"{len(valeurs_connues)} joueur(s) avec valeur marchande connue (onglet Valeur marchande)."
    )
else:
    st.sidebar.caption(
        "Filtre budget indisponible : aucune valeur marchande consultée pour l'instant "
        "(onglet Valeur marchande)."
    )

# --- Phrase d'interprétation dynamique (toujours visible, avant les chiffres) ---
st.markdown(build_narrative(df, sel))

alerte_fiabilite = check_reliability(sel)
if alerte_fiabilite:
    st.warning(alerte_fiabilite)

# --- Chiffres clés ---
kpis = compute_kpis(df, sel)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Joueurs trouvés", kpis["count"], f"{kpis['pct_dataset']} % du dataset" if kpis["count"] else None)
c2.metric("OVR moyen", kpis["moyennes"].get("OVR", "—"),
          f"{kpis['deltas'].get('OVR', 0):+.1f} vs ensemble" if kpis["count"] else None)
c3.metric("PAC moyen", kpis["moyennes"].get("PAC", "—"),
          f"{kpis['deltas'].get('PAC', 0):+.1f} vs ensemble" if kpis["count"] else None)
c4.metric("DRI moyen", kpis["moyennes"].get("DRI", "—"),
          f"{kpis['deltas'].get('DRI', 0):+.1f} vs ensemble" if kpis["count"] else None)

if sel.empty:
    st.warning("Aucun joueur ne correspond à ces critères. Élargissez les filtres.")
    st.stop()

# --- Verdict : le meilleur profil identifié, avant tout le reste ---
poids_actifs = get_weights_for_positions(postes)
libelle_poids = " · ".join(f"{stat} {int(p * 100)} %" for stat, p in poids_actifs.items())

top3_df = get_top_recommendation(sel, poids_actifs, top_n=3)
top3_noms = top3_df["Name"].tolist()

if top3_df.empty:
    st.info(
        "Aucun profil évaluable par le score composite dans cette sélection "
        "(les gardiens en sont exclus — voir doc/README.md)."
    )
else:
    top1 = top3_df.iloc[0]
    st.markdown(
        f"""
        <div class="verdict-card">
            <div class="meta">MEILLEUR PROFIL IDENTIFIÉ</div>
            <div class="name">{top1['Name']} — {top1['Team']} ({top1['League']})</div>
            <div class="meta">Poste : {top1['Position']} · OVR {top1['OVR']} · PAC {top1['PAC']} · DRI {top1['DRI']}</div>
            <div class="score">Score {top1['Score']}/100</div>
            <div class="meta">Pondération adaptée au poste filtré : {libelle_poids}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

tab_apercu, tab_visu, tab_classement, tab_comparateur, tab_fiche, tab_cible, tab_valeur, tab_export = st.tabs(
    ["Vue d'ensemble", "Visualisations", "Classements", "Comparateur",
     "Fiche joueur", "Profil-cible", "Valeur marchande", "Export"]
)

# --- Onglet 1 : vue d'ensemble ---
with tab_apercu:
    col_gauche, col_droite = st.columns([1, 1])
    with col_gauche:
        st.markdown("**Où se place la sélection sur OVR ?**")
        st.pyplot(build_ovr_distribution_chart(df, sel))
    with col_droite:
        st.markdown("**Sélection vs reste du dataset**")
        st.dataframe(compare_selection_vs_rest(df, sel), use_container_width=True, hide_index=True)

    st.markdown("**Meilleurs profils** (les 3 mieux notés sur le score composite sont surlignés)")
    st.dataframe(build_ranking_table(sel, top_names=top3_noms), use_container_width=True)

# --- Onglet 2 : visualisations ---
with tab_visu:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**PAC par poste** — quel poste est le plus rapide dans la sélection ?")
        st.pyplot(build_pac_by_position_chart(sel))
    with col2:
        st.markdown("**Vitesse vs Dribble** — coloré par championnat, top 3 cerclé")
        st.pyplot(build_pac_dri_scatter_chart(sel, league_palette, top_names=top3_noms))

    st.markdown("**Corrélations entre statistiques** — quels profils vont ensemble ?")
    st.pyplot(build_correlation_heatmap_chart(sel))

# --- Onglet 3 : classements ---
with tab_classement:
    stat_choisie = st.selectbox("Statistique à classer", STATS_CLES, index=0)
    st.markdown(f"**Quel championnat porte les meilleurs profils sur {stat_choisie} ?**")
    st.pyplot(build_league_ranking_chart(sel, stat=stat_choisie, excluded_leagues=exclusions_actives))

# --- Onglet 4 : comparateur de joueurs (radar) ---
with tab_comparateur:
    st.markdown("Choisissez 2 ou 3 joueurs de la sélection à comparer.")
    noms_dispo = sel.sort_values("OVR", ascending=False)["Name"].tolist()
    noms_choisis = st.multiselect("Joueurs à comparer", noms_dispo, default=noms_dispo[:2], max_selections=3)
    if noms_choisis:
        st.pyplot(build_radar_comparison_chart(sel, noms_choisis))
    else:
        st.info("Sélectionnez au moins un joueur.")

# --- Onglet 5 : fiche joueur + alternatives ---
with tab_fiche:
    joueur = st.selectbox(
        "Joueur", sel.sort_values("OVR", ascending=False)["Name"].tolist(), key="fiche_joueur"
    )
    ligne = sel[sel["Name"] == joueur].iloc[0]

    col_info, col_radar = st.columns([1, 1])
    with col_info:
        st.markdown(f"**{ligne['Name']}**")
        st.markdown(
            f"{ligne['Team']} · {ligne['League']} · {ligne['Position']} · {int(ligne['Age'])} ans\n\n"
            f"OVR {ligne['OVR']} · PAC {ligne['PAC']} · SHO {ligne['SHO']} · "
            f"PAS {ligne['PAS']} · DRI {ligne['DRI']} · DEF {ligne['DEF']} · PHY {ligne['PHY']}"
        )
    with col_radar:
        st.pyplot(build_radar_comparison_chart(sel, [joueur]))

    st.markdown("**Alternatives au profil** — joueurs statistiquement proches, dans tout le dataset")
    st.dataframe(build_ranking_table(find_similar_players(df, joueur, top_n=5)), use_container_width=True)

# --- Onglet 6 : profil-cible (recherche sans partir d'un joueur existant) ---
with tab_cible:
    st.markdown("Construisez un profil-cible avec les curseurs, sans partir d'un joueur existant. "
               "La recherche porte sur tout le dataset, indépendamment des filtres ci-dessus.")
    cols = st.columns(len(STATS_SIMILARITE))
    cible = {}
    for col, stat in zip(cols, STATS_SIMILARITE):
        with col:
            cible[stat] = st.slider(stat, 20, 99, 75, key=f"cible_{stat}")

    resultats_cible = find_players_matching_target(df, cible, top_n=10)
    st.markdown("**Joueurs les plus proches de ce profil**")
    st.dataframe(build_ranking_table(resultats_cible), use_container_width=True)

# --- Onglet 7 : valeur marchande (PlayerElo) ---
with tab_valeur:
    st.markdown(
        "Données externes à l'API **PlayerElo** (78K+ joueurs), séparées du dataset de statistiques "
        "de jeu utilisé partout ailleurs dans l'application. Nécessite une clé API "
        "(`PLAYERELO_API_KEY`) — voir `doc/README.md`."
    )

    nom_recherche = st.text_input("Rechercher un joueur", value=joueur, placeholder="Nom du joueur...")
    if st.button("Chercher", key="btn_chercher_nom") and nom_recherche:
        nom_a_chercher = resolve_canonical_name(nom_recherche, df)

        # Le nom résolu localement (ex. "Neymar Jr", nom complet du CSV) peut être
        # PLUS LONG que ce que PlayerElo stocke (ex. "Neymar" tout court) : une
        # recherche par sous-chaîne sur la version enrichie échoue alors qu'elle
        # aurait marché sur le nom brut. On essaie donc le nom tel quel D'ABORD,
        # la version résolue seulement en repli, sans doublon si les deux sont
        # identiques.
        variantes = [nom_recherche, nom_a_chercher, nom_recherche.title(), nom_a_chercher.title()]
        variantes = list(dict.fromkeys(v for v in variantes if v))  # dédoublonne, garde l'ordre

        candidats = []
        try:
            for variante in variantes:
                candidats = search_players_by_name(variante, limit=15)
                if candidats:
                    break
        except PlayerEloError as erreur:
            candidats = []
            st.error(str(erreur))

        st.session_state["candidats_valeur"] = candidats
        st.session_state.pop("dernier_resultat_valeur", None)

    candidats = st.session_state.get("candidats_valeur", [])

    if candidats:
        # Filtres appliqués localement sur les résultats déjà reçus : aucun
        # appel API supplémentaire, contrairement à des filtres côté serveur.
        postes_dispo = ["Tous les postes"] + sorted({c.get("position") or "?" for c in candidats})
        ligues_dispo = ["Tous les championnats"] + sorted({c.get("current_league") or "?" for c in candidats})

        col_f1, col_f2, col_f3, col_f4 = st.columns([1, 1, 1, 1])
        with col_f1:
            poste_choisi = st.selectbox("Poste", postes_dispo, key="filtre_poste_valeur")
        with col_f2:
            ligue_choisie = st.selectbox("Championnat", ligues_dispo, key="filtre_ligue_valeur")
        with col_f3:
            club_filtre = st.text_input("Club contient...", key="filtre_club_valeur")
        with col_f4:
            agents_libres = st.checkbox("Agents libres uniquement", key="filtre_agents_libres")

        resultats_filtres = candidats
        if poste_choisi != "Tous les postes":
            resultats_filtres = [c for c in resultats_filtres if c.get("position") == poste_choisi]
        if ligue_choisie != "Tous les championnats":
            resultats_filtres = [c for c in resultats_filtres if c.get("current_league") == ligue_choisie]
        if club_filtre:
            resultats_filtres = [
                c for c in resultats_filtres
                if club_filtre.lower() in (c.get("current_team") or "").lower()
            ]
        if agents_libres:
            resultats_filtres = [c for c in resultats_filtres if not c.get("current_team")]

        st.caption(f"{len(resultats_filtres)} / {len(candidats)} résultat(s) après filtrage")

        if resultats_filtres:
            options = {
                f"{c.get('player_name')} — {c.get('current_team') or 'agent libre'} "
                f"({c.get('current_league', '?')}) — Elo {c.get('elo', '?')}": c.get("player_id")
                for c in resultats_filtres
            }
            choix = st.selectbox("Résultats", list(options.keys()), key="choix_candidat_valeur")
            if st.button("Voir la valeur marchande", key="btn_valeur_candidat"):
                st.session_state["dernier_resultat_valeur"] = fetch_value_by_id(options[choix])
        else:
            st.info("Aucun résultat avec ces filtres.")
    elif "candidats_valeur" in st.session_state:
        st.warning("Aucun joueur PlayerElo trouvé pour ce nom.")

    dernier = st.session_state.get("dernier_resultat_valeur")
    if dernier:
        if "erreur" in dernier:
            st.error(dernier["erreur"])
        else:
            st.metric(
                "Valeur marchande estimée",
                f"{dernier['valeur_eur']:,} €" if dernier.get("valeur_eur") is not None else "Non communiquée",
            )
            st.caption(
                f"{dernier.get('nom_playerelo', '?')} · {dernier.get('club') or 'agent libre'} "
                f"({dernier.get('ligue', '?')}) · {dernier.get('poste', '?')} · "
                f"Elo {dernier.get('elo', '?')} · player_id {dernier['player_id']}"
            )

    st.markdown("**Valeurs déjà consultées** (filtre par valeur marchande, sur ce qui a été recherché)")
    table_valeurs = get_cached_values_table()
    if table_valeurs.empty:
        st.info("Aucune valeur marchande consultée pour l'instant.")
    else:
        bornes = table_valeurs["Valeur marchande (€)"].dropna()
        if len(bornes.unique()) > 1:
            plage = st.slider(
                "Filtrer par valeur marchande (€)",
                int(bornes.min()), int(bornes.max()),
                (int(bornes.min()), int(bornes.max())),
            )
            table_valeurs = table_valeurs[
                table_valeurs["Valeur marchande (€)"].between(plage[0], plage[1])
            ]
        elif len(bornes.unique()) == 1:
            st.caption(f"Une seule valeur en cache pour l'instant ({int(bornes.iloc[0]):,} €) "
                      "— le filtre par plage apparaîtra dès qu'il y en aura au moins deux différentes.")
        st.dataframe(table_valeurs, use_container_width=True, hide_index=True)

# --- Onglet 8 : export ---
with tab_export:
    st.markdown(f"**{len(sel)} joueurs** correspondent aux critères actuels.")

    col_csv, col_pdf = st.columns(2)
    with col_csv:
        st.download_button(
            "Télécharger la sélection (CSV)",
            data=export_selection_to_csv(sel),
            file_name="selection_recrutement.csv",
            mime="text/csv",
        )
    with col_pdf:
        if st.button("Générer le rapport (PDF)"):
            chemin_pdf = export_report_pdf(df, sel, league_palette, poids_actifs)
            with open(chemin_pdf, "rb") as f:
                st.download_button("Télécharger le rapport (PDF)", data=f, file_name="rapport_recrutement.pdf",
                                  mime="application/pdf")
