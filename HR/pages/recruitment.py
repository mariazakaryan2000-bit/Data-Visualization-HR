import dash
from dash import dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path='/recruitment', name='Recruitment ROI')


df = pd.read_csv('assets/HRDataset_v14.csv')
today = pd.to_datetime('2026-03-12')
df['DateofHire'] = pd.to_datetime(df['DateofHire'])
df['DateofTermination'] = pd.to_datetime(df['DateofTermination'])
df['Tenure_Years'] = (df['DateofTermination'].fillna(today) - df['DateofHire']).dt.days / 365.25


layout = dbc.Container([
    html.H3("Recruitment Performance", className="my-3"),
    
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.Label("Minimum Salary Threshold:"),
            dcc.Slider(
                id='min-salary-slider',
                min=df['Salary'].min(),
                max=df['Salary'].max(),
                value=df['Salary'].min(),
                marks={i: f'${i//1000}k' for i in range(int(df['Salary'].min()), int(df['Salary'].max()), 40000)},
                step=5000
            )
        ])), width=12, className="mb-4")
    ]),
    
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            dcc.Graph(id='recruitment-bar-chart')
        ])), width=12)
    ])
])

@callback(
    Output('recruitment-bar-chart', 'figure'),
    Input('min-salary-slider', 'value')
)
def update_recruitment_chart(min_val):
    # Filter dataset for employees earning more than the slider value
    filtered_df = df[df['Salary'] >= min_val]
    
    fig = px.histogram(
        filtered_df,
        x="RecruitmentSource",
        color="PerformanceScore",
        title=f"Top Recruitment Sources (Salary > ${min_val:,.0f})",
        template="simple_white",
        category_orders={"PerformanceScore": ["Exceeds", "Fully Meets", "Needs Improvement", "PIP"]}
    )
    fig.update_layout(xaxis_tickangle=-45, barmode="stack")
    return fig