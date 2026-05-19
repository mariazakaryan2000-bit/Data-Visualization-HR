import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# 1. Register the page
dash.register_page(__name__, path='/', name='Overview')

# 2. Helper function to create KPI cards
def make_card(title, value, color):
    return dbc.Card([
        dbc.CardBody([
            html.H5(title, className="card-title text-muted"),
            html.H2(value, className=f"text-{color}")
        ])
    ], className="shadow-sm h-100")

# 3. Load and Process Data
df = pd.read_csv('assets/HRDataset_v14.csv')
today = pd.to_datetime('2026-03-12')
df['DateofHire'] = pd.to_datetime(df['DateofHire'])
df['DateofTermination'] = pd.to_datetime(df['DateofTermination'])
df['Tenure_Years'] = (df['DateofTermination'].fillna(today) - df['DateofHire']).dt.days / 365.25

# Metrics Calculation
total_employees = len(df)
avg_salary = df['Salary'].mean()
active_employees = len(df[df['Termd'] == 0])

# 4. Create Visualizations
# Chart 1: Distribution by Department
fig_pie = px.pie(df, names='Department', title='Workforce by Department', hole=0.4)
fig_pie.update_layout(margin=dict(t=40, b=0, l=0, r=0))

# Chart 2: Average Salary by Department
df_dept_sal = df.groupby('Department')['Salary'].mean().reset_index()
fig_bar = px.bar(df_dept_sal, x='Department', y='Salary', 
                 title='Average Salary by Department',
                 labels={'Salary': 'Avg Salary ($)'})
fig_bar.update_layout(margin=dict(t=40, b=0, l=0, r=0))

# 5. Main Layout
layout = dbc.Container([
    # Page Title
    html.H2("HR Executive Summary", className="text-center my-4 fw-bold"),
    
    # Row 1: KPI Cards
    dbc.Row([
        dbc.Col(make_card("Total Staff", f"{total_employees}", "primary"), width=4),
        dbc.Col(make_card("Avg. Salary", f"${avg_salary:,.0f}", "success"), width=4),
        dbc.Col(make_card("Active Employees", f"{active_employees}", "info"), width=4),
    ], className="mb-5"),

    # Section Title
    html.H3("Workforce Insights", className="text-secondary mb-4"),

    # Row 2: Charts
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=fig_pie)
                ])
            ], className="shadow-sm")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=fig_bar)
                ])
            ], className="shadow-sm")
        ], width=6),
    ], className="mb-4")

], fluid=True)