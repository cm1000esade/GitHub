
# coding: utf-8

# The first one will be a scatterplot with two DropDown boxes for the different indicators. It will have also a slide for the different years in the data.

# In[4]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

df = pd.read_csv("nama_10_gdp_1_Data.csv")

available_indicators = df['NA_ITEM'].unique()

app.layout = html.Div([
    html.Div([

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
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='GDP and main components'),
    
    dcc.Slider(
        id='year--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        # initial number
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df['TIME'].unique()}
    )
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
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server()


# The other graph will be a line chart with two DropDown boxes, one for the country and the other for selecting one of the indicators. (hint use Scatter object using mode = 'lines' (more here)

# In[2]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

df = pd.read_csv("nama_10_gdp_1_Data.csv")

available_indicators = df['NA_ITEM'].unique()
available_countries = df["GEO"].unique()

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='indicator',
                # set the indicator
                options=[{'label': i, 'value': i} for i in available_indicators],
                # 初期値
                value='Gross domestic product at market prices'
            ),

        ],
        # 上の2つの要素をひとまとめにstyleを設定する
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='country',
                options=[{'label': i, 'value': i} for i in available_countries],
                # 初期値
                value='European Union (current composition)'
            ),

        # 上の2つの要素をひとまとめにstyleを設定する
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    # ここに出力する図を挿入する
    dcc.Graph(id='GDP and main components-2'),
    
])

@app.callback(
    dash.dependencies.Output('GDP and main components-2', 'figure'),
    [dash.dependencies.Input('country', 'value'),
     dash.dependencies.Input('indicator', 'value')
     #dash.dependencies.Input('year--slider', 'value')
    ])


def update_graph(xaxis_column_name, 
                yaxis_column_name,
                 #country,indicator
                ):
    #df1 = df[df['GEO'] == country]
    #df1 = df[(df["NA_ITEM"] == indicator) & (df["GEO"] == country)]
    #df2 = df[df["NA_ITEM"] == indicator]
    
    return {
        'data': [go.Scatter(
            x = df["TIME"].unique(),
            #x=df1[df1['NA_ITEM'] == xaxis_column_name]['TIME'],
            y=df[(df["NA_ITEM"] == xaxis_column_name) & (df["GEO"] == yaxis_column_name)]['Value'],
            text=df[df['NA_ITEM'] == yaxis_column_name]['Value'],
            mode='lines',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server()

