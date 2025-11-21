import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def nettoyage_csv(data: pd.DataFrame) -> None:
    print("il manque\n", data.isna().sum(), "\n\n")  # affiche le nombre de valeurs manquantes
    sns.heatmap(data.isnull(), cbar=False)
    # plt.title("Valeurs manquantes")
    # plt.show()  # affiche un schéma des valeurs manquantes par colonne

    print(data.duplicated().sum())  # nombre de doublons
    data.drop_duplicates(inplace=True)  # supprime les doublons

