import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go



########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


########### Set up the layout
app.layout=html.Div([
    # dcc.Store(id='store_financials'),
    # dcc.Store(id='store_customers'),
    dcc.Dropdown(id='centres',
                 options=[],
                 value=[],#'P059-OIL STF MADHUBAN',
                 multi=True,
                 placeholder="Project name"),
    dcc.Tabs(id='tabs',
              # value='materialtab',
             children=[
                 dcc.Tab(label='Financials',value='financetab'),
                
                 dcc.Tab(label='Customers',value='customertab'),
                 dcc.Tab(label='Vendors',value='vendortab'),
                 dcc.Tab(label='Materials',value='materialtab'),
                 dcc.Tab(label='Documents',value='documenttab'),
                 dcc.Tab(label='Search',value='searchtab')]),
    html.Div(id='content',children=z)])

if __name__ == '__main__':
    app.run_server()
