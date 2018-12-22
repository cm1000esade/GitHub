#!/usr/bin/env python
# coding: utf-8

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

df = pd.read_csv("nama_10_gdp_1_Data.csv")
# drop GEO categories which contain "Euro" because they are not single country
df = df[df.GEO.str.contains("Euro") == False]

available_indicators = df['NA_ITEM'].unique()
available_countries = df['GEO'].unique()

# make drop-down boxes for the first graph (indicator-indicator)
app.layout = html.Div([
    html.Div([

        # insert the graph title
        html.Div(children="The graph with two indicator drop-down boxes and year-slider"),

        # set the first indicator drop-down box
        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                # set the available_indicator as options
                options=[{'label': i, 'value': i} for i in available_indicators],
                # initial number
                value='Gross domestic product at market prices'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                # initial number
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
            style={'width': '48%', 'display': 'inline-block'}),

        # set the second indicator drop-down box
        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                # initial number
                value='Final consumption expenditure'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                # initial number
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )],
            # set the style
            style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    # insert the graph
    dcc.Graph(id='GDP and main components'),

    # set the year-slider
    dcc.Slider(
        id='year--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        # initial number
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df['TIME'].unique()}),

    html.H1(children="""   """),

    # insert the graph title
    html.Div(children="The graph with indicator and country drop-down boxes"),

   # set the indicator drop-down box
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='indicator',
                # set the indicator
                options=[{'label': i, 'value': i} for i in available_indicators],
                # initial number
                value='Gross domestic product at market prices'
            ),
        ],
            # set the style
            style={'width': '48%', 'display': 'inline-block'}),

        # set the country drop-down box
        html.Div([
            dcc.Dropdown(
                id='country',
                options=[{'label': i, 'value': i} for i in available_countries],
                # initial number
                value='Belgium'
            )],
            # set the style
            style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    # insert the graph
    dcc.Graph(id='GDP and main components-2')
])


@app.callback(
    dash.dependencies.Output('GDP and main components', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('year--slider', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['TIME'] == year_value]

    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log',
                'rangemode': 'tozero'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log',
                'rangemode': 'nonnegative'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }


@app.callback(
    dash.dependencies.Output('GDP and main components-2', 'figure'),
    [dash.dependencies.Input('indicator', 'value'),
     dash.dependencies.Input('country', 'value')])

def update_graph(indicator,
                 country
                 ):
    dff = df[df['GEO'] == country]

    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == indicator]['TIME'],
            y=dff[dff['NA_ITEM'] == indicator]['Value'],
            text=dff[dff['NA_ITEM'] == indicator]['Value'],
            mode='lines+markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'year',
                'type': 'linear',
                'range': [2008, 2017]
            },
            yaxis={
                'title': indicator + " in " + country,
                'type': 'linear',
                'rangemode': 'nonnegative'
            },
            margin={'l': 50, 'b': 50, 't': 10, 'r': 10},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server()
