import dash
import dash_core_components as dcc
import dash_html_components as html
import folium
import pandas as pd
import os
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server=app.server
port = int(os.environ.get('PORT', 5000))

url1 = 'https://raw.githubusercontent.com/krbarounis/Dash_app/master/plotly_2000.csv'
url2='https://raw.githubusercontent.com/krbarounis/Dash_app/master/plotly_2010.csv'
url3='https://raw.githubusercontent.com/krbarounis/Dash_app/master/plotly_changes.csv'
url4='https://raw.githubusercontent.com/krbarounis/Dash_app/master/plotly_changes_full.csv'
url5='https://raw.githubusercontent.com/krbarounis/Dash_app/master/clusters_and_2000.csv'
df_2000=pd.read_csv(url1,sep=',').round(2)
df_2010=pd.read_csv(url2,sep=',').round(2)
df_changes_sample=pd.read_csv(url3,sep=',').round(2)
df_changes_full=pd.read_csv(url4,sep=',').round(2)
df_low=df_changes_sample[df_changes_sample.income_bracket=='Bottom 25% (<37k)']
df_high=df_changes_sample[df_changes_sample.income_bracket=='Top 25% (> 63k)']
df_middle=df_changes_sample[df_changes_sample.income_bracket=='Middle 50% (<63k and >37k)']
df_clusters=pd.read_csv(url5,sep=',').round(2)

fig = make_subplots(rows=1,cols=2,subplot_titles=('% Change in Rent vs. % Change in Income',
                    '% Change in Home Value vs. % Change in Income'))
fig.add_trace(go.Scatter(
                      x=df_changes_full['MRENT00_PC'],
                      y=df_changes_full['HINC00_PC'],
                      mode='markers'),row=1,col=1)
fig.add_trace(go.Scatter(
                      x=df_changes_full['MHMVAL00_PC'],
                      y=df_changes_full['HINC00_PC'],
                        mode='markers'),row=1,col=2)
fig.update_xaxes(title_text='% Change in Median Rent',range=[-150,400],row=1,col=1)
fig.update_yaxes(title_text='% Change in Median Income',range=[-100,150],row=1,col=1)
fig.update_xaxes(title_text='% Change in Median Home Value',range=[-150,400],row=1,col=2)
fig.update_yaxes(title_text='% Change in Median Income',range=[-100,150],row=1,col=2)
fig.update_layout(showlegend=False)

app.layout = html.Div(children=[
    html.H1(
        children="Analyzing Trends in Boston's Suffolk County",
        style={'textAlign': 'center'
        }
    ),
    html.Div(children="""
        Welcome! In Section 1 of this dashboard, you will find data visualizations and analytical commentary regarding changes in socioeconomic, racial, and housing trends in Suffolk County, MA, which have been derived from the 2000 and 2010 decennial censuses. Further down, in Section 2, you'll find a data scientist's approach to grouping the county's census tracts by their shared features, and an interactive tool to learn more about each census tract. Enjoy!
    """),
    html.H3(children='''Section 1: Trends
    '''),
    html.H6(children='''Boston became more racially diverse
    '''),
  
    dcc.Graph(
        id='Fig1',
        figure={
            'data': [
                go.Bar(name='White', y=["2000 Census","2010 Census"], x=[df_2000.NHWHT00.sum(),df_2010.nhwht10.sum()],orientation='h',),
                      go.Bar(name='Non-white', y=["2000 Census","2010 Census"], x=[df_2000[['NHBLK00','NTV00','ASIAN00','HISP00',
                                                   'HAW00','INDIA00','CHINA00','FILIP00',
                                                   'JAPAN00','KOREA00','VIET00','MEX00',
                                                   'PR00','CUBAN00']].sum().sum(),
                                          df_2010[['nhblk10','ntv10','asian10','hisp10',
                                                   'haw10','india10','china10','filip10',
                                                   'japan10','korea10','viet10','mex10',
                                                   'pr10','cuban10']].sum().sum()],orientation='h')
            ],
            'layout': {
                'barmode':'stack',
                'title': 'Change in Racial Composition of Population 2000-2010',
                'xaxis':{
                        'title':'Population'}
            }
        }
    ),
    html.Div(children='''
        While Boston's population grew from approximately 690k in 2000 to 722k in 2010 (an increase of 4.5%), the non-Hispanic white population declined by ~13,000 (a decline of 3.5%) and the non-white population (defined as non-Hispanic blacks,
Hispanics of any race, Asians, and other non-whites) grew by ~64,000 (an increase of 16%). The city therefore continued to be a majority minority city. 
    '''),
    
    html.H5(children='''Boston became less affordable
    '''),
    dcc.Graph(figure=fig),
    
    html.Div(children='''Adjusting for inflation, changes in median rent and median home value outpaced changes in median household income. The median home value, median rent, and median household income in the county's median tract rose 41%, 24%, and 10% respectively. Additionally, housing costs rose in over 95% of tracts in the area, while only 61% of tracts saw increases in median household income.
    '''),
    html.H5(children='''The county saw an increase in income inequality
    '''),
    dcc.Graph(id='Fig2',
              figure={
                  'data':[
                      go.Scatter(x=df_low.HINC00,
                                 y=df_low.HINC00_PC,
                                 mode='markers',
                                 marker={
                                     'size':10},
                                 name='Bottom 25% (<$37k)'
                                ),
                      go.Scatter(x=df_high.HINC00,
                                 y=df_high.HINC00_PC,
                                 mode='markers',
                                 marker={
                                     'size':10},
                                 name='Top 25% (>$63k)'
                                ),
                      go.Scatter(x=df_middle.HINC00,
                                 y=df_middle.HINC00_PC,
                                 mode='markers',
                                 marker={
                                     'size':10},
                                 name='Middle 50% (<$63k and >$37k)'
                                )
                          ],
                    'layout': {
                    'title': 'Percentage change in Median Household Income vs. Income in 2000',
                    'xaxis':{
                        'title':'Median Household Income in 2000 (Adjusted for inflation)'},
                    'yaxis':{
                        'title':'% Change in Median Household Income (2000-2010)'}
                        }
                    }
             ),
    html.Div(children='''61% of census tracts in the county experienced an increase in median household income between 2000 and 2010. Within the highest quartile of tracts by median income in 2000, 69% realized income gains,while only 46% of census tracts in the lowest quartile saw increases. Additionally, tracts in the lowest quartile experienced a larger income decline overall than tracts in the highest quartile, with income levels falling an average of 23% and 11%, respectively.
    '''),
    html.H3(children='''Section 2: Investigating gentrification
    '''),
    html.Div(children='''Using an algorithm that creates groups by finding commonalities amongst a set of data, I divided the census tracts in Suffolk County into three, and have subjectively labeled them as i) gentrifying, ii) becoming more affordable, and iii) becoming more costly. I arrived at these labels by comparing the changes that occured within each cluster relative to the county average across 6 traditional indicators of gentrification. To get a better understanding of this concept, scroll over the radar plots below, and compare the values for the county average to the values for each cluster.
    '''),
    html.H5(children='''Cluster 1: Gentrifying
    '''),
    dcc.Graph(
        id='Fig3',
        figure={
            'data': [
                go.Scatterpolar(r=[29.95,87.36,69.79,28.49,11.23,129.64],
                  theta=['% Change in Household Income','% Change in Median Home Value','% Change in Median Rent', 
         '% Change in Owner Occupied Housing', '% Change in Non-White Population',
         '% Change in Population with College Degree'],
                    name='Cluster 1',
                               marker={
        'color':'red'
    }),
                go.Scatterpolar(
                  r=[8.20,76.14,54.41,6.23,28.04,36.73],
                  theta=['% Change in Household Income','% Change in Median Home Value','% Change in Median Rent', 
         '% Change in Owner Occupied Housing', '% Change in Non-White Population',
         '% Change in Population with College Degree'],
                  name='County Average',
                marker={
        'color':'blue'
    }
)],
            'layout': go.Layout(
                polar={
                    'radialaxis':{
                        'visible':True,
                        'range':[-20,125],
                    }
                }
            )
        } 
    ),
    html.Div(children='''This cluster represents neighborhoods that are gentrifying. In this group, five of the six variables increased more than those of the county average (those related to housing costs, education level, and owner occupancy), with the one exception being "% Change in Non-White Population". Minority groups are often displaced as a result gentrification, so we'd expect to see a decline in this variable. The county experienced an average increase of 28% in its Non-White population, while this cluster saw an increase of only 11%. While not a decline, this increase is 17% below the county average.
    '''),
    html.H5(children='''Cluster 2: Lagging behind
   '''),
    
    dcc.Graph(
        id='Fig4',
        figure={
            'data': [
                go.Scatterpolar(r=[-12.11,72.58,40.70,-7.45,22.16,2.05],
                  theta=['% Change in Household Income','% Change in Median Home Value','% Change in Median Rent', 
         '% Change in Owner Occupied Housing', '% Change in Non-White Population',
         '% Change in Population with College Degree'],
                    name='Cluster 2',
                               marker={
        'color':'green'
    }),
                go.Scatterpolar(
                  r=[8.20,76.14,54.41,6.23,28.04,36.73],
                  theta=['% Change in Household Income','% Change in Median Home Value','% Change in Median Rent', 
         '% Change in Owner Occupied Housing', '% Change in Non-White Population',
         '% Change in Population with College Degree'],
                  name='County Average',
                marker={
        'color':'blue'
    })],
            'layout': go.Layout(
                polar={
                    'radialaxis':{
                        'visible':True,
                        'range':[-20,125]
                    }
                }
            )
        }
    ),
    html.Div(children='''This cluster represents neighborhoods that aren't representative of Boston's overall upward trends in income, housing price, owner occupancy, and educated population. In contrast to the previous cluster, this group experienced declines in median household income and owner occupied housing units. The group experienced an increase of only 40% in median rent, while Boston saw an average growth of 54%. It also only experienced a 2% increase in population with a college degree, compared to the county average of 36%.
    '''),
    html.H5(children='''Cluster 3: Representing the average 
    '''),
    dcc.Graph(
        id='Fig5',
        figure={
            'data': [
                go.Scatterpolar(r=[19.24,81.35,61.29,7.34,40.02,34.12],
                  theta=['% Change in Household Income','% Change in Median Home Value','% Change in Median Rent', 
         '% Change in Owner Occupied Housing', '% Change in Non-White Population',
         '% Change in Population with College Degree'],
                    name='Cluster 3',
                               marker={
        'color':'orange'
    }),
                go.Scatterpolar(
                  r=[8.20,76.14,54.41,6.23,28.04,36.73],
                  theta=['% Change in Household Income','% Change in Median Home Value','% Change in Median Rent', 
         '% Change in Owner Occupied Housing', '% Change in Non-White Population',
         '% Change in Population with College Degree'],
                  name='County Average',
                marker={
        'color':'blue'
    })],
            'layout': go.Layout(
                polar={
                    'radialaxis':{
                        'visible':True,
                        'range':[-20,125]
                    }
                },
                plot_bgcolor='aliceblue',
            )
        }
    ),
    html.Div(children='''This cluster is representative of the county average, i.e. Boston overall, as the neighborhoods in this group generally experienced changes in line with those of the county average. We discussed those changes in Section 1. 
    '''),
    html.H4(children='''Map of Suffolk County Census Tracts by Cluster 
    ''',style={"textAlign": "center"}),
    html.Iframe(id='map',
                srcDoc=open('index4.html','r').read(),width=500,height=600,
                style={'width':'75%','padding-left':'12.5%','padding-right':'.5%'}),
    html.Div([
    html.H4("Choose two tract IDs and a variable!", style={"textAlign": "center"}),
        html.Div(children='''To understand how census tracts and clusters differ from each other, use the tool below to compare two neighborhoods of your choice. Click the left two drop down menus to pick Tract IDs (see map for reference to geographic area) and use the right menu to pick any 1 of the 6 variables''',style={"textAlign": "center"}),
        
        html.Div([html.Div([dcc.Dropdown(id='product-selected1',
                                     options=[{'label': i.title(), 'value': i} for i in df_clusters.columns.values[-7:-1]],
                                     value="Percent Change in Median Income")], className="six columns",
                       style={"width": "55%", "float": "right"}),
              html.Div([dcc.Dropdown(id='tractid1',
                                     options=[{'label':i,'value': i} for i in df_clusters.tractid],
                                     value=25025000100)], className="six columns",
                       style={"width": "40%", "float": "left"}),
              html.Div([dcc.Dropdown(id='tractid2',
                                     options=[{'label':i,'value': i} for i in df_clusters.tractid],
                                     value=25025000602)], className="six columns", style={"width": "40%", "float": "left"}),
              ], className="row", style={"padding": 50, "width": "60%", "margin-left": "auto", "margin-right": "auto"}),
    dcc.Graph(id='my-graph'),

    # dcc.Link('Go to Source Code', href='{}/code'.format(app_name))
], className="container")
])

@app.callback(
    dash.dependencies.Output('my-graph', 'figure'),
    [dash.dependencies.Input('product-selected1', 'value'),
     dash.dependencies.Input('tractid1', 'value'),
     dash.dependencies.Input('tractid2', 'value'),
    ])
def update_graph(selected_product1, tractid1, tractid2):
    df_clusters.index=df_clusters.tractid
    trace1 = go.Bar(x=['tract '+str(tractid1), 'tract '+str(tractid2)], y=[df_clusters[selected_product1].loc[tractid1],df_clusters[selected_product1].loc[tractid2]], name=selected_product1.title())

    return {
        'data': [trace1],
        'layout': go.Layout(title='Compare Tracts',
                            colorway=["#BD2F43", "#BD2F43"], hovermode="closest",
                            xaxis={'title': "Tract ID", 'titlefont': {'color': 'black', 'size': 14},
                                   'tickfont': {'size': 9, 'color': 'black'}},
                            yaxis={'title': f"{selected_product1.title()}", 'titlefont': {'color': 'black', 'size': 14, },
                                   'tickfont': {'color': 'black'}})}
                
if __name__ == '__main__':
    app.run(port=port)