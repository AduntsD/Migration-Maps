#import pathlib
from dash import Dash, dcc, Output, Input, html  # pip install dash
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import plotly.express as px
import pandas as pd                        # pip install pandas

# incorporate data into app
# Source - https://www.cdc.gov/nchs/pressroom/stats_of_the_states.htm
#PATH = pathlib.Path(__file__).parent
#DATA_PATH = PATH.joinpath("data").resolve()
df = pd.read_csv("share_no_educ_alldest.csv")


# Build your components
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
#app.title = "Migration Wishes"
mytitle = dcc.Markdown(children='# Percentage of Population in Origin Country Wishing to Migrate to ')
mygraph = dcc.Graph(figure={})
dropdown = dcc.Dropdown(options=df.columns.values[6:13],
                        value='Germany',  # initial value displayed when the page first loads
                        clearable=False)

# Customize your own Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([mytitle], width=12)
    ], justify='center'),
    dbc.Row([
        dbc.Col([mygraph], width=12)
    ]),
    dbc.Row([
        dbc.Col([dropdown], width=6)
    ], justify='center'),

], fluid=True)

# Callback allows components to interact
@app.callback(
    Output(mygraph, 'figure'),
    Output(mytitle, 'children'),
    Input(dropdown, 'value')
)
def update_graph(column_name):  # function arguments come from the component property of the Input

    print(column_name)
    print(type(column_name))
    # https://plotly.com/python/choropleth-maps/
    fig = px.choropleth(data_frame=df,
                        locations='origin',
                        locationmode="country names",
                        scope="world",
                        height=600,
                        color=column_name,
                        color_continuous_scale=px.colors.sequential.Agsunset,
                        range_color=(0, 4),
                        color_continuous_midpoint=8,
                        animation_frame='year')
    
    fig.update_layout(coloraxis_colorbar_title='# % of Population')

    return fig, '# Percentage of Population in Origin Country Wishing to Migrate to ' + column_name  # returned objects are assigned to the component property of the Output

# Run app
if __name__ == '__main__':
    app.run_server(debug=False)
    
    