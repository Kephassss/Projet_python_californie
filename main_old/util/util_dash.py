from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pathlib import Path

try:
    from util.util_recuperation_data import (
        colonnes_defaut,
        assurer_colonnes_temporelles,
    )
except Exception:  # Direct run from inside util/
    from util_recuperation_data import (
        colonnes_defaut,
        assurer_colonnes_temporelles,
    )


# ---------- Data loading ----------
project_root = Path(__file__).resolve().parent.parent
data_path = project_root / "CA_Weather_Fire_Dataset_1984-2025.csv"
df = pd.read_csv(data_path, parse_dates=["DATE"]) if data_path.exists() else pd.DataFrame()

if not df.empty:
    # Ensure expected temporal columns exist
    df = assurer_colonnes_temporelles(df, besoin=("YEAR", "MONTH", "DAY_OF_YEAR", "DATE"), copy=True)
    # Normalize FIRE_START_DAY to bool
    if df.get("FIRE_START_DAY") is not None and df["FIRE_START_DAY"].dtype != bool:
        df["FIRE_START_DAY"] = (
            df["FIRE_START_DAY"].astype(str).str.lower().map({"true": True, "false": False})
        ).fillna(False)

# Variables available to plot (intersect with dataset)
available_vars = [c for c in colonnes_defaut if c in df.columns] if not df.empty else []


# ---------- App ----------
app = Dash(
    __name__,
    title="California Wildfires Dashboard",
    assets_folder=str(project_root / "assets"),
)
server = app.server


def fire_template(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0f0f0f",
        plot_bgcolor="#0f0f0f",
        font=dict(color="#f5f5f5"),
        margin=dict(l=40, r=20, t=60, b=40),
    )
    return fig


# ---------- Layout ----------
app.layout = html.Div(
    id="app-root",
    children=[
        html.Header(
            className="app-header",
            children=[
                html.H1("Incendies en Californie", className="title"),
                html.Div("Exploration interactive du climat et des départs de feu", className="subtitle"),
            ],
        ),
        html.Div(
            className="content",
            children=[
                html.Aside(
                    className="sidebar",
                    children=[
                        html.Div("Filtres", className="section-title"),
                        dcc.Dropdown(
                            id="var-select",
                            options=[{"label": v.replace("_", " "), "value": v} for v in available_vars],
                            value=available_vars[:1] if available_vars else [],
                            multi=True,
                            placeholder="Choisir les variables…",
                            className="control",
                        ),
                        dcc.RangeSlider(
                            id="year-range",
                            min=int(df["YEAR"].min()) if not df.empty else 1984,
                            max=int(df["YEAR"].max()) if not df.empty else 2025,
                            step=1,
                            value=[
                                int(df["YEAR"].min()) if not df.empty else 1984,
                                int(df["YEAR"].max()) if not df.empty else 2025,
                            ],
                            marks=None,
                            tooltip={"placement": "bottom", "always_visible": True},
                            className="control",
                        ),
                        dcc.RadioItems(
                            id="unit",
                            options=[
                                {"label": "Fahrenheit", "value": "F"},
                                {"label": "Celsius", "value": "C"},
                            ],
                            value="F",
                            className="control radio",
                        ),
                        dcc.Slider(
                            id="smooth-window",
                            min=1,
                            max=21,
                            step=2,
                            value=7,
                            marks={1: "1", 7: "7", 14: "14", 21: "21"},
                            className="control",
                        ),
                        html.Div("Carte", className="section-title"),
                        dcc.RadioItems(
                            id="map-mode",
                            options=[
                                {"label": "Jour", "value": "jour"},
                                {"label": "Période", "value": "periode"},
                            ],
                            value="jour",
                            className="control radio",
                        ),
                        dcc.Slider(
                            id="day-of-year",
                            min=1,
                            max=366,
                            step=1,
                            value=200,
                            marks={1: "1", 91: "91", 182: "182", 274: "274", 366: "366"},
                            className="control",
                        ),
                        dcc.RangeSlider(
                            id="doy-range",
                            min=1,
                            max=366,
                            step=1,
                            value=[150, 250],
                            marks=None,
                            tooltip={"placement": "bottom", "always_visible": True},
                            className="control",
                        ),
                    ],
                ),
                html.Main(
                    className="main",
                    children=[
                        dcc.Tabs(id="tabs", value="series", className="dash-tabs", children=[
                            dcc.Tab(label="Séries", value="series"),
                            dcc.Tab(label="Heatmap Feux", value="fires"),
                            dcc.Tab(label="Heatmap Températures", value="temps"),
                            dcc.Tab(label="Saisonnalité", value="season"),
                            dcc.Tab(label="Boxplots", value="box"),
                            dcc.Tab(label="Carte", value="map"),
                        ]),
                        html.Div(id="tab-content", className="tab-content", children=[
                            dcc.Loading(
                                type="cube",
                                children=[
                                    dcc.Graph(id="fig-series"),
                                    dcc.Graph(id="fig-fires", style={"display": "none"}),
                                    dcc.Graph(id="fig-temps", style={"display": "none"}),
                                    dcc.Graph(id="fig-season", style={"display": "none"}),
                                    dcc.Graph(id="fig-box", style={"display": "none"}),
                                    dcc.Graph(id="fig-map", style={"display": "none"}),
                                ],
                            )
                        ]),
                    ],
                ),
            ],
        ),
        html.Footer(className="footer", children="Données: CA_Weather_Fire (1984–2025) • Thème incendie"),
    ],
)


# ---------- Helpers ----------
def apply_unit(dfx: pd.DataFrame, unit: str) -> pd.DataFrame:
    out = dfx.copy()
    if unit == "C":
        for col in ["MAX_TEMP", "MIN_TEMP"]:
            if col in out.columns:
                out[col] = (out[col] - 32) * 5.0 / 9.0
        if "TEMP_RANGE" in out.columns:
            out["TEMP_RANGE"] = out["TEMP_RANGE"] * 5.0 / 9.0
    return out


def filter_years(dfx: pd.DataFrame, year_min: int, year_max: int) -> pd.DataFrame:
    return dfx[(dfx["YEAR"] >= year_min) & (dfx["YEAR"] <= year_max)]


# ---------- Callbacks ----------
@app.callback(
    Output("fig-series", "figure"),
    Input("var-select", "value"),
    Input("year-range", "value"),
    Input("unit", "value"),
)
def update_series(vars_selected, year_range, unit):
    if df.empty or not vars_selected:
        fig = go.Figure()
        return fire_template(fig)

    dfx = apply_unit(filter_years(df, year_range[0], year_range[1]), unit)

    # Long-form for multi-variable overlay
    plot_df = dfx[["DAY_OF_YEAR", "YEAR"] + [v for v in vars_selected if v in dfx.columns]].melt(
        id_vars=["DAY_OF_YEAR", "YEAR"], var_name="Variable", value_name="Valeur"
    )

    fig = px.scatter(
        plot_df,
        x="DAY_OF_YEAR",
        y="Valeur",
        color="Variable",
        hover_data=["YEAR"],
        opacity=0.45,
        trendline=None,
    )
    fig.update_traces(marker=dict(size=5))
    fig.update_layout(title="Evolution par jour de l'année")
    return fire_template(fig)


@app.callback(
    Output("fig-fires", "figure"),
    Input("year-range", "value"),
)
def update_fires_heatmap(year_range):
    if df.empty:
        return fire_template(go.Figure())

    dfx = filter_years(df, year_range[0], year_range[1]).copy()
    dfx["FIRE_START_DAY_INT"] = dfx["FIRE_START_DAY"].astype(int)
    pivot = dfx.pivot_table(
        index="YEAR", columns="DAY_OF_YEAR", values="FIRE_START_DAY_INT", aggfunc="sum", fill_value=0
    )

    fig = go.Figure(
        data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns,
            y=pivot.index,
            colorscale="YlOrRd",
            colorbar=dict(title="Feux/jour"),
        )
    )
    fig.update_layout(title="Heatmap des départs de feu (jours × années)")
    return fire_template(fig)


@app.callback(
    Output("fig-temps", "figure"),
    Input("year-range", "value"),
    Input("unit", "value"),
)
def update_temp_heatmap(year_range, unit):
    if df.empty:
        return fire_template(go.Figure())
    dfx = apply_unit(filter_years(df, year_range[0], year_range[1]), unit)
    if "AVG_TEMP" in dfx.columns:
        avg = dfx["AVG_TEMP"].copy()
    else:
        avg = (dfx["MAX_TEMP"] + dfx["MIN_TEMP"]) / 2.0
    tmp = dfx.assign(AVG_TEMP_CALC=avg)
    pivot = tmp.pivot_table(index="YEAR", columns="MONTH", values="AVG_TEMP_CALC", aggfunc="mean")

    fig = go.Figure(
        data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns,
            y=pivot.index,
            colorscale="Inferno",
            colorbar=dict(title="Temp moyenne" + (" (°C)" if unit == "C" else " (°F)")),
        )
    )
    fig.update_layout(title="Températures moyennes (mois × années)")
    return fire_template(fig)


@app.callback(
    Output("fig-season", "figure"),
    Input("year-range", "value"),
    Input("smooth-window", "value"),
)
def update_seasonality(year_range, window):
    if df.empty:
        return fire_template(go.Figure())

    dfx = filter_years(df, year_range[0], year_range[1])
    series = (
        dfx.groupby("DAY_OF_YEAR")["FIRE_START_DAY"].mean().sort_index()
    )
    if window and window > 1:
        series = series.rolling(window, min_periods=1, center=True).mean()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=series.index, y=series.values, mode="lines", line=dict(color="#ff6a00")))
    fig.update_layout(title="Profil saisonnier des départs de feu (moyenne)", xaxis_title="Jour de l'année", yaxis_title="Taux moyen")
    return fire_template(fig)


@app.callback(
    Output("fig-box", "figure"),
    Input("var-select", "value"),
    Input("year-range", "value"),
    Input("unit", "value"),
)
def update_box(vars_selected, year_range, unit):
    if df.empty or not vars_selected:
        return fire_template(go.Figure())
    var = vars_selected[0]
    dfx = apply_unit(filter_years(df, year_range[0], year_range[1]), unit)
    if var not in dfx.columns:
        return fire_template(go.Figure())
    fig = px.box(dfx, x="MONTH", y=var, points="outliers", color_discrete_sequence=["#ff512f"])
    fig.update_layout(title=f"Distribution mensuelle: {var}")
    return fire_template(fig)


# Map: California choropleth shading by fire counts
@app.callback(
    Output("fig-map", "figure"),
    Input("year-range", "value"),
    Input("map-mode", "value"),
    Input("day-of-year", "value"),
    Input("doy-range", "value"),
)
def update_map(year_range, mode, day_of_year, doy_range):
    if df.empty:
        return fire_template(go.Figure())

    dfx = filter_years(df, year_range[0], year_range[1]).copy()
    dfx["FIRE_START_DAY_INT"] = dfx["FIRE_START_DAY"].astype(int)

    if mode == "jour" and day_of_year is not None:
        sub = dfx[dfx["DAY_OF_YEAR"].astype(int) == int(day_of_year)]
        total_fires = int(sub["FIRE_START_DAY_INT"].sum())
        years_count = max(1, year_range[1] - year_range[0] + 1)
        zmax = max(1, years_count)
        title = f"Incendies en Californie • Jour {int(day_of_year)} (somme sur {years_count} an(s))"
    else:
        start_doy, end_doy = (doy_range or [1, 366])
        if start_doy > end_doy:
            start_doy, end_doy = end_doy, start_doy
        sub = dfx[(dfx["DAY_OF_YEAR"] >= int(start_doy)) & (dfx["DAY_OF_YEAR"] <= int(end_doy))]
        total_fires = int(sub["FIRE_START_DAY_INT"].sum())
        years_count = max(1, year_range[1] - year_range[0] + 1)
        days_count = max(1, int(end_doy) - int(start_doy) + 1)
        zmax = max(1, years_count * days_count)
        title = f"Incendies en Californie • Jours {int(start_doy)}–{int(end_doy)} (somme sur {years_count} an(s))"

    fig = go.Figure(
        data=go.Choropleth(
            locations=["CA"],
            z=[total_fires],
            locationmode="USA-states",
            colorscale="Reds",
            zmin=0,
            zmax=zmax,
            colorbar=dict(title="Nbr d'incendies"),
            marker_line_color="white",
        )
    )
    fig.update_geos(scope="usa", fitbounds="locations", visible=False)
    fig.update_layout(title=title, margin=dict(l=10, r=10, t=60, b=10))
    return fire_template(fig)


# Only show the graph for the active tab
@app.callback(
    Output("fig-series", "style"),
    Output("fig-fires", "style"),
    Output("fig-temps", "style"),
    Output("fig-season", "style"),
    Output("fig-box", "style"),
    Output("fig-map", "style"),
    Input("tabs", "value"),
)
def toggle_tabs(active):
    styles = {"display": "none"}
    visible = {"display": "block"}
    return (
        visible if active == "series" else styles,
        visible if active == "fires" else styles,
        visible if active == "temps" else styles,
        visible if active == "season" else styles,
        visible if active == "box" else styles,
        visible if active == "map" else styles,
    )


def get_app():
    return app


def run(debug: bool = True, host: str = "127.0.0.1", port: int = 8050):
    app.run(debug=debug, host=host, port=port)


if __name__ == "__main__":
    run(debug=True)

