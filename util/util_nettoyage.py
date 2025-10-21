
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def nettoyage_csv(data):
    print("il manque\n", data.isna().sum(), "\n\n")  # affiche le nombre de valeurs manquantes
    sns.heatmap(data.isnull(), cbar=False)

    # plt.title("Valeurs manquantes")
    # plt.show() #plot un schema qui montre les donnes manquante pour chaque colonnes

    print(data.duplicated().sum()) #donne les valeurs duppliquées
    data=data.drop_duplicates() #supprime les valeurs duppliquées


def affichage_pair_plot_en_fonction_de_la_date(data):
    determiner_l_index_des_data_manquantes(data=data)
    # sns.pairplot(data[["DATE",'PRECIPITATION','MAX_TEMP','MIN_TEMP','AVG_WIND_SPEED','FIRE_START_DAY','YEAR','TEMP_RANGE','WIND_TEMP_RATIO','MONTH','SEASON','LAGGED_PRECIPITATION','LAGGED_AVG_WIND_SPEED','DAY_OF_YEAR']],hue='DAY_OF_YEAR')
    sns.pairplot(data[['AVG_WIND_SPEED', 'WIND_TEMP_RATIO', 'MAX_TEMP', 'MIN_TEMP', 'DATE']], hue='DATE')
    plt.show()

def affichage_de_chaque_donnees_en_fonction_de_la_date(data):
    for col in data.columns:
        # on trace chaque type de données en fonction de du jour de l'année
        sns.scatterplot(data=data, x='DAY_OF_YEAR', y=data[col])
        plt.xlabel('DAY_OF_YEAR')
        plt.ylabel(col)
        plt.title(f'Évolution de {col} en fonction de la date')
        plt.show()

def determiner_l_index_des_data_manquantes(data):
    for index, row in data.iterrows() :
        if row.isna().any() :
            print(row['DATE'])

def determiner_val_abberante(data):
    data['DAY_OF_YEAR'] = pd.to_datetime(data['DATE']).dt.dayofyear  # convertit  la colonne date en day of year

    # liste des colonnes
    colonnes_a_moyenner = [
        'PRECIPITATION',
        'MAX_TEMP',
        'MIN_TEMP',
        'AVG_WIND_SPEED',
        'TEMP_RANGE',
        'WIND_TEMP_RATIO',
        'LAGGED_PRECIPITATION',
        'LAGGED_AVG_WIND_SPEED'
    ]

    # on regroupe les valeurs du df pour day of year avec les colonnes que l'on veut et on calcule la valeur moyenne
    moyennes_par_jour = data.groupby('DAY_OF_YEAR')[colonnes_a_moyenner].mean().reset_index()

    # on affiche les moyennes
    print(moyennes_par_jour.head())






