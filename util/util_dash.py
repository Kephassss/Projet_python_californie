import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pathlib import Path
from datetime import date

try:
    from util.util_recuperation_data import (
        colonnes_defaut,
        assurer_colonnes_temporelles,
    )
except Exception:
    from util_recuperation_data import (
        colonnes_defaut,
        assurer_colonnes_temporelles,
    )

# ---------- Data Loading ----------
project_root = Path(__file__).resolve().parent.parent
data_path = project_root / "CA_Weather_Fire_Dataset_1984-2025.csv"
df = pd.read_csv(data_path, parse_dates=["DATE"]) if data_path.exists() else pd.DataFrame()

if not df.empty:
    df = assurer_colonnes_temporelles(df, besoin=("YEAR", "MONTH", "DAY_OF_YEAR", "DATE"), copy=True)
    # Normalize FIRE_START_DAY to boolean
    if df.get("FIRE_START_DAY") is not None and df["FIRE_START_DAY"].dtype != bool:
        df["FIRE_START_DAY"] = (
            df["FIRE_START_DAY"].astype(str).str.lower().map({"true": True, "false": False})
        ).fillna(False)

available_vars = [c for c in colonnes_defaut if c in df.columns] if not df.empty else []

# ---------- App Initialization ----------
app = dash.Dash(
    __name__,
    title="California Wildfires Monitor",
    external_stylesheets=[dbc.themes.CYBORG],  # Dark theme base
    assets_folder=str(project_root / "assets"),
)
server = app.server

# ---------- Plotly Template ----------
def fire_template(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",  # Transparent to let card bg show
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e0e0e0", family="Roboto"),
        margin=dict(l=40, r=20, t=40, b=40),
        hoverlabel=dict(bgcolor="#333", font_size=14),
        title_font=dict(size=18, color="#fd7e14"),
    )
    return fig

# ---------- Layout Components ----------

sidebar = html.Div(
    className="control-panel",
    children=[
        html.H4("Contrôles", className="text-white mb-4"),
        
        html.Label("Période d'analyse", className="control-label"),
        dcc.DatePickerRange(
            id="date-picker",
            min_date_allowed=df["DATE"].min() if not df.empty else date(1984, 1, 1),
            max_date_allowed=df["DATE"].max() if not df.empty else date(2025, 12, 31),
            start_date=date(2000, 1, 1),
            end_date=date(2020, 12, 31),
            display_format='DD/MM/YYYY',
            className="mb-3",
            style={"width": "100%"}
        ),

        html.Label("Filtre Saisonnier", className="control-label"),
        dcc.Dropdown(
            id="season-filter",
            options=[
                {"label": "Toute l'année", "value": "all"},
                {"label": "Saison des feux (Juin-Sept)", "value": "fire_season"},
                {"label": "Hiver (Déc-Fév)", "value": "winter"},
            ],
            value="all",
            clearable=False,
            className="mb-3 text-dark"
        ),

        html.Label("Variables Météo", className="control-label"),
        dcc.Dropdown(
            id="var-select",
            options=[{"label": v.replace("_", " "), "value": v} for v in available_vars],
            value=available_vars[:2] if available_vars else [],
            multi=True,
            placeholder="Sélectionner...",
            className="mb-3 text-dark"
        ),

        html.Label("Unité Température", className="control-label"),
        dbc.RadioItems(
            id="unit",
            options=[
                {"label": "Fahrenheit (°F)", "value": "F"},
                {"label": "Celsius (°C)", "value": "C"},
            ],
            value="F",
            inline=True,
            className="mb-4"
        ),
        
        html.Hr(className="border-secondary"),
        html.Small("Ajustez les filtres pour mettre à jour les graphiques en temps réel.", className="text-muted")
    ],
)

kpi_row = dbc.Row(
    [
        dbc.Col(dbc.Card([
            html.Div(id="kpi-fires", className="kpi-value"),
            html.Div("Total Incendies", className="kpi-label")
        ], className="kpi-card"), width=12, sm=6, lg=3),
        
        dbc.Col(dbc.Card([
            html.Div(id="kpi-temp", className="kpi-value"),
            html.Div("Temp. Max Moyenne", className="kpi-label")
        ], className="kpi-card"), width=12, sm=6, lg=3),
        
        dbc.Col(dbc.Card([
            html.Div(id="kpi-wind", className="kpi-value"),
            html.Div("Vent Moyen", className="kpi-label")
        ], className="kpi-card"), width=12, sm=6, lg=3),
        
        dbc.Col(dbc.Card([
            html.Div(id="kpi-days", className="kpi-value"),
            html.Div("Jours Analysés", className="kpi-label")
        ], className="kpi-card"), width=12, sm=6, lg=3),
    ],
    className="mb-4"
)

content = html.Div(
    [
        html.Div(
            [
                html.H1("Incendies en Californie", className="app-title"),
                html.P("Analyse climatique et historique des feux de forêt", className="app-subtitle"),
            ],
            className="app-header mb-4"
        ),
        
        dbc.Container(
            [
                kpi_row,
                
                dbc.Tabs(
                    [
                        dbc.Tab(label="Vue d'ensemble", tab_id="tab-overview"),
                        dbc.Tab(label="Analyse Temporelle", tab_id="tab-time"),
                        dbc.Tab(label="Corrélations", tab_id="tab-corr"),
                        dbc.Tab(label="Carte", tab_id="tab-map"),
                    ],
                    id="tabs",
                    active_tab="tab-overview",
                    className="mb-4"
                ),
                
                html.Div(id="tab-content")
            ],
            fluid=True
        )
    ]
)

app.layout = dbc.Container(
    dbc.Row(
        [
            dbc.Col(sidebar, width=12, lg=3, className="p-0"),
            dbc.Col(content, width=12, lg=9, className="p-0"),
        ],
        className="g-0" # No gutter
    ),
    fluid=True,
    className="p-0"
)


# ---------- Helpers ----------
def filter_data(start_date, end_date, season_filter):
    if df.empty: return df
    
    mask = (df["DATE"] >= pd.to_datetime(start_date)) & (df["DATE"] <= pd.to_datetime(end_date))
    dff = df.loc[mask].copy()
    
    if season_filter == "fire_season":
        dff = dff[dff["MONTH"].between(6, 9)]
    elif season_filter == "winter":
        dff = dff[dff["MONTH"].isin([12, 1, 2])]
        
    return dff

def convert_units(dff, unit):
    if unit == "C":
        for col in ["MAX_TEMP", "MIN_TEMP", "AVG_TEMP"]:
            if col in dff.columns:
                dff[col] = (dff[col] - 32) * 5/9
    return dff

# ---------- Callbacks ----------

@app.callback(
    [Output("kpi-fires", "children"),
     Output("kpi-temp", "children"),
     Output("kpi-wind", "children"),
     Output("kpi-days", "children")],
    [Input("date-picker", "start_date"),
     Input("date-picker", "end_date"),
     Input("season-filter", "value"),
     Input("unit", "value")]
)
def update_kpis(start, end, season, unit):
    if not start or not end or df.empty:
        return "0", "0", "0", "0"
        
    dff = filter_data(start, end, season)
    dff = convert_units(dff, unit)
    
    total_fires = dff["FIRE_START_DAY"].sum()
    avg_temp = dff["MAX_TEMP"].mean()
    avg_wind = dff["AVG_WIND_SPEED"].mean()
    days = len(dff)
    
    unit_label = "°C" if unit == "C" else "°F"
    
    return (
        f"{int(total_fires):,}",
        f"{avg_temp:.1f}{unit_label}",
        f"{avg_wind:.1f} mph",
        f"{days:,}"
    )

@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"),
     Input("date-picker", "start_date"),
     Input("date-picker", "end_date"),
     Input("season-filter", "value"),
     Input("var-select", "value"),
     Input("unit", "value")]
)
def render_tab_content(active_tab, start, end, season, vars_selected, unit):
    if df.empty:
        return html.Div("Aucune donnée disponible.")
        
    dff = filter_data(start, end, season)
    dff = convert_units(dff, unit)
    
    if active_tab == "tab-overview":
        # 1. Fire Heatmap (Year x Month)
        fires_pivot = dff.pivot_table(
            index="YEAR", columns="MONTH", values="FIRE_START_DAY", aggfunc="sum", fill_value=0
        )
        fig_heat = go.Figure(data=go.Heatmap(
            z=fires_pivot.values,
            x=fires_pivot.columns,
            y=fires_pivot.index,
            colorscale="YlOrRd",
            colorbar=dict(title="Feux")
        ))
        fig_heat.update_layout(title="Intensité des Incendies (Année vs Mois)")
        fire_template(fig_heat)
        
        # 2. Seasonality Line
        season_series = dff.groupby("DAY_OF_YEAR")["FIRE_START_DAY"].mean().rolling(7, center=True).mean()
        fig_season = px.line(x=season_series.index, y=season_series.values, labels={"x": "Jour de l'année", "y": "Probabilité"})
        fig_season.update_traces(line_color="#fd7e14", line_width=3)
        fig_season.update_layout(title="Saisonnalité (Moyenne lissée 7 jours)")
        fire_template(fig_season)

        return dbc.Row([
            dbc.Col(dbc.Card([dbc.CardHeader("Carte de Chaleur Temporelle"), dcc.Graph(figure=fig_heat)], className="custom-card"), lg=6),
            dbc.Col(dbc.Card([dbc.CardHeader("Profil Saisonnier"), dcc.Graph(figure=fig_season)], className="custom-card"), lg=6),
        ])
        
    elif active_tab == "tab-time":
        # Time Series
        if not vars_selected:
            return html.Div("Veuillez sélectionner des variables.", className="text-warning")
            
        fig_time = go.Figure()
        for v in vars_selected:
            # Resample for clearer chart if range is large
            daily = dff.groupby("DATE")[v].mean()
            fig_time.add_trace(go.Scatter(x=daily.index, y=daily.values, name=v, mode='lines', opacity=0.8))
            
        fig_time.update_layout(title="Evolution Temporelle des Variables")
        fire_template(fig_time)
        
        return dbc.Row([
            dbc.Col(dbc.Card([dbc.CardHeader("Séries Temporelles"), dcc.Graph(figure=fig_time)], className="custom-card"), width=12)
        ])
        
    elif active_tab == "tab-corr":
        # Scatter Matrix or Correlation
        if len(vars_selected) < 2:
            return html.Div("Sélectionnez au moins 2 variables pour voir les corrélations.", className="text-warning")
            
        fig_corr = px.scatter_matrix(dff, dimensions=vars_selected, color="FIRE_START_DAY", 
                                   color_discrete_map={True: "#fd7e14", False: "#007bff"}, opacity=0.5)
        fig_corr.update_layout(title="Matrice de Corrélation (Orange = Jour d'incendie)")
        fire_template(fig_corr)
        
        return dbc.Row([
            dbc.Col(dbc.Card([dbc.CardHeader("Analyse Multivariée"), dcc.Graph(figure=fig_corr)], className="custom-card"), width=12)
        ])
        
    elif active_tab == "tab-map":
        # Simple Choropleth (Total Fires per Year/Period) - Placeholder as we don't have lat/lon
        # We can show total fires for CA
        total_fires = dff["FIRE_START_DAY"].sum()
        fig_map = go.Figure(go.Choropleth(
            locations=["CA"], locationmode="USA-states", z=[total_fires],
            colorscale="Reds", zmin=0, showscale=True
        ))
        fig_map.update_geos(scope="usa", fitbounds="locations", visible=False, bgcolor="rgba(0,0,0,0)")
        fig_map.update_layout(title=f"Total Incendies sur la période: {int(total_fires)}")
        fire_template(fig_map)
        
        return dbc.Row([
            dbc.Col(dbc.Card([dbc.CardHeader("Localisation (État)"), dcc.Graph(figure=fig_map)], className="custom-card"), width=12)
        ])

    return html.Div("Onglet en construction.")

def run(debug: bool = True, host: str = "127.0.0.1", port: int = 8050):
    app.run(debug=debug, host=host, port=port)

if __name__ == "__main__":
    run(debug=True)
