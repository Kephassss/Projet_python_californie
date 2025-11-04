import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from util.util_recuperation_data import (
    determiner_l_index_des_data_manquantes,
    colonnes_defaut,
)

c = [
    'PRECIPITATION', 'MAX_TEMP', 'MIN_TEMP', 'AVG_WIND_SPEED',
    'TEMP_RANGE', 'WIND_TEMP_RATIO', 'LAGGED_PRECIPITATION', 'LAGGED_AVG_WIND_SPEED'
]


def affichage_de_chaque_donnees_en_fonction_de_la_date(data: pd.DataFrame) -> None:
    for col in data.columns:
        # Trace chaque type de donnee en fonction du jour de l'annee
        if col == 'DAY_OF_YEAR':
            continue
        sns.scatterplot(data=data, x='DAY_OF_YEAR', y=data[col])
        plt.xlabel('DAY_OF_YEAR')
        plt.ylabel(col)
        plt.title(f"Evolution de {col} en fonction de la date")
        plt.show()


def affichage_pair_plot_en_fonction_de_la_date(data: pd.DataFrame) -> None:
    determiner_l_index_des_data_manquantes(data=data)
    # Exemple d'affichage pairplot en fonction de la date
    # sns.pairplot(data[["DATE", 'PRECIPITATION', 'MAX_TEMP', 'MIN_TEMP', 'AVG_WIND_SPEED']], hue='DATE')
    sns.pairplot(data[['AVG_WIND_SPEED', 'WIND_TEMP_RATIO', 'MAX_TEMP', 'MIN_TEMP', 'DATE']], hue='DATE')
    plt.show()


def affichage_data(data: pd.DataFrame) -> None:

    # Colonnes disponibles = type dispo ( temp max, wind, humidite etc)
    type_dispo = [col_data for col_data in colonnes_defaut if col_data in data.columns]
    print("Colonnes disponibles:", type_dispo)

    type_data = input("Choisir un type de donnee a afficher : ").strip().upper()
    if type_data not in type_dispo:
        print(f"Type inconnu: {type_data}. Choisissez parmi: {type_dispo}")
        return

    if 'DAY_OF_YEAR' not in data.columns:
        data = data.copy()
        data['DATE'] = pd.to_datetime(data['DATE'])
        data['DAY_OF_YEAR'] = data['DATE'].dt.dayofyear


    plt.figure(figsize=(12, 6))
    sns.scatterplot(data=data, x='DAY_OF_YEAR', y=type_data, s=10, alpha=0.5)
    plt.xlabel('DAY_OF_YEAR')
    plt.ylabel(type_data)
    plt.title(f"Evolution de {type_data} en fonction du jour de l'annee")
    plt.show()

# def affichage_histoplot(data: pd.DataFrame) -> None: on peut pas histoplot plusieurs valeurs ?
#     # Colonnes disponibles = type dispo ( temp max, wind, humidite etc)
#     type_dispo = [col_data for col_data in colonnes_defaut if col_data in data.columns]
#     print("Colonnes disponibles:", type_dispo)
#     list_type_histo=[]
#     choice ='oui'
#     while choice == 'oui':
#         type_data = input("Choisir un type de donnee a afficher : ").strip().upper()
#         list_type_histo.append(type_data)
#         choice = input('choisir un autre type ? oui/non : ')
#
#     if any(t not in type_dispo for t in list_type_histo):
#         print(f"Type inconnu dans la liste: {list_type_histo}. Choisissez parmi: {type_dispo}")
#         return
#
#     if 'DAY_OF_YEAR' not in data.columns:
#         data = data.copy()
#         data['DATE'] = pd.to_datetime(data['DATE'])
#         data['DAY_OF_YEAR'] = data['DATE'].dt.dayofyear
#
#
#     plt.figure(figsize=(12, 6))
#     sns.histplot(data=data, x='DAY_OF_YEAR', y=list_type_histo, s=10, alpha=0.5)
#     plt.xlabel('DAY_OF_YEAR')
#     plt.title(f"Evolution de {list_type_histo} en fonction du jour de l'annee")
#     plt.show()


def afficher_jour_depart_incendie(data: pd.DataFrame) -> None:
    encours
