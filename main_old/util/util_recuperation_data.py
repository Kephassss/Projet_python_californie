import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

#pas besoin de travailler sur d'autre colonnes de data
colonnes_defaut = [
    'PRECIPITATION', 'MAX_TEMP', 'MIN_TEMP', 'AVG_WIND_SPEED',
    'TEMP_RANGE', 'WIND_TEMP_RATIO', 'LAGGED_PRECIPITATION', 'LAGGED_AVG_WIND_SPEED'
]

def recuperer_moyenned_un_type_au_choix_data_par_an(data, type_data):
    df = assurer_colonnes_temporelles(data, besoin=("DATE", "DAY_OF_YEAR"))
    if type_data in colonnes_defaut:
        moy, colonnes = moyenne_par_data(data=df, colonnes=type_data)
        return moy
    # Si type non supporté, retourner None pour conserver le comportement actuel implicite
    return None



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

    # S'assurer que 'DAY_OF_YEAR' est disponible
    data = assurer_colonnes_temporelles(data, besoin=("DAY_OF_YEAR",))

    #fonction en dessous pour recuperer la moyenne de la colonne en question par data
    moy, colonnes = moyenne_par_data(data)

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

def moyenne_par_data(data, colonnes=None) -> pd.DataFrame:
    # Colonnes numériques à analyser (filtrées sur celles présentes)

    if colonnes is None:
        colonnes = [c for c in colonnes_defaut if c in data.columns]
    else:
        colonnes = [c for c in colonnes if c in data.columns]
    if not colonnes:
        print("Aucune colonne à analyser trouvée.")
        return data
    # S'assure que DAY_OF_YEAR est disponible pour le groupby
    data = assurer_colonnes_temporelles(data, besoin=("DAY_OF_YEAR",))
    # Moyenne par jour de l'année sur tout l'historique
    moy = data.groupby('DAY_OF_YEAR')[colonnes].mean().reset_index()
    moy = moy.rename(columns={c: f"{c}_mean" for c in colonnes})
    return moy, colonnes


def assurer_colonnes_temporelles(
    data: pd.DataFrame,
    besoin=("YEAR", "MONTH", "DAY_OF_YEAR"),
    copy: bool = True,
) -> pd.DataFrame:
    """
    Garantit la présence et le bon typage des colonnes temporelles courantes.
    pas rééllement util car notre dataset ne bouge pas mais la fonction est intéressante pour appliquer le cours

    - Si "DATE" existe, elle est convertie en datetime si nécessaire.
    - Ajoute "YEAR" / "MONTH" / "DAY_OF_YEAR" si demandées et déductibles depuis DATE.

    Paramètres:
      - data: DataFrame source (non modifié si copy=True)
      - besoin: itérable des colonnes temporelles à garantir
                (par ex. ("YEAR", "DAY_OF_YEAR"))
      - copy: renvoyer une copie (True) ou modifier en place (False)

    Retour:
      - DataFrame contenant les colonnes temporelles demandées lorsque possible.
    """
    df = data.copy() if copy else data

    # Normaliser l'entrée besoin en set de chaînes
    besoin_set = set(map(str, besoin))

    # Convertir DATE en datetime si présente
    if 'DATE' in df.columns:
        if not pd.api.types.is_datetime64_any_dtype(df['DATE']):
            df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')

    # YEAR
    if 'YEAR' in besoin_set and 'YEAR' not in df.columns and 'DATE' in df.columns:
        df['YEAR'] = df['DATE'].dt.year

    # MONTH
    if 'MONTH' in besoin_set and 'MONTH' not in df.columns and 'DATE' in df.columns:
        df['MONTH'] = df['DATE'].dt.month

    # DAY_OF_YEAR
    if 'DAY_OF_YEAR' in besoin_set and 'DAY_OF_YEAR' not in df.columns and 'DATE' in df.columns:
        df['DAY_OF_YEAR'] = df['DATE'].dt.dayofyear

    return df

def heatmap_temp_moy_en_fonction_jour_et_an(data: pd.DataFrame):
    # Vérifie l'existence de la colonne de température moyenne
    if "AVG_TEMP" not in data.columns:
        data["AVG_TEMP"] = (data["MAX_TEMP"] + data["MIN_TEMP"]) / 2
    else:
        raise ValueError("Aucune colonne AVG_TEMP")

    # Pivot: Années en lignes, Mois en colonnes
    heatmap_data = data.pivot_table(index="YEAR",columns="MONTH",values="AVG_TEMP")

    # Affichage heatmap
    plt.figure(figsize=(14, 8))
    sns.heatmap(heatmap_data,cmap="coolwarm",  linewidths=.5,linecolor='gray',annot=False)
    plt.title("Températures moyennes par mois et par année", fontsize=14)
    plt.xlabel("Mois")
    plt.ylabel("Année")
    plt.show()

