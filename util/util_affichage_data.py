import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
<<<<<<< HEAD
import numpy as np

from matplotlib.colors import PowerNorm
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (nécessaire pour activer le 3D)
=======
import plotly.express as px
import plotly.io as io
io.renderers.default='browser'
>>>>>>> c64621eee549a2da20ea39e28dec91bad95a0dc1

from util.util_recuperation_data import (
    determiner_l_index_des_data_manquantes,
    colonnes_defaut,
    assurer_colonnes_temporelles,
)

c = [
    'PRECIPITATION', 'MAX_TEMP', 'MIN_TEMP', 'AVG_WIND_SPEED',
    'TEMP_RANGE', 'WIND_TEMP_RATIO', 'LAGGED_PRECIPITATION', 'LAGGED_AVG_WIND_SPEED'
]


def affichage_de_chaque_donnees_en_fonction_de_la_date(data: pd.DataFrame) -> None:
    df = assurer_colonnes_temporelles(data, besoin=("DAY_OF_YEAR",))
    for col in df.columns:
        # Trace chaque type de donnee en fonction du jour de l'annee
        if col == 'DAY_OF_YEAR':
            continue
        sns.scatterplot(data=df, x='DAY_OF_YEAR', y=df[col])
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
    df = assurer_colonnes_temporelles(data, besoin=("DATE", "DAY_OF_YEAR"))
    type_dispo = [col_data for col_data in colonnes_defaut if col_data in df.columns]
    print("Colonnes disponibles:", type_dispo)

    type_data = input("Choisir un type de donnee a afficher : ").strip().upper()
    if type_data not in type_dispo:
        print(f"Type inconnu: {type_data}. Choisissez parmi: {type_dispo}")
        return

    plt.figure(figsize=(12, 6))
    sns.scatterplot(data=df, x='DAY_OF_YEAR', y=type_data, s=10, alpha=0.5)
    plt.xlabel('DAY_OF_YEAR')
    plt.ylabel(type_data)
    plt.title(f"Evolution de {type_data} en fonction du jour de l'annee")
    plt.show()
    
    
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
    sns.heatmap(heatmap_data,annot=True)
    plt.title("Températures moyennes par mois et par année", fontsize=14)
    plt.xlabel("Mois")
    plt.ylabel("Année")
    plt.show()
    
    
def valeurs_aberantes(data) :
    for col in data.columns : 
        fig = px.box(data,y=col)
        fig.show()
        print(col,'maximale et minimale : ',data[col].max(), ', ',data[col].min())
        


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
    white_at = 2 # ≥ ce nombre = blanc (saturation)
    use_pow = False
    gamma = 0.8  # courbe du dégradé si use_pow=True (plus petit = plus vite clair)

    # S'assure que YEAR et DAY_OF_YEAR sont présents (et DATE typée)
    df = assurer_colonnes_temporelles(data, besoin=("YEAR", "DAY_OF_YEAR", "DATE"))

    # nb d'incendies par (année, jour)
    heat = (df.groupby(['YEAR', 'DAY_OF_YEAR'])['FIRE_START_DAY']
            .sum()
            .unstack(fill_value=0))

    # jours a à 366 jours (bissextile inclus)
    all_days = pd.RangeIndex(1, 367)
    heat = heat.reindex(columns=all_days, fill_value=0)

    # saturer pour que blanc = white_at
    heat = heat.clip(upper=white_at)

    plt.style.use('dark_background')
    plt.figure(figsize=(16, 7))

    norm = PowerNorm(gamma=gamma, vmin=0, vmax=white_at) if use_pow else None

    ax = sns.heatmap(
        heat.sort_index(),  # années croissantes
        cmap='gray',  # noir -> blanc
        vmin=0, vmax=white_at,  # blanc atteint à white_at
        norm=norm,  # optionnel (non linéaire)
        cbar=True,
        cbar_kws={'label': f'Incendies/jour (saturé à {white_at})'},
        linewidths=0
    )

    ax.set_xlabel("Jour de l'année")
    ax.set_ylabel("Année")
    ax.set_title("Incendies par jour et par année (plus clair = plus d’incendies)")
    plt.tight_layout()
    plt.show()

def graph_temperature_comparaison_annees_juin_septembre(data: pd.DataFrame, farenite_en_degre=False) -> None:
    # Assure YEAR/MONTH si DATE existe
    df = assurer_colonnes_temporelles(data, besoin=("YEAR", "MONTH", "DATE"))
    if 'YEAR' not in df.columns or 'MONTH' not in df.columns:
        raise ValueError("Il faut soit une colonne DATE, soit YEAR et MONTH dans le DataFrame.")

    # --- Températures ---
    if not {'MAX_TEMP', 'MIN_TEMP'}.issubset(df.columns):
        raise ValueError("Colonnes requises: MAX_TEMP et MIN_TEMP")

    if farenite_en_degre:
        df['MAX_TEMP'] = (df['MAX_TEMP'] - 32) * 5 / 9
        df['MIN_TEMP'] = (df['MIN_TEMP'] - 32) * 5 / 9

    df['AVG_TEMP'] = (df['MAX_TEMP'] + df['MIN_TEMP']) / 2.0

    # --- Filtre été : Juin→Septembre ---
    df = df[df['MONTH'].between(6, 9)]

    # --- Moyenne annuelle (été) ---
    yearly_avg = df.groupby('YEAR')['AVG_TEMP'].mean().sort_index()

    years = yearly_avg.index.values
    if years.size < 2:
        raise ValueError("Pas assez d'années pour tracer une tendance.")

    # --- Séparation 20 premières / 20 dernières ---
    n = 20
    if years.size < 2 * n:
        # Fallback si moins de 40 années
        n = years.size // 2
        if n == 0:
            raise ValueError("Pas assez d'années pour comparer deux périodes.")

    first_years = years[:n]
    last_years = years[-n:]

    y_first = yearly_avg.loc[first_years].values
    y_last = yearly_avg.loc[last_years].values

    # slope en °C par an (ou °/an si Fahrenheit non converti)
    m1, b1 = np.polyfit(first_years, y_first, 1)
    m2, b2 = np.polyfit(last_years, y_last, 1)

    # --- Tracé ---
    plt.figure(figsize=(12, 6))

    # Période 1 (20 premières)
    plt.plot(first_years, y_first, marker='o', linestyle='-', label='20 premières années')
    plt.plot(first_years, m1 * first_years + b1, linestyle='--', label=f"Régression 1 (pente {m1:.3f}/an)")

    # Période 2 (20 dernières)
    plt.plot(last_years, y_last, marker='o', linestyle='-', label='20 dernières années')
    plt.plot(last_years, m2 * last_years + b2, linestyle='--', label=f"Régression 2 (pente {m2:.3f}/an)")

    plt.title("Température moyenne (juin→septembre)\nComparaison 20 premières vs 20 dernières années")
    plt.xlabel("Année")
    plt.ylabel("Température moyenne")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # --- Impressions utiles ---
    print(f"Période 1 (20 premières) : pente = {m1:.4f} par an  (~{m1 * 10:.3f} par décennie)")
    print(f"Période 2 (20 dernières) : pente = {m2:.4f} par an  (~{m2 * 10:.3f} par décennie)")

def comparer_laugmentation_des_departs_de_feu_sur_les_20_premieres_et_20_dernieres_annees(data):
    df = assurer_colonnes_temporelles(data, besoin=("YEAR", "MONTH", "DATE"))
    df['FIRE_START_DAY'] = df['FIRE_START_DAY'].astype(int)

    fires_year = df.groupby("YEAR")['FIRE_START_DAY'].sum()
    years = fires_year.index.sort_values()
    n = 20 if len(years) >= 40 else len(years) // 2

    first = years[:n]
    last = years[-n:]

    fy1 = fires_year.loc[first]
    fy2 = fires_year.loc[last]

    fires_month = df.groupby(["YEAR", "MONTH"])['FIRE_START_DAY'].sum()
    top_month_each_year = fires_month.groupby(level=0).idxmax()

    for yr, (_, mo) in top_month_each_year.items():
        print(f"{yr}: mois {mo}")

    plt.figure(figsize=(10, 5))
    plt.bar(fy1.index, fy1.values, alpha=0.6, label="20 premières années")
    plt.bar(fy2.index, fy2.values, alpha=0.6, label="20 dernières années")
    plt.title("Nombre d'incendies par an (20 premières vs 20 dernières années)")
    plt.xlabel("Année")
    plt.ylabel("Nombre d'incendies")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

# --- Graphiques d'interprétation supplémentaires ---

def profil_saisonnier_incendies(data: pd.DataFrame, fenetre_lissage: int = 7) -> None:
    """
    Profil saisonnier: probabilité moyenne d'incendie par jour de l'année,
    lissée sur 'fenetre_lissage' jours.
    """
    df = assurer_colonnes_temporelles(data, besoin=("DAY_OF_YEAR",))
    s = df.groupby('DAY_OF_YEAR')['FIRE_START_DAY'].mean().sort_index()
    if fenetre_lissage and fenetre_lissage > 1:
        s = s.rolling(fenetre_lissage, min_periods=1, center=True).mean()

    plt.figure(figsize=(12, 4))
    plt.plot(s.index, s.values, color='firebrick')
    plt.title("Profil saisonnier des départs d'incendie (moyenne, lissé)")
    plt.xlabel("Jour de l'année")
    plt.ylabel("Taux d'incendie moyen")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()



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

# Rtro-compatibilit : alias pour l'ancien nom appel depuis main.py
def graph_3d_temperature_comparaison_annes_jui_septembre(data: pd.DataFrame, farenite_en_degre=False) -> None:
    return graph_temperature_comparaison_annees_juin_septembre(data, farenite_en_degre)
