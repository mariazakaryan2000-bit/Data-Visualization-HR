import dash
from dash import html, dcc
import dash_bootstrap_components as dbc


app = dash.Dash(
    __name__,
    use_pages=True,                # This allows Dash to find files in the 'pages' folder
    external_stylesheets=[dbc.themes.BOOTSTRAP] 
)
server = app.server
# 2. Create the Navigation Bar
navbar = dbc.NavbarSimple(
    children=[
        # This loop automatically creates a link for every page found in the 'pages' folder
        dbc.NavItem(dbc.NavLink(page["name"], href=page["path"], active="exact"))
        for page in dash.page_registry.values()
    ],
    brand="HR Analytics Dashboard",   # Title on the left side of the Navbar
    brand_href="/",                   # Clicking the title takes to the home page
    color="primary",                  # Classic Bootstrap blue color
    dark=True,                        # Tells Dash the background is dark, so text should be light
    className="mb-4"                  # Adds a small margin at the bottom of the navbar
)

# 3. Define the Global Layout
app.layout = dbc.Container([
    navbar,                           # Navbar stays at the top on every page
    dash.page_container               # This is where the content of each page will be displayed
], fluid=True)                        # 'fluid=True' makes the dashboard use the full width of the screen

# 4. Run the Server
if __name__ == "__main__":
    app.run(debug=True)