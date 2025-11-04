import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from util.util_recuperation_data import determiner_l_index_des_data_manquantes, recuperer_moyenne_data_par_an, \
    colonnes_defaut

c = [
    'PRECIPITATION', 'MAX_TEMP', 'MIN_TEMP', 'AVG_WIND_SPEED',
    'TEMP_RANGE', 'WIND_TEMP_RATIO', 'LAGGED_PRECIPITATION', 'LAGGED_AVG_WIND_SPEED'
]
def affichage_de_chaque_donnees_en_fonction_de_la_date(data: pd.DataFrame) -> None:
    for col in data.columns:
        # Trace chaque type de donnée en fonction du jour de l'année
        if col == 'DAY_OF_YEAR':
            continue
        sns.scatterplot(data=data, x='DAY_OF_YEAR', y=data[col])
        plt.xlabel('DAY_OF_YEAR')
        plt.ylabel(col)
        plt.title(f'Évolution de {col} en fonction de la date')
        plt.show()


def affichage_pair_plot_en_fonction_de_la_date(data: pd.DataFrame) -> None:
    determiner_l_index_des_data_manquantes(data=data)
    # Exemple d'affichage pairplot en fonction de la date
    # sns.pairplot(data[["DATE", 'PRECIPITATION', 'MAX_TEMP', 'MIN_TEMP', 'AVG_WIND_SPEED']], hue='DATE')
    sns.pairplot(data[['AVG_WIND_SPEED', 'WIND_TEMP_RATIO', 'MAX_TEMP', 'MIN_TEMP', 'DATE']], hue='DATE')
    plt.show()

def affichage_data(data: pd.DataFrame) -> None:
    print(colonnes_defaut)
    type_data = input(" Choisir un type de donnée à afficher : ")
    moy =recuperer_moyenne_data_par_an(data=data, type_data=type_data)
    df = data.merge(moy, on='DAY_OF_YEAR', how='left')
    plt.figure(figsize = (12,6))
    sns.histplot(df ,x=colonnes_defaut)
    plt.show()

