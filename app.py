import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go



########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


########### Set up the layout
app.layout=html.H3(['TEST'])
    # dcc.Store(id='store_financials'),
    # 
if __name__ == '__main__':
    app.run_server()
