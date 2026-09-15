import pandas as pd
import pytest


@pytest.fixture
def sample_df():
    """Petit dataset synthétique couvrant les cas limites qui ont posé
    problème en cours de route : gardien mélangé aux joueurs de champ,
    homonymes, les deux genres, plusieurs championnats.
    """
    return pd.DataFrame([
        {"Name": "Ada Rapide", "OVR": 80, "PAC": 90, "SHO": 70, "PAS": 65, "DRI": 85, "DEF": 30, "PHY": 60,
         "Position": "RW", "League": "Premier League", "Team": "Testville", "Nation": "France",
         "Age": 24, "gender": "M"},
        {"Name": "Bo Milieu", "OVR": 78, "PAC": 70, "SHO": 65, "PAS": 88, "DRI": 80, "DEF": 55, "PHY": 65,
         "Position": "CM", "League": "Ligue 1 McDonald's", "Team": "Testville", "Nation": "France",
         "Age": 27, "gender": "M"},
        {"Name": "Cy Defenseur", "OVR": 76, "PAC": 65, "SHO": 30, "PAS": 60, "DRI": 55, "DEF": 88, "PHY": 82,
         "Position": "CB", "League": "Bundesliga", "Team": "Testburg", "Nation": "Germany",
         "Age": 29, "gender": "M"},
        {"Name": "Dee Gardien", "OVR": 79, "PAC": 50, "SHO": 20, "PAS": 55, "DRI": 40, "DEF": 20, "PHY": 78,
         "Position": "GK", "League": "LALIGA EA SPORTS", "Team": "Testburg", "Nation": "Spain",
         "Age": 30, "gender": "M"},
        {"Name": "Elle Rapide", "OVR": 81, "PAC": 88, "SHO": 72, "PAS": 68, "DRI": 84, "DEF": 32, "PHY": 58,
         "Position": "LW", "League": "Serie A Enilive", "Team": "Testinas", "Nation": "Italy",
         "Age": 23, "gender": "F"},
        {"Name": "Fee Milieu", "OVR": 74, "PAC": 68, "SHO": 60, "PAS": 85, "DRI": 78, "DEF": 50, "PHY": 60,
         "Position": "CAM", "League": "Liga F", "Team": "Testinas", "Nation": "Spain",
         "Age": 26, "gender": "F"},
        {"Name": "Gus Gardien", "OVR": 77, "PAC": 48, "SHO": 18, "PAS": 52, "DRI": 38, "DEF": 22, "PHY": 80,
         "Position": "GK", "League": "Liga F", "Team": "Testinas", "Nation": "Spain",
         "Age": 28, "gender": "F"},
    ])
