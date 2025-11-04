import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

#pas besoin de travailler sur d'autre colonnes de data
colonnes_defaut = [
    'PRECIPITATION', 'MAX_TEMP', 'MIN_TEMP', 'AVG_WIND_SPEED',
    'TEMP_RANGE', 'WIND_TEMP_RATIO', 'LAGGED_PRECIPITATION', 'LAGGED_AVG_WIND_SPEED'
]

def recuperer_moyenne_data_par_an(data, type_data):

    if 'DAY_OF_YEAR' not in data.columns:
        data = data.copy()
        data['DATE'] = pd.to_datetime(data['DATE'])
        data['DAY_OF_YEAR'] = data['DATE'].dt.dayofyear
        if type_data in colonnes_defaut:
            moy, colonnes =moyenne_par_data(data=data,
                                 colonnes=type_data )
        return moy



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

    #juste pour s'assurer que 'DAY_OF_YEAR' est disponible
    if 'DAY_OF_YEAR' not in data.columns:
        data = data.copy()
        data['DATE'] = pd.to_datetime(data['DATE'])
        data['DAY_OF_YEAR'] = data['DATE'].dt.dayofyear

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
    #Moyenne par jour de l'année sur tout l'historique
    moy = data.groupby('DAY_OF_YEAR')[colonnes].mean().reset_index()
    moy = moy.rename(columns={c: f"{c}_mean" for c in colonnes})
    return moy, colonnes

