import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

########### Define your variables
beers=['Chesapeake Stout', 'Snake Dog IPA', 'Imperial Porter', 'Double Dog IPA']
ibu_values=[35, 60, 85, 75]
abv_values=[5.4, 7.1, 9.2, 4.3]
color1='lightblue'
color2='darkgreen'
mytitle='Beer Comparison'
tabtitle='beer!'
myheading='Flying Dog Beers'
label1='IBU'
label2='ABV'
githublink='https://github.com/austinlasseter/flying-dog-beers'
sourceurl='https://www.flyingdog.com/beers/'

########### Set up the chart
bitterness = go.Bar(
    x=beers,
    y=ibu_values,
    name=label1,
    marker={'color':color1}
)
alcohol = go.Bar(
    x=beers,
    y=abv_values,
    name=label2,
    marker={'color':color2}
)

beer_data = [bitterness, alcohol]
beer_layout = go.Layout(
    barmode='group',
    title = mytitle
)

beer_fig = go.Figure(data=beer_data, layout=beer_layout)


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

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
