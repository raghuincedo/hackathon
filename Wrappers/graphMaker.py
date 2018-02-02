# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

class Graphs:
    def __init__(self):
        pass
    def histogram(self, title, x_label, y_label, X, Y):
        app = dash.Dash()
        app.layout = html.Div(children=[
            html.H1(children='Hello Dash'),

            html.Div(children='''
                Dash: A web application framework for Python.
            '''),

            dcc.Graph(
                id='example-graph',
                figure={
                    'data': [
                        {'x': X, 'y': Y, 'type': 'bar', 'name': 'SF'},
                        {'x': X, 'y': Y, 'type': 'bar', 'name': u'Montréal'},
                    ],
                    'layout': {
                        'title': title
                    }
                }
            )
        ])
        if __name__ == '__main__':
            app.run_server(debug=True)


    def histogram2(self, title, x_label, y_label, X, Y):
        app = dash.Dash()
        app.layout = html.Div(children=[
            html.H1(children='Hello Dash'),

            html.Div(children='''
                Dash: A web application framework for Python.
            '''),

            dcc.Graph(
                id='example-graph',
                figure={
                    'data': [
                        {'x': X, 'y': Y, 'type': 'bar', 'name': 'SF'},
                        {'x': X, 'y': Y, 'type': 'bar', 'name': u'Montréal'},
                    ],
                    'layout': {
                        'title': title
                    }
                }
            )
        ])
        app.run_server(debug=True)

    def showData(self, df):
        def generate_table(dataframe, max_rows=10):
            return html.Table(
                # Header
                [html.Tr([html.Th(col) for col in dataframe.columns])] +

                # Body
                [html.Tr([
                    html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
                ]) for i in range(min(len(dataframe), max_rows))]
            )

        app = dash.Dash()

        app.layout = html.Div(children=[
            html.H4(children='Sample Data'),
            generate_table(df)
        ])
        app.run_server(debug=True)

    def pieChart(self):
        from dash.dependencies import Input, Output, State

        app = dash.Dash()

        def app_layout():
            return (
                html.Div([
                    dcc.Tabs(
                        tabs=[{'label': 'Pie1', 'value': 1},
                              {'label': 'Pie2', 'value': 2},
                              {'label': 'Pie3', 'value': 3},
                              {'label': 'Pie4', 'value': 4}
                              ],
                        value=1,
                        id='tabs'
                    ),
                    html.Div(id='output-tab')
                ])
            )

        app.layout = app_layout()

        @app.callback(Output('output-tab', 'children'),
                      [Input('tabs', 'value')])
        def display_content(value):
            data = [
                {
                    'values': [[10, 90], [5, 95], [15, 85], [20, 80]][int(value) - 1],
                    'type': 'pie',
                },
            ]

            return html.Div([
                dcc.Graph(
                    id='graph',
                    figure={
                        'data': data,
                        'layout': {
                            'margin': {
                                'l': 30,
                                'r': 0,
                                'b': 30,
                                't': 0
                            },
                            'legend': {'x': 0, 'y': 1}
                        }
                    }
                )
            ])

        #if __name__ == '__main__':
        app.server.run(debug=True)

    def scatterPlot(self, X, y):
        app = dash.Dash()

        app.scripts.config.serve_locally = True

        app.layout = html.Div([
            dcc.Tabs(
                tabs=[
                    {'label': 'Tab {}'.format(i), 'value': i} for i in range(1, 5)
                ],
                value=3,
                id='tabs'
            ),
            html.Div(id='tab-output')
        ], style={
            'width': '80%',
            'fontFamily': 'Sans-Serif',
            'margin-left': 'auto',
            'margin-right': 'auto'
        })

        @app.callback(Output('tab-output', 'children'), [Input('tabs', 'value')])
        def display_content(value):
            data = [
                {
                    'x': X,
                    'y': y,
                    'name': 'x',
                    'marker': {
                        'color': 'rgb(55, 83, 109)'
                    },
                    'type': ['bar', 'scatter', 'box'][int(value) % 3]
                },
                {
                    'x': X,
                    'y': y,
                    'name': '',
                    'marker': {
                        'color': 'rgb(26, 118, 255)'
                    },
                    'type': ['bar', 'scatter', 'box'][int(value) % 3]
                }
            ]

            return html.Div([
                dcc.Graph(
                    id='graph',
                    figure={
                        'data': data,
                        'layout': {
                            'margin': {
                                'l': 30,
                                'r': 0,
                                'b': 30,
                                't': 0
                            },
                            'legend': {'x': 0, 'y': 1}
                        }
                    }
                ),
                #html.Div(' '.join(get_sentences(10)))
            ])


        app.run_server(debug=True)

#x = [1, 2, 3]
#y= [4, 1, 2]
#obj = Graphs()
#obj.histogram2("sample", "x-axis", "y-axis", x, y)
#x = list(action3(action_type3, filtered_data))[-20:]

#obj = Graphs()
#obj.scatterPlot(list(x))

