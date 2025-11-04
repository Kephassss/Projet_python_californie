import pandas as pd
from util.util_nettoyage import nettoyage_csv
from util.util_recuperation_data import determiner_l_index_des_data_manquantes, determiner_val_abberante
from util.util_affichage_data import affichage_histoplot,affichage_data,affichage_de_chaque_donnees_en_fonction_de_la_date


if __name__ == '__main__':
    data = pd.read_csv("C:/Users/pierr/Desktop/python/PythonProject1/CA_Weather_Fire_Dataset_1984-2025.csv")  # charge le csv
    print(data.info, "\n\n")  # affiche les infos du csv
    nettoyage_csv(data) #lancement du programme de nettoyage présent dans un dossier annexe
    #determiner_l_index_des_data_manquantes(data)
    # affichage_pair_plot_en_fonction_de_la_date
    val_aberrante=determiner_val_abberante(data)
    # affichage_data(data)
    affichage_histoplot(data)

    # affichage_de_chaque_donnees_en_fonction_de_la_date(data)