import pandas as pd
from util.util_nettoyage import nettoyage_csv
<<<<<<< HEAD

from util.util_recuperation_data import (determiner_l_index_des_data_manquantes,
                                         determiner_val_abberante)

from util.util_affichage_data import (
    comparer_laugmentation_des_departs_de_feu_sur_les_20_premieres_et_20_dernieres_annees,
    graph_temperature_comparaison_annees_juin_septembre,
    afficher_jour_depart_incendie,
    affichage_data,
    affichage_de_chaque_donnees_en_fonction_de_la_date,
    profil_saisonnier_incendies,
)
=======
from util.util_recuperation_data import determiner_l_index_des_data_manquantes, determiner_val_abberante
from util.util_affichage_data import  valeurs_aberantes,heatmap_temp_moy_en_fonction_jour_et_an,affichage_data,affichage_de_chaque_donnees_en_fonction_de_la_date,affichage_pair_plot_en_fonction_de_la_date
>>>>>>> c64621eee549a2da20ea39e28dec91bad95a0dc1


if __name__ == '__main__':
    data = pd.read_csv("U:/2ème_année/python1311/Projet_python_californie/CA_Weather_Fire_Dataset_1984-2025.csv")  # charge le csv
    print(data.info, "\n\n")  # affiche les infos du csv
    #nettoyage_csv(data) #lancement du programme de nettoyage présent dans un dossier annexe
    
    #determiner_l_index_des_data_manquantes(data)
<<<<<<< HEAD
    # affichage_pair_plot_en_fonction_de_la_date
    # val_aberrante=determiner_val_abberante(data)
    # affichage_data(data)
    graph_temperature_comparaison_annees_juin_septembre(data)
    # affichage_de_chaque_donnees_en_fonction_de_la_date(data)
    comparer_laugmentation_des_departs_de_feu_sur_les_20_premieres_et_20_dernieres_annees(data)

    # Nouveaux graphiques d'interprétation
    profil_saisonnier_incendies(data)



















    # ██████╗ ██████╗ ███╗   ███╗██████╗ ███████╗██████╗ ██╗███╗   ██╗██╗    ███╗   ███╗ █████╗ ██████╗  ██████╗ ██████╗
    # ██╔════╝██╔═══██╗████╗ ████║██╔══██╗██╔════╝██╔══██╗██║████╗  ██║██║    ████╗ ████║██╔══██╗██╔══██╗██╔════╝██╔═══██╗
    # ██║     ██║   ██║██╔████╔██║██████╔╝█████╗  ██████╔╝██║██╔██╗ ██║██║    ██╔████╔██║███████║██████╔╝██║     ██║   ██║
    # ██║     ██║   ██║██║╚██╔╝██║██╔═══╝ ██╔══╝  ██╔══██╗██║██║╚██╗██║██║    ██║╚██╔╝██║██╔══██║██╔══██╗██║     ██║   ██║
    # ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║     ███████╗██║  ██║██║██║ ╚████║██║    ██║ ╚═╝ ██║██║  ██║██║  ██║╚██████╗╚██████╔╝
    # ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚═╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝
=======

    #val_aberrante=determiner_val_abberante(data)
    
    #affichage_data(data)
    
    heatmap_temp_moy_en_fonction_jour_et_an(data)
    
    #affichage_de_chaque_donnees_en_fonction_de_la_date(data)
    
    #affichage_histoplot(data)
    
    #affichage_pair_plot_en_fonction_de_la_date(data)
    
    #affichage_de_chaque_donnees_en_fonction_de_la_date(data)
    
    valeurs_aberantes(data)
>>>>>>> c64621eee549a2da20ea39e28dec91bad95a0dc1
