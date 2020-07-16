import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go



########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


########### Set up the layout
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 11:55:16 2020

@author: arupnar.mim2013
"""


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import dash_table
import math
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import json
from plotly.offline import plot
import plotly.express as px
from plotly.subplots import make_subplots
import sqlite3


colors=pd.read_excel(r'Plotly colours.xlsx')

def plot_stack(df,x_axis_col,y_axis_col,stacks_col,*hovercol):
    if x_axis_col is None or stacks_col is None:
        fig=go.Figure()
    else:
        if hovercol:
            for x in hovercol:
                hover_col=x
        else:
            hover_col=stacks_col
        fig=go.Figure()
        p=df.groupby([x_axis_col])[y_axis_col].sum().reset_index().sort_values(by=y_axis_col)
        # p=p[p[y_axis_col]!=0]
        j=p[y_axis_col].sum()    
            
        fig2=go.Scatter(y=p[y_axis_col],x=p[x_axis_col],text=p[x_axis_col],hoverinfo='x+y+text',mode='markers',name='Total',showlegend=True,marker_color='blueviolet')     
        fig.add_trace(fig2)       
        if (x_axis_col==stacks_col):
            if(hover_col==stacks_col):
                a=df.groupby([x_axis_col])[y_axis_col].sum().reset_index()
            else:
                if (x_axis_col==hover_col):
                    a=df.groupby([x_axis_col])[y_axis_col].sum().reset_index()
                else:
                    a=df.groupby([x_axis_col,hover_col])[y_axis_col].sum().reset_index()
        else:
            if (hover_col==stacks_col):
                a=df.groupby([x_axis_col,stacks_col])[y_axis_col].sum().reset_index()
            else:
                a=df.groupby([x_axis_col,stacks_col,hover_col])[y_axis_col].sum().reset_index()
                
        stacks=df[stacks_col].dropna().drop_duplicates(keep='first').reset_index().sort_values(by=stacks_col).reset_index()
        for i,v in stacks[stacks_col].items():
            # print(v)
            b=a[a[stacks_col]==v]
            q=b[y_axis_col].sum()/1000000
            # b=b[b[y_axis_col]!=0]
            # i=131
            x=i-115*(math.floor(i/115))
            
            fig1=go.Bar(y=b[y_axis_col],x=b[x_axis_col],hovertext=b[hover_col],hoverinfo='x+y+text',name=v+" ("+str("{:,.2f}".format(q))+"M)",showlegend=True,marker_color=colors.loc[x,'Colour'])
            
            fig.add_trace(fig1)
        fig.update_layout(hovermode='x',barmode='relative',title='Total : '+str("{:,.2f}".format(j))+'/-')
    return fig




# external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP,css']



# centres=pd.read_csv(r'C:\Users\arupnar.mim2013\AnacondaProjects\centres.csv')
# centres1=[{'label':i,'value':i} for i in centres['flexa_Profit Ctr']]

years=['2011-12','2012-13','2013-14','2014-15','2015-16','2016-17','2017-18','2018-19','2019-20']
years1=[{'label':i,'value':i} for i in years]



# app=dash.Dash(__name__,external_stylesheets=external_stylesheets,suppress_callback_exceptions = True)
       
# app.config['suppress_callback_exceptions'] = True


fig=go.Figure()


app.layout=html.Div([dcc.Dropdown(id='years',
                 options=years1,
                 value=[],#'P059-OIL STF MADHUBAN',
                 multi=True,
                 placeholder="Financial Year"),
    html.Div([
            html.Div(id='f-data',style={'display':'none'}),
            # html.Div(id='f-data1',style={'display':'none'}),
            html.Div([
                html.Div([
                    html.Label('Filter field : ',style={'width':'100%'}),
                    dcc.Dropdown(id='f-filtercol0',
                                 options=[],
                                 value='Financial Year',#'P059-OIL STF MADHUBAN',
                                 multi=False,
                                 placeholder="Filter field",
                                 clearable=False,
                                 style={'width':"100%"}),
                    html.Label('Filter values : ',style={'width':'100%'}),
                    dcc.Dropdown(id='f-filterval0',
                                 options=[],
                                 multi=True,
                                 placeholder="Filter values",
                                 value='2019-20',
                                 clearable=False,
                                 style={'width':'100%'})],
                    style={'width':'15%','display':'inline-block','vertical-align':'Top'}),
                html.Div([
                    html.Div([
                        html.Div([html.Label('X-axis : ')],style={'width':'5%','display':'inline-block','vertical-align':'Top'}),
                        html.Div([
                        dcc.Dropdown(id='f-xaxis1',
                                     options=[],
                                     value='GL Type',#'P059-OIL STF MADHUBAN',
                                     multi=False,
                                     placeholder="X-Axis")],
                        style={'width':'35%','display':'inline-block'}),
                    html.Div([html.Label('Legend : ')],style={'margin-left':'4%','width':'5%','display':'inline-block','vertical-align':'Top'}),
                    html.Div([
                        dcc.Dropdown(id='f-stacks1',
                                     options=[],
                                     value='Schedule',#'P059-OIL STF MADHUBAN',
                                     multi=False,
                                     placeholder="Legend")],
                        style={'width':'35%','display':'inline-block'})],
                    style={'width':'100%','margin-left':'5%'}),
                    html.Div([
                        dcc.Graph(id='f-fig1',figure=fig)],
                        style={'width':'100%'})],
                    style={'width':'85%','display':'inline-block'})],
                style={'width':'100%','border':'2px blue solid'}),
            html.Div([
                html.Div([
                    html.Label('Filter field : ',style={'width':'100%'}),
                    dcc.Dropdown(id='f-filtercol1',
                                 options=[],
                                 value='Schedule',#'P059-OIL STF MADHUBAN',
                                 multi=False,
                                 placeholder="Filter field",
                                 clearable=False,
                                 style={'width':"100%"}),
                    html.Label('Filter values : ',style={'width':'100%'}),
                    dcc.Dropdown(id='f-filterval1',
                                 options=[],
                                 multi=True,
                                 placeholder="Filter values",
                                 value='2019-20',
                                 clearable=False,
                                 style={'width':'100%'})],
                    style={'width':'15%','display':'inline-block','vertical-align':'Top'}),
                html.Div([
                    html.Div([
                        html.Div([html.Label('X-axis : ')],style={'width':'5%','display':'inline-block','vertical-align':'Top'}),
                        html.Div([
                        dcc.Dropdown(id='f-xaxis2',
                                     options=[],
                                     value='Account Name',#'P059-OIL STF MADHUBAN',
                                     multi=False,
                                     placeholder="X-Axis")],
                        style={'width':'35%','display':'inline-block'}),
                    html.Div([html.Label('Legend : ')],style={'margin-left':'4%','width':'5%','display':'inline-block','vertical-align':'Top'}),
                    html.Div([
                        dcc.Dropdown(id='f-stacks2',
                                     options=[],
                                     value='Schedule',#'P059-OIL STF MADHUBAN',
                                     multi=False,
                                     placeholder="Legend")],
                        style={'width':'35%','display':'inline-block'})],
                    style={'width':'100%','margin-left':'5%'}),
                    html.Div([
                        dcc.Graph(id='f-fig2',figure=fig)],
                        style={'width':'100%'})],
                    style={'width':'85%','display':'inline-block'})],
                style={'width':'100%','margin-top':'4%','border':'2px blue solid'}),
            html.Div([
                html.H3('All effects - GL name',style={'width':'20%','display':'inline-block','vertical-align':'Top'}),
                dcc.Dropdown(id='f-glname',
                             options=[],
                             multi=False,
                             placeholder="Type GL name",
                             # value='ABC',
                             clearable=False,
                             style={'width':'80%','display':'inline-block'}),],
                style={'margin-top':'4%','width':'100%','vertical-align':'Top'}),
            
                
            html.Div([
            html.Div([
                html.Div([
                html.Label('Filter field : ',style={'width':'100%'}),
                dcc.Dropdown(id='f-filtercol2',
                             options=[],
                             value='Financial Year',#'P059-OIL STF MADHUBAN',
                             multi=False,
                             placeholder="Filter field",
                             clearable=False,
                             style={'width':"100%"}),
                html.Label('Filter values : ',style={'width':'100%'}),
                dcc.Dropdown(id='f-filterval2',
                             options=[],
                             multi=True,
                             placeholder="Filter values",
                             # value='ABC',
                             clearable=False,
                             style={'width':'100%'})],
                    style={'width':'15%','display':'inline-block','vertical-align':'Top'}),
            
                html.Div([
                    html.Div([
                        html.Div([html.Label('X-axis : ')],style={'width':'5%','display':'inline-block','vertical-align':'Top'}),
                        html.Div([
                            dcc.Dropdown(id='f-xaxis3',
                                         options=[],
                                         value='Posting Date',#'P059-OIL STF MADHUBAN',
                                         multi=False,
                                         placeholder="X-Axis")],
                            style={'width':'35%','display':'inline-block'}),
                        html.Div([html.Label('Legend : ')],style={'margin-left':'4%','width':'5%','display':'inline-block','vertical-align':'Top'}),
                        html.Div([
                            dcc.Dropdown(id='f-stacks3',
                                         options=[],
                                         value='Schedule',#'P059-OIL STF MADHUBAN',
                                         multi=False,
                                         placeholder="Legend")],
                            style={'width':'35%','display':'inline-block'})],
                        style={'width':'100%','margin-left':'5%'}),
                    
                    html.Div([
                        dcc.Graph(id='f-fig3',figure=fig)],
                        style={'width':'100%'})],
                    style={'width':'85%','display':'inline-block'})],
                style={'width':'100%','display':'flex'}),
            html.Div([
               
                    html.Label('Other effects ',style={'width':'15%','display':'inline-block','vertical-align':'Top'}),
               
                    html.Div([
                        dcc.Graph(id='f-fig4',figure=fig)],
                        style={'width':'85%','display':'inline-block'})],
                   
                style={'width':'100%'}),],
            style={'width':'100%','border':'2px blue solid'})],
            style={'width':'100%'})])

@app.callback(Output('f-data','children'),
              [Input('years','value')])
def update_data(value):

     v=[]
     if type(value)==str:
         v=[value]
     else:
         for val in value:
             v.append(val)
     data=pd.read_pickle(r'sugardata1.pkl')
     data1=data[data['Financial Year'].isin(v)]
     pivot1=pd.pivot_table(data1,index=['Financial Year','GL Type','Schedule','Account Name'],values=['Amount'],aggfunc=np.sum).reset_index()
     final={'pivot1':pivot1.to_json(orient='split',date_format='iso')}
     return json.dumps(final)

@app.callback(Output('f-filtercol0','options'),
              [Input('f-data','children')])#,
              # Input('years','value')])
def update_figure(value):
    b=json.loads(value)
    data=pd.read_json(b['pivot1'],orient='split')
    # data=pd.read_pickle(r'C:\Users\arupnar.mim2013\AnacondaProjects\sugardata1.pkl')
    
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
    return options

@app.callback(Output('f-filterval0','options'),
              [Input('f-data','children'),
               Input('f-filtercol0','value')])#,
              # Input('years','value')])
def update_figure(value,value2):
    b=json.loads(value)
    data=pd.read_json(b['pivot1'],orient='split')
    # data=pd.read_pickle(r'C:\Users\arupnar.mim2013\AnacondaProjects\sugardata1.pkl')
    if data.empty or value2 is None:
        options=[]
    else:
        data1=data[value2].dropna().drop_duplicates(keep='first').reset_index().sort_values(by=value2)
        options=[{'label':i,'value':i} for i in data1[value2]]
    return options

@app.callback(Output('f-filterval0','value'),
              [Input('f-data','children'),
               Input('f-filtercol0','value')])#,
              # Input('centres','value')])
def update_figure(value,value2):
    b=json.loads(value)
    data=pd.read_json(b['pivot1'],orient='split')
    # data=pd.read_pickle(r'C:\Users\arupnar.mim2013\AnacondaProjects\sugardata1.pkl')
    if data.empty or value2 is None:
        options=[]
    else:
        data1=data[value2].dropna().drop_duplicates(keep='first').reset_index().sort_values(by=value2)
        options=data1[value2]
    return options

@app.callback(Output('f-xaxis1','options'),
              [Input('f-data','children')])#,
              # Input('centres','value')])
def update_figure(value):
    b=json.loads(value)
    data=pd.read_json(b['pivot1'],orient='split')
    # data=pd.read_pickle(r'C:\Users\arupnar.mim2013\AnacondaProjects\sugardata1.pkl')
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
    return options


@app.callback(Output('f-stacks1','options'),
              [Input('f-data','children')])#,
              # Input('centres','value')])
def update_figure(value):
    b=json.loads(value)
    data=pd.read_json(b['pivot1'],orient='split')
    # data=pd.read_pickle(r'C:\Users\arupnar.mim2013\AnacondaProjects\sugardata1.pkl')
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
    return options


@app.callback(Output('f-fig1','figure'),
              [Input('f-data','children'),
                Input('f-xaxis1','value'),
                Input('f-stacks1','value'),
                Input('f-filtercol0','value'),
                Input('f-filterval0','value')])
def update_figure(value,xaxis,stacks,filtercol1,filterval1):#,filtercol2,filterval2,filtercol3,filterval3):
    b=json.loads(value)
    data=pd.read_json(b['pivot1'],orient='split')
    # data=pd.read_pickle(r'C:\Users\arupnar.mim2013\AnacondaProjects\sugardata1.pkl')
    if data.empty:
        fig=go.Figure()
    else:
        v=[]
        if type(filterval1)==str:
            v=[filterval1]
        else:
            for val in filterval1:
                v.append(val)
       
      
        data1=data[(data[filtercol1].isin(v))]#&(data[filtercol2].isin(w))]#&(data[filtercol3].isin(x))]
        if data1.empty:
            fig=go.Figure()
        else:
            fig=plot_stack(data1,xaxis,'Amount',stacks)
    return fig


@app.callback(Output('f-filtercol1','options'),
              [Input('f-data','children')])#,
              # Input('centres','value')])
def update_figure(value):
    b=json.loads(value)
    data=pd.read_json(b['pivot1'],orient='split')
    # data=pd.read_pickle(r'C:\Users\arupnar.mim2013\AnacondaProjects\sugardata1.pkl')
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
    return options

@app.callback(Output('f-filterval1','options'),
              [Input('f-data','children'),
               Input('f-filtercol1','value')])#,
              # Input('centres','value')])
def update_figure(value,value2):
    b=json.loads(value)
    data=pd.read_json(b['pivot1'],orient='split')
    # data=pd.read_pickle(r'C:\Users\arupnar.mim2013\AnacondaProjects\sugardata1.pkl')
    if data.empty or value2 is None:
        options=[]
    else:
        data1=data[value2].dropna().drop_duplicates(keep='first').reset_index().sort_values(by=value2)
        options=[{'label':i,'value':i} for i in data1[value2]]
    return options


@app.callback(Output('f-filtercol2','options'),
              [Input('f-data','children')])#,
              # Input('centres','value')])
def update_figure(value):
    b=json.loads(value)
    data=pd.read_json(b['pivot1'],orient='split')
    # data=pd.read_pickle(r'C:\Users\arupnar.mim2013\AnacondaProjects\sugardata1.pkl')
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
    return options

@app.callback(Output('f-filterval2','options'),
              [Input('f-data','children'),
               Input('f-filtercol2','value')])#,
              # Input('centres','value')])
def update_figure(value,value2):
    b=json.loads(value)
    data=pd.read_json(b['pivot1'],orient='split')
    # data=pd.read_pickle(r'C:\Users\arupnar.mim2013\AnacondaProjects\sugardata1.pkl')
    if data.empty or value2 is None:
        options=[]
    else:
        data1=data[value2].dropna().drop_duplicates(keep='first').reset_index().sort_values(by=value2)
        options=[{'label':i,'value':i} for i in data1[value2]]
    return options



@app.callback(Output('f-xaxis2','options'),
              [Input('f-data','children')])#,
              # Input('centres','value')])
def update_figure(value):
    b=json.loads(value)
    data=pd.read_json(b['pivot1'],orient='split')
    # data=pd.read_pickle(r'C:\Users\arupnar.mim2013\AnacondaProjects\sugardata1.pkl')
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
    return options


@app.callback(Output('f-stacks2','options'),
              [Input('f-data','children')])#,
              # Input('centres','value')])
def update_figure(value):
    b=json.loads(value)
    data=pd.read_json(b['pivot1'],orient='split')
    # data=pd.read_pickle(r'C:\Users\arupnar.mim2013\AnacondaProjects\sugardata1.pkl')
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
    return options

@app.callback(Output('f-xaxis3','options'),
              [Input('f-data','children')])#,
              # Input('centres','value')])
def update_figure(value):
    b=json.loads(value)
    # data=pd.read_json(b['pivot1'],orient='split')
    data=pd.read_pickle(r'sugardata1.pkl')
    if data.empty:
        options=[]
    else:
        # data1=data.columns
        # data2=data1.replace("/","-")
        options=[{'label':i,'value':i} for i in data.columns]
    return options


@app.callback(Output('f-stacks3','options'),
              [Input('f-data','children')])#,
              # Input('centres','value')])
def update_figure(value):
    b=json.loads(value)
    # data=pd.read_json(b['pivot1'],orient='split')
    data=pd.read_pickle(r'sugardata1.pkl')
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
    return options


@app.callback(Output('f-fig2','figure'),
              [Input('f-data','children'),
                Input('f-xaxis2','value'),
                Input('f-stacks2','value'),
                Input('f-filtercol1','value'),
                Input('f-filterval1','value')])
def update_figure(value,xaxis,stacks,filtercol1,filterval1):#,filtercol2,filterval2,filtercol3,filterval3):
    b=json.loads(value)
    data=pd.read_json(b['pivot1'],orient='split')
    # data=pd.read_pickle(r'C:\Users\arupnar.mim2013\AnacondaProjects\sugardata1.pkl')
    if data.empty:
        fig=go.Figure()
    else:
        v=[]
        if type(filterval1)==str:
            v=[filterval1]
        else:
            for val in filterval1:
                v.append(val)
       
      
        data1=data[(data[filtercol1].isin(v))]#&(data[filtercol2].isin(w))]#&(data[filtercol3].isin(x))]
        if data1.empty:
            fig=go.Figure()
        else:
            fig=plot_stack(data1,xaxis,'Amount',stacks)
    return fig

@app.callback(Output('f-glname','options'),
              [Input('f-data','children')])
def update_figure(value):
   b=json.loads(value)
   data=pd.read_json(b['pivot1'],orient='split')
   # data=pd.read_pickle(r'C:\Users\arupnar.mim2013\AnacondaProjects\sugardata1.pkl')
   # v=[]
   # if type(value2)==str:
   #     v=[value2]
   # else:
   #      for val in value2:
   #          v.append(val)
   if data.empty:
       options=[]
   else:
       # data['glgroup_GL name']=data['glgroup_GL name'].str.replace("/","-")
       data1=data['Account Name'].dropna().drop_duplicates(keep='first').reset_index()
       options=[{'label':i,'value':i} for i in data1['Account Name']]

       # options=data
   return options


@app.callback(Output('f-fig3','figure'),
              [Input('f-data','children'),
               Input('f-xaxis3','value'),
               Input('f-stacks3','value'),
               Input('f-filtercol2','value'),
               Input('f-filterval2','value'),
               Input('f-glname','value'),
               Input('years','value')])
def update_figure(value,xaxis,stacks,filtercol1,filterval1,glname,year):#,filtercol2,filterval2,filtercol3,filterval3):
    b=json.loads(value)
    # data=pd.read_json(b['pivot1'],orient='split')
    data=pd.read_pickle(r'sugardata1.pkl')
    p=[]
    if type(year)==str:
        p=[year]
    else:
        for val in year:
            p.append(val)
    data11=data[data['Financial Year'].isin(p)]
    # data['Account Name'].unique()
    # glname='AUTADE SUGARS PVT LTD'
    w=[]
    if type(filterval1)==str or filterval1==None:
        w=[filterval1]
    else:
        for val in filterval1:
            w.append(val)
    
    data1=data11[data11['Account Name']==glname]
    data2=data1[data1[filtercol1].isin(w)]
    data1keys=data2['Document Number'].dropna().drop_duplicates(keep='first')
    data3=data[data['Document Number'].isin(data1keys)]
    data=data3
    if data.empty:
        fig=go.Figure()
    else:
        v=[]
        if type(glname)==str:
            v=[glname]
        else:
            for val in glname:
                v.append(val)
        # data=data[data['Effect']=='Self-effects']
       # data=pivot1
       # filtercol1='flexa_Year'
       # v=['2019.0']
        # keys=data[data[filtercol1].isin(v)]
        # keys1=keys['flexa_key_x'].dropna().drop_duplicates(keep='first')
        # data1=data[data['flexa_key_x'].isin(keys1)]
        data2=data[data['Account Name'].isin(v)]
        # print(data.columns)
        data2=data2.sort_values(by='Posting Date')
        data2['Posting Date']=data2['Posting Date'].dt.strftime('%m/%Y')
        
        # data1['flexa_Pstng Date']=data1['flexa_Pstng Date'].astype('category')
        if data2.empty:
            fig=go.Figure()
        else:
            # data1['new']=data1['bkpf_']
            fig=plot_stack(data2,xaxis,'Amount',stacks,'Particulars')
            if (xaxis=='Posting Date'):
                 fig.update_layout(xaxis = dict(type = "category"))
                 fig.update_layout(xaxis=dict(categoryarray=data2['Posting Date']))
                 # fig.update_layout(hoverinfo=data1['flexa_Profit Ctr'])
   
    return fig
# xaxis='Posting Date'
# stacks='Account Name'
# plot(fig)
@app.callback(Output('f-fig4','figure'),
              [Input('f-data','children'),
               Input('f-xaxis3','value'),
               Input('f-stacks3','value'),
               Input('f-filtercol2','value'),
               Input('f-filterval2','value'),
               Input('f-glname','value'),
                Input('years','value')])
def update_figure(value,xaxis,stacks,filtercol1,filterval1,glname,year):#,filtercol2,filterval2,filtercol3,filterval3):
    b=json.loads(value)
    # data=pd.read_json(b['pivot1'],orient='split')
    data=pd.read_pickle(r'sugardata1.pkl')
    # data['Account Name'].unique()
    # glname='AUTADE SUGARS PVT LTD'
    p=[]
    if type(year)==str:
        p=[year]
    else:
        for val in year:
            p.append(val)
    data11=data[data['Financial Year'].isin(p)]
    w=[]
    if type(filterval1)==str or filterval1==None:
        w=[filterval1]
    else:
        for val in filterval1:
            w.append(val)
    
    data1=data11[data11['Account Name']==glname]
    data2=data1[data1[filtercol1].isin(w)]
    data1keys=data2['Document Number'].dropna().drop_duplicates(keep='first')
    data3=data[data['Document Number'].isin(data1keys)]
    data=data3
    if data.empty:
        fig=go.Figure()
    else:
        v=[]
        if type(glname)==str:
            v=[glname]
        else:
            for val in glname:
                v.append(val)
        # data=data[data['Effect']=='Self-effects']
       # data=pivot1
       # filtercol1='flexa_Year'
       # v=['2019.0']
        # keys=data[data[filtercol1].isin(v)]
        # keys1=keys['flexa_key_x'].dropna().drop_duplicates(keep='first')
        # data1=data[data['flexa_key_x'].isin(keys1)]
        data2=data[-data['Account Name'].isin(v)]
        # print(data.columns)
        data2=data2.sort_values(by='Posting Date')
        data2['Posting Date']=data2['Posting Date'].dt.strftime('%m/%Y')
        
        # data1['flexa_Pstng Date']=data1['flexa_Pstng Date'].astype('category')
        if data2.empty:
            fig=go.Figure()
        else:
            # data1['new']=data1['bkpf_']
            fig=plot_stack(data2,xaxis,'Amount',stacks,'Particulars')
            if (xaxis=='Posting Date'):
                 fig.update_layout(xaxis = dict(type = "category"))
                 fig.update_layout(xaxis=dict(categoryarray=data2['Posting Date']))
                 # fig.update_layout(hoverinfo=data1['flexa_Profit Ctr'])
   
    return fig

# @app.callback(Output('f-fig3','figure'),
#               [Input('f-data','children'),
#                Input('f-xaxis3','value'),
#                Input('f-stacks3','value'),
#                Input('f-filtercol2','value'),
#                Input('f-filterval2','value'),
#                Input('centres','value')])#,
            
# def update_figure(value,xaxis,stacks,filtercol,filterval,centres):#,filtercol2,filterval2,filtercol3,filterval3):
#     b=json.loads(value)
#     data=pd.read_json(b['pivot1'],orient='split')
#     if data.empty:
#         fig=go.Figure()
#     else:
#         # if filtercol1 is None or filterval1 is None:
#         #     fig=go.Figure()
#         # else:
#         v=[]
#         # for val in filterval:
#         #     v.append(val)
            
#         # w=[]
#         if type(filterval)==str:
#             v=[filterval]
#         elif type(filterval)==list:
#             for val in filterval:
#                 v.append(val)
       
#         x=[]
#         if type(centres)==str:
#             x=[centres]
#         else:
#             for val in centres:
#                 x.append(val)
                
#         # # if not v:
#         #         fig=go.Figure()
#         #     else:
#         data1=data[data[filtercol].isin(v)]['flexa_key_x'].dropna().drop_duplicates(keep='first').reset_index()#&(data[filtercol2].isin(w))]#&(data[filtercol3].isin(x))]
#         data2=data[(data['flexa_key_x'].isin(data1['flexa_key_x']))]#&(-((data[filtercol].isin(v))))]#&(data['flexa_Profit Ctr'].isin(x)))))]
        
#         if data1.empty:
#             fig=go.Figure()
#         else:
#             fig=plot_stack(data2,xaxis,'flexa_LC Amount',stacks)
#     return fig
       


    # 
if __name__ == '__main__':
    app.run_server()
