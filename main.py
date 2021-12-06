from flask import Flask, request
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from collections import deque
import dash_bootstrap_components as dbc
from dash import State
from flask_restful import Resource, Api


SENSOR_VALUE = 0
valQueue = deque(maxlen=20)
timeQueue = deque(maxlen=20)

FLASK_SERVER = Flask(__name__)
api = Api(FLASK_SERVER)
app = dash.Dash(server=FLASK_SERVER)


class WSN(Resource):
    def get(self, value):
            return '{}sensor'.format(valQueue[-1])
        
    def post(self, value):
        global SENSOR_VALUE
        SENSOR_VALUE = float(value)
        return '{} is written'.format(SENSOR_VALUE)

api.add_resource(WSN, '/<string:value>')


app.layout =  html.Div( children=[
    html.H1("smart home"),
    dcc.Graph(id='graphwheredraw', animate=True),
                          dcc.Interval(id='timeevent',interval=4000)
                         ])                        
                        

@app.callback(Output('graphwheredraw', 'figure'),
              [Input('timeevent', 'n_intervals')])
def update_graph_scatter(input_data):
    import datetime
    x = datetime.datetime.now()
    timeQueue.append(x)
    valQueue.append(SENSOR_VALUE)    
    ans = {'data': [{ 'x': list(timeQueue), 'y': list(valQueue),'mode':'lines+markers'}],
           'layout':go.Layout(
                plot_bgcolor="#000000",
                xaxis=dict(range=[min(timeQueue),max(timeQueue)],linecolor="#ffffff"),
                yaxis=dict(range=[min(valQueue),max(valQueue)],linecolor="#ffffff")
            )
           }
    return ans
app.run_server()
