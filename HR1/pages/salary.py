import dash
from dash import dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import statsmodels

dash.register_page(__name__, path='/salary', name='Salary Analysis')



df = pd.read_csv('assets/HRDataset_v14.csv')
today = pd.to_datetime('2026-03-12')
df['DateofHire'] = pd.to_datetime(df['DateofHire'])
df['DateofTermination'] = pd.to_datetime(df['DateofTermination'])
df['Tenure_Years'] = (df['DateofTermination'].fillna(today) - df['DateofHire']).dt.days / 365.25
    

layout = dbc.Container([
    html.H3("Salary & Tenure Analysis", className="my-3"),
    
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.Label("Filter by Department:"),
            dcc.Dropdown(
                id='dept-selector',
                options=[{'label': i, 'value': i} for i in df['Department'].unique()],
                value=df['Department'].unique()[0], # Default to the first department
                clearable=False
            )
        ])), width=12, className="mb-4")
    ]),
    
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            dcc.Graph(id='salary-scatter-plot')
        ])), width=12)
    ])
])
color_map = {
    "Exceeds": "#1f77b4",           # Blue
    "Fully Meets": "#ff7f0e",       # Orange
    "Needs Improvement": "#2ca02c", # Green
    "PIP": "#d62728"                # Red
}
@callback(
    Output('salary-scatter-plot', 'figure'),
    Input('dept-selector', 'value')
)
def update_graph(selected_department):
    # Filtering data based on dropdown selection
    filtered_df = df[df['Department'] == selected_department]
    
    fig = px.scatter(
        filtered_df,
        x="Tenure_Years", 
        y="Salary", 
        color="PerformanceScore",
        color_discrete_map=color_map,
        marginal_y="violin",
        marginal_x="box",
        trendline="ols",
        template="simple_white",
        title=f"Salary vs. Experience in {selected_department}"
    )
    return fig
