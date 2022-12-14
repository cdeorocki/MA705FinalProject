import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import time 
import datetime
from dash import Dash, dash_table

app = Dash(__name__)
server = app.server

stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Importing data and removing unneeded columns
df = pd.read_csv('billionaires1996to2014min.csv', index_col=1)
df = df.drop(['Citizenship', 'Age', 'Sourceofwealth', 'IndustryAggregates', 'North', 'Region', 'Industry', 'Company', 'Deflator1996','Realnetworth', 'Realbillionaires', ' Gdpcurrentus ', 'Countrycode'], axis=1)
df.reset_index(inplace=True)

# Removing unused year stats - only looking at 2000-2014
df = df.loc[df.Year != '15-Sep']
df = df.loc[df.Year != '1996']
df = df.loc[df.Year != '1997']
df = df.loc[df.Year != '1998']
df = df.loc[df.Year != '1999']
df = df.loc[df.Year != '2015']

# Importing billionaire information to match to all records
df2 = pd.read_csv('billionaireinfo.csv', index_col=1)
df2.reset_index(inplace=True)

# Merging datasets
df2.index = df2.Name
df['Country'] = df.Name.map(df2.Country)
df['Region'] = df.Name.map(df2.Region)
df['DOB'] = df.Name.map(df2.DOB)
df['Gender'] = df.Name.map(df2.Gender)
df['Self Made'] = df.Name.map(df2.SelfMade)
df['Generation'] = df.Name.map(df2.Generation)
df['Industry'] = df.Name.map(df2.Industry)
df['Industry Aggregator'] = df.Name.map(df2.IndustryType)
df['Company'] = df.Name.map(df2.Company)
df['Company Info'] = df.Name.map(df2.Type)
df['Company Acquired'] = df.Name.map(df2.CompanyAcquired)

df = df.sort_values('Rank', axis = 0, ascending = True)
df['Year'] = df['Year'].astype('int')
df['Net Worth US Billion'] = round(df['Networthusbillion'],2)
df = df.drop(['Networthusbillion'], axis=1)
df['Count'] = int(1)
df.to_csv('X2.csv', index=False)

years = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014]


### pandas dataframe to html table
def generate_table(dataframe, max_rows=len(df)):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns]), style={'color':'white', 'textAlign':'center', 'background':'#00838F', 'borderSpacing': '4em', 'borderCollapse':'seperate'}
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ])for i in range(min(len(dataframe), max_rows))
        ], style={'textAlign':'center', 'width':'100%', 'background':'#fff6e5'})
    ])

fig = px.bar(df, x='Region', y='Count', color='Region')
fig2 = px.pie(df, values='Count', names='Gender')

### Layout Start
app.layout = html.Div([

    ### Header
    html.H1('Tracking Billionaires Over the Years From 2000 Through 2014',
        style={'textAlign':'center', 'color':'#00838F', 'fontFamily':'sans-serif'}),
    html.H3('Individual MA705 Project | Cecilly Deorocki', 
    style={'textAlign':'center', 'color':'#b2d8d8', 'fontFamily':'sans-serif'}),    
    ### End header

    ### Start second row Div container to display description
    html.Div(children=[
        html.Div([
            html.H3('What is this dashboard about?', style={'color':'#00838F'}),
            html.Section("This dashboard explores the number and origin of billionaires globally, over a period of years from 2000 through 2014."),
            html.Br(),
            html.Section("The original data has been published by Forbes each year and was collected further by researchers at Peterson Institute"),
            html.Section("for International Economics. As part of the study, the scholars tried to attain additional information such as wealth"),
            html.Section("origin, generation of wealth and company notes. The researchers focused on the years 1996, 2001 and 2014. This dashboard"),
            html.Section("attempts to provide an easy way to explore the data for all years from 2000 through 2014, in large part because the dataset"),
            html.Section("was most comprehensive during those years."),
            html.Br(),
            html.Section("For each year available, each billionaire at that time, is listed within the dataset. Accompanying this information"),
            html.Section("are details about the billionaires’ net worth in billions, net worth ranking per year, country and global region of"),
            html.Section("origin, date of birth, gender, whether their wealth was self-made or inherited, industry of operation, and details"),
            html.Section("about their associated company. The data was cleaned and merged to ensure multiple entries with varying levels of"),
            html.Section("detail regarding the same billionaire became uniform. Any missing information is marked as unknown."),
        ],style={'display': 'inline-block', 'width':'45%', 'border':'1px #bbcecc solid', 'padding':'10px', 'margin': '20px', 'background' : '#d8ebeb'}),
        html.Div([
            html.H3('How to use this dashboard:', style={'color':'#00838F'}),
            html.Section("Select a year from the drop-down menu."),
            html.Br(),
            html.Section("This will adjust the bar chart which displays number of billionaires by region for the year selected."),
            html.Section("This will also adjust the pie chart which displays gender breakdown of billionaires for the year selected."),
            html.Br(),
            html.Section("The Bar Chart Options radio item revises the bar chart to display the gender, wealth origin or industry allocation of billionaires for the year selected."),
            html.Section("The Pie Chart Options radio item revises the pie chart to display the region, wealth origin or industry allocation of billionaires for the year selected."),
            html.Section("This allows your to visually compare different billioniare variables against eachother for specific years."),
            html.Br(),
            html.Section("For further detail about each individual billionaire within a selected year, including their name, date of birth, ranking and the"),
            html.Section("applicability of inter-generational wealth, among other variables, please explore the table which lists all details of this dashboard"),
            html.Section("and is in ascending order by billionaire ranking per the year displayed.")
        ],style={'display': 'inline-block', 'width':'55%', 'border':'1px #bbcecc solid', 'padding':'10px', 'margin': '20px', 'background' : '#d8ebeb'}),
    ],style={"display": "flex"}),
    ### End second row

     ### Third row div blocks for year drop down
         html.Div([
                 html.H3('Select Year:', style={'color':'white'}),
                 dcc.Dropdown(years, '2000', id='year_dropdown', style={'width' : '80%', 'margin': '10px', 'float' : 'center', 'color' : '#ffa700'}),
             ],style={'display': 'inline-block', 'width':'98%', 'border':'2px #ffa700 solid', 'padding':'1px', 'margin': '20px', 'background' : '#00838F'}),
     ### End third row

    ### Fourth row div blocks for bar and pie chart options
     html.Div(children=[
         
        html.Div([
            html.H3('Bar Chart Options:'),
            dcc.RadioItems(
                options=[
                    {'label': 'Region', 'value': 'Region'},
                    {'label': 'Gender', 'value': 'Gender'},
                    {'label': 'Origin of Wealth', 'value': 'Self Made'},
                    {'label': 'Industry', 'value': 'Industry'}],
                    value='Region', id='bar_radio_x')
            ],style={'display': 'inline-block', 'width':'50%', 'border':'1px #bbcecc solid', 'padding':'5px', 'margin': '20px', 'color':'#00838F', 'background' : '#d8ebeb'}),
        
        html.Div([
            html.H3('Pie Chart Options:'),
            dcc.RadioItems(
                options=[
                    {'label': 'Region', 'value': 'Region'},
                    {'label': 'Gender', 'value': 'Gender'},
                    {'label': 'Origin of Wealth', 'value': 'Self Made'},
                    {'label': 'Industry', 'value': 'Industry'}],
                    value='Gender', id='pie_radio')
            ],style={'display': 'inline-block', 'width':'50%', 'border':'1px #bbcecc solid', 'padding':'5px', 'margin': '20px', 'color':'#00838F', 'background' : '#d8ebeb'}),
        
    ],style={"display": "flex"}),
    ### End fourth row

    ### Begin fifth row
html.Div(children=[
        
        html.Div([
            html.H3('Bar Chart'),
            dcc.Graph(figure=fig,
              id='barchart',
              style={'width' : '95%', 'align-items' : 'center', 'background':'#00838F'})
        ],style={'display': 'inline-block', 'width':'50%', 'border':'1px #bbcecc solid', 'padding':'10px', 'margin': '20px', 'color':'#00838F', 'background' : '#d8ebeb'}),

        html.Div([
            html.H3('Pie Chart'),
            dcc.Graph(figure=fig2,
              id='piechart',
              style={'width' : '95%', 'align-items' : 'center'})
        ],style={'display': 'inline-block', 'width':'50%', 'border':'1px #bbcecc solid', 'padding':'10px', 'margin': '20px', 'color':'#00838F', 'background' : '#d8ebeb'}),

    ],style={"display": "flex"}),
    ### End fifth row
    
    ### Main Data Table
    #dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], id='table_all'),
html.Div(generate_table(df),  
                id='table_all',
                style={'margin': '20px', 'padding':'15px', 'border':'2px #ffa700 solid',}),

    ### References
html.Div(children=[
        html.Div([
            html.H3('References:'),
            html.A('1) Plotly Components',
            href='https://dash.plotly.com/dash-core-components',
            target='_blank'),
            html.Br(),
            html.A('2) Plotly Bar and Pie Chart',
            href='https://plotly.com/python/basic-charts/',
            target='_blank'),
            html.Br(),
            html.A('3) Luke Cherveny - Lesson Materials and Slides',
            href='http://lukecherveny.com/ma705fall22/index.html',
            target='_blank'),
            html.Br(),
            html.A('4) Data is Plural - Data Research',
            href='https://www.data-is-plural.com/archive/',
            target='_blank'),
            html.Br(),
            html.A('5) Initial Source of Raw Data and Background',
            href='https://www.piie.com/publications/working-papers/origins-superrich-billionaire-characteristics-database?ResearchID=2917',
            target='_blank')
        ],style={'display': 'inline-block', 'width':'98%', 'border':'1px #bbcecc solid', 'padding':'2px', 'margin': '20px', 'color':'#00838F', 'background' : '#d8ebeb'})
            ])
])

    ### Callback and Interactive Items
@app.callback(
    Output(component_id='table_all', component_property='children'),
    Input(component_id='year_dropdown', component_property='value')
    )

def update_table_year(years):
    t = df[df.Year == (years)].sort_values('Rank')
    return generate_table(t)

@app.callback(
    Output(component_id='barchart', component_property='figure'),
    Input(component_id='year_dropdown', component_property='value'),
    Input(component_id='bar_radio_x', component_property='value')
    )

def update_bar(years, attribute):
    b1 = df[df.Year == years]
    fig = px.bar(b1, x=attribute, y='Count', color=attribute, color_discrete_sequence=px.colors.qualitative.G10, title=years)
    return fig

@app.callback(
    Output(component_id='piechart', component_property='figure'),
    Input(component_id='year_dropdown', component_property='value'),
    Input(component_id='pie_radio', component_property='value')
    )

def update_pie(years, variable):
    p1 = df[df.Year == years]
    fig2 = px.pie(p1, values='Count', names=variable, hole=.3, color_discrete_sequence=px.colors.qualitative.G10, title=years)
    return fig2

if __name__ == '__main__':
    app.run_server(debug=True)
