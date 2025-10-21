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


def affichage_pair_plot_en_fonction_de_la_date(data: pd.DataFrame) -> None:
    determiner_l_index_des_data_manquantes(data=data)
    # Exemple d'affichage pairplot en fonction de la date
    # sns.pairplot(data[["DATE", 'PRECIPITATION', 'MAX_TEMP', 'MIN_TEMP', 'AVG_WIND_SPEED']], hue='DATE')
    sns.pairplot(data[['AVG_WIND_SPEED', 'WIND_TEMP_RATIO', 'MAX_TEMP', 'MIN_TEMP', 'DATE']], hue='DATE')
    plt.show()


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


def determiner_l_index_des_data_manquantes(data: pd.DataFrame) -> None:
    for _, row in data.iterrows():
        if row.isna().any():
            print(row.get('DATE', 'DATE_INCONNUE'))


def determiner_val_abberante(data: pd.DataFrame, colonnes=None) -> pd.DataFrame:
    """
    Version simplifiée demandée:
    - Calcule la moyenne par jour de l'année (toutes années confondues)
    - Marque "aberrant" si valeur > 2 * moyenne_du_jour
    - Affiche un petit résumé par année
    """

    # 1) S'assurer que 'DAY_OF_YEAR' est disponible
    if 'DAY_OF_YEAR' not in data.columns:
        data = data.copy()
        data['DATE'] = pd.to_datetime(data['DATE'])
        data['DAY_OF_YEAR'] = data['DATE'].dt.dayofyear

    # 2) Colonnes numériques à analyser (filtrées sur celles présentes)
    colonnes_defaut = [
        'PRECIPITATION', 'MAX_TEMP', 'MIN_TEMP', 'AVG_WIND_SPEED',
        'TEMP_RANGE', 'WIND_TEMP_RATIO', 'LAGGED_PRECIPITATION', 'LAGGED_AVG_WIND_SPEED'
    ]
    if colonnes is None:
        colonnes = [c for c in colonnes_defaut if c in data.columns]
    else:
        colonnes = [c for c in colonnes if c in data.columns]
    if not colonnes:
        print("Aucune colonne à analyser trouvée.")
        return data

    #Moyenne par jour de l'année sur tout l'historique
    moy = data.groupby('DAY_OF_YEAR')[colonnes].mean().reset_index()
    moy = moy.rename(columns={c: f"{c}_mean" for c in colonnes})

    #Rattache la moyenne du jour à chaque ligne
    df = data.merge(moy, on='DAY_OF_YEAR', how='left')

    #Calcul et determination des abberations si la valeur lue > 2 * moyenne_du_jour
    for col in colonnes:
        df[f'ABERRANT_{col}'] = df[col] > 2 * df[f'{col}_mean']

    #Résumé léger qui boucle sur chaque année (si la colonne YEAR existe) (voir si util)
    if 'YEAR' in df.columns:
        for an in sorted(df['YEAR'].dropna().unique()):
            sous = df[df['YEAR'] == an]
            resume = ", ".join(
                f"{c}:{int(sous[f'ABERRANT_{c}'].sum())}" for c in colonnes
            )
            print(f"Année {int(an)} | {resume}")
    else:
        resume = ", ".join(f"{c}:{int(df[f'ABERRANT_{c}'].sum())}" for c in colonnes)
        print(f"Total | {resume}")

    return df

