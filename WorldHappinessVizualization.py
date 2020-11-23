import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots


fig = go.Figure()

# Load CSV file from Datasets folder
df1 = pd.read_csv('2018.csv')

# Choropleth
fig = go.Figure(data=go.Choropleth(
    locationmode='country names',
    locations=df1['Country'],
    z=df1['Score'],
    text=df1['Country'],
    colorscale='sunset',
    autocolorscale=False,
    reversescale=True,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_title='Happiness Score',
))
# Choropleth

fig.update_layout(
    title_text='2018 World Happiness',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    annotations=[dict(
        x=0.55,
        y=0.1,
        xref='paper',
        yref='paper',
        text='Source: <a href="https://www.kaggle.com/unsdsn/world-happiness">\
                World Happiness Report</a>',
        showarrow=False
    )]
)
app = dash.Dash()


YEARS = [2018, 2019]
# Layout of the Dashboard
app.layout = html.Div(children=[
    html.H1(children='World Happiness Dash',
            style={
                'textAlign': 'center',
                'color': '#C70039',
                'font-family': 'Courier New'
            }
            ),
    # Title of the Website at the top
    html.Div('Web dashboard for Data Visualization of World Happiness', style={'textAlign': 'center',   'font-family': 'Courier New'}),
    # Subtitle at the top
    html.Div('World Happiness Based by Region', style={'textAlign': 'center', 'font-family': 'Courier New'}),
    html.Br(),
    html.Br(),
    html.Hr(style={'border-top': 'dashed #C70039'}),

    # Having the Cholorpleth show on the dash board
    html.H3('Cloropleth Chart', style= {'font-family': 'Courier New'}),
    html.Div('This shows a world overview of happiness scores', style= {'font-family': 'Courier New'}),
    dcc.Graph(id="Choropleth", figure=fig, style={'height': '%50', 'width': '%100'}), # more room for map

    # Start of Interactive Bar Chart Start
    html.H3('Interactive Bar chart', style= {'font-family': 'Courier New'}),
    html.Div('This bar chart represent the reported world happiness by region and year as well as '
             'what contributed to the score', style= {'font-family': 'Courier New'}),
    # Creating the Interactive Bar Chart onto the dash board
    dcc.Graph(id='graph1', style={'background': '#544F4F'}),
    # Drop down box title
    html.Div('Please select a region', style={'color': '#000000', 'margin': '10px', 'font-family': 'Courier New'}),
    # Dropdown Menu for Stacked Bar Chart
    dcc.Dropdown(
        style= {'font-family': 'Courier New'},
        id='select-region',
        options=[
            {'label': 'Australia and New Zealand', 'value': 'Australia and New Zealand'},
            {'label': 'Central and Eastern Europe', 'value': 'Central and Eastern Europe'},
            {'label': 'Eastern Asia', 'value': 'Eastern Asia'},
            {'label': 'Latin America and Caribbean', 'value': 'Latin America and Caribbean'},
            {'label': 'Middle East and Northern Africa', 'value': 'Middle East and Northern Africa'},
            {'label': 'North America', 'value': 'North America'},
            {'label': 'Southeastern Asia', 'value': 'Southeastern Asia'},
            {'label': 'Southern Asia', 'value': 'Southern Asia'},
            {'label': 'Sub-Saharan Africa', 'value': 'Sub-Saharan Africa'},
            {'label': 'Western Europe', 'value': 'Western Europe'}
        ],
        value='Central and Eastern Europe'
    ),
    # Slider
    html.Div(
        id="left-column",
        children=[
            html.Div(
                id="slider-container",
                children=[
                    html.P(
                        style= {'font-family': 'Courier New'},
                        id="slider-text",
                        children="Drag the slider to change the year:",
                    ),
                    dcc.Slider(
                        id="years-slider",
                        updatemode='mouseup',
                        min=min(YEARS),
                        max=max(YEARS),
                        value=min(YEARS),
                        marks={
                            str(year): {
                                "label": str(year),
                                "style": {"color": "#000000"},
                            }
                            for year in YEARS
                        },
                    ),
                ],
            ),
        ],
    ),

])


# Call Back to change the Stacked Bar Chart
@app.callback(Output('graph1', 'figure'),
              [Input('select-region', "value"),
               Input('years-slider', "value")])
def update_figure(selected_region, selected_year):
    if selected_year == 2018:
        new_df = pd.read_csv('2018.csv')
    else:
        new_df = pd.read_csv('2019.csv')

    stackbarchart_df = new_df[new_df['Region'] == selected_region]

    stackbarchart_df = stackbarchart_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    stackbarchart_df = stackbarchart_df.groupby(['Country']).agg(
        {'Overall rank': 'sum', 'GDP per capita': 'sum', 'Social support': 'sum',
         'Healthy life expectancy': 'sum', 'Freedom to make life choices': 'sum', 'Generosity': 'sum',
         'Perceptions of corruption': 'sum'}).reset_index()

    stackbarchart_df = stackbarchart_df.sort_values(by=['Overall rank'], ascending=[False]).reset_index()

    trace1_stackbarchart = go.Bar(x=stackbarchart_df['Country'], y=stackbarchart_df['GDP per capita'],
                                  name='Economy', marker={'color': '#7B0000'})

    trace2_stackbarchart = go.Bar(x=stackbarchart_df['Country'], y=stackbarchart_df['Social support'],
                                  name='Social support', marker={'color': '#D53C00'})

    trace3_stackbarchart = go.Bar(x=stackbarchart_df['Country'], y=stackbarchart_df['Healthy life expectancy'],
                                  name='Healthy life expectancy', marker={'color': '#FF8700'})

    trace4_stackbarchart = go.Bar(x=stackbarchart_df['Country'], y=stackbarchart_df['Freedom to make life choices'],
                                  name='Freedom', marker={'color': '#F5BD1F'})

    trace5_stackbarchart = go.Bar(x=stackbarchart_df['Country'], y=stackbarchart_df['Generosity'],
                                  name='Generosity',
                                  marker={'color': '#FFD93D'})

    trace6_stackbarchart = go.Bar(x=stackbarchart_df['Country'], y=stackbarchart_df['Perceptions of corruption'],
                                  name='Perceptions of corruption', marker={'color': '#EDFF74'})

    data_stackbarchart = [trace1_stackbarchart, trace2_stackbarchart, trace3_stackbarchart, trace4_stackbarchart,
                          trace5_stackbarchart, trace6_stackbarchart]

    return {'data': data_stackbarchart, 'layout': go.Layout(title='Happiness Scores in ' + selected_region + " in year " + str(selected_year),
                                                            xaxis={'title': 'Country'},
                                                            yaxis={'title': 'Happiness Overall'},
                                                            barmode='stack')}


# This is to update the choropleth
@app.callback(Output('Choropleth', 'figure'),
              [Input('years-slider', "value")])
def update_Choropleth(selected_year):
    # Adjusts the DF for the data
    if selected_year == 2018:
        new_df = pd.read_csv('2018.csv')
    else:
        new_df = pd.read_csv('2019.csv')

    # Generates new Figure
    fig = go.Figure(data=go.Choropleth(
        locationmode='country names',
        locations=new_df['Country'],
        z=new_df['Score'],
        text=new_df['Country'],
        colorscale='sunset',
        autocolorscale=False,
        reversescale=True,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title='Happiness Score',
    ))

    # Changes the layout of the Choropleth
    fig.update_layout(
        height=1000, # height for map, makes it scale larger
        title_text= str(selected_year) + ' World Happiness',
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        ),
        annotations=[dict(
            x=0.55,
            y=0.1,
            xref='paper',
            yref='paper',
            text='Source: <a href="https://www.kaggle.com/unsdsn/world-happiness">\
                World Happiness Report</a>',
            showarrow=False
        )]
    )

    # This large return may actually update the choropleth
    return fig


if __name__ == '__main__':
    app.run_server()
fig.show()
