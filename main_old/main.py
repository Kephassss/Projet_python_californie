import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, callback, Output, Input
from pathlib import Path

from util.util_nettoyage import nettoyage_csv
from util import util_dash
from util.util_recuperation_data import (
    determiner_l_index_des_data_manquantes,
    determiner_val_abberante,
)
from util.util_affichage_data import (
    comparer_laugmentation_des_departs_de_feu_sur_les_20_premieres_et_20_dernieres_annees,
    graph_temperature_comparaison_annees_juin_septembre,
    afficher_jour_depart_incendie,
    affichage_data,
    affichage_de_chaque_donnees_en_fonction_de_la_date,
    profil_saisonnier_incendies,
    heatmap_temp_moy_en_fonction_jour_et_an,
    valeurs_aberantes,
    heatmap_temp_moy_en_fonction_jour_et_an
)


LAUNCH_DASH = True  # Mettre False si vous ne voulez pas lancer le dashboard depuis main


if __name__ == '__main__':
    # Charge le CSV depuis le dossier du projet (chemin relatif)
    base_dir = Path(__file__).resolve().parent
    data_path = base_dir / "CA_Weather_Fire_Dataset_1984-2025.csv"
    data = pd.read_csv(data_path)
    # print(data.info, "\n\n")  # Affiche les infos du CSV

    # Nettoyage de base
    nettoyage_csv(data)

    # Outils d'analyse/affichage (decommenter ceux a utiliser)
    # determiner_l_index_des_data_manquantes(data)
    # val_aberrante = determiner_val_abberante(data)
    # affichage_data(data)
    # affichage_de_chaque_donnees_en_fonction_de_la_date(data)
    # graph_temperature_comparaison_annees_juin_septembre(data)
    # afficher_jour_depart_incendie(data)
    # comparer_laugmentation_des_departs_de_feu_sur_les_20_premieres_et_20_dernieres_annees(data)
    # profil_saisonnier_incendies(data)
    # valeurs_aberantes(data)
    # heatmap_temp_moy_en_fonction_jour_et_an(data)

    if LAUNCH_DASH:
        # Lance le tableau de bord Dash
        util_dash.run(debug=True)









    # ██████╗ ██████╗ ███╗   ███╗██████╗ ███████╗██████╗ ██╗███╗   ██╗██╗    ███╗   ███╗ █████╗ ██████╗  ██████╗ ██████╗
    # ██╔════╝██╔═══██╗████╗ ████║██╔══██╗██╔════╝██╔══██╗██║████╗  ██║██║    ████╗ ████║██╔══██╗██╔══██╗██╔════╝██╔═══██╗
    # ██║     ██║   ██║██╔████╔██║██████╔╝█████╗  ██████╔╝██║██╔██╗ ██║██║    ██╔████╔██║███████║██████╔╝██║     ██║   ██║
    # ██║     ██║   ██║██║╚██╔╝██║██╔═══╝ ██╔══╝  ██╔══██╗██║██║╚██╗██║██║    ██║╚██╔╝██║██╔══██║██╔══██╗██║     ██║   ██║
    # ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║     ███████╗██║  ██║██║██║ ╚████║██║    ██║ ╚═╝ ██║██║  ██║██║  ██║╚██████╗╚██████╔╝
    # ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚═╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝
