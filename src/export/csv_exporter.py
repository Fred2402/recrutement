"""Export de la sélection courante en CSV — pour la transmettre telle
quelle au directeur sportif.
"""

import pandas as pd

from src.config import COLONNES_TABLE


def export_selection_to_csv(sel: pd.DataFrame) -> str:
    """Retourne le contenu CSV (str) de la sélection, prêt pour st.download_button."""
    return sel.sort_values("OVR", ascending=False)[COLONNES_TABLE].to_csv(index=False)
