import io
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import base64
import pandas as pd
import joblib
import os
import numpy as np
from sklearn import neighbors
from sklearn.preprocessing import LabelEncoder
from sklearn import model_selection
from sklearn import preprocessing


model = joblib.load("nutriscore_knn_model.pkl")
model = model.best_estimator_

labelencoder = joblib.load("labelencoder.pkl")

std_scale = joblib.load("std_scale.pkl")

cols = ['energy_kcal_100g', 'fat_100g', 'saturated_fat_100g',
       'carbohydrates_100g', 'sugars_100g', 'proteins_100g', 'salt_100g']

temp = pd.DataFrame(columns=cols)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.H4('Prédiction Nutri-Score'),
    html.Plaintext('By Xavier Barbier - @xavbarbier'),

    html.Div(id='kcal-output-container'),
    
    dcc.Slider(
        id='kcal-slider',
        min=0,
        max=900,
        step=1,
        value=450,
    ),


    html.Div(id='prot-output-container'),
    
    dcc.Slider(
        id='prot-slider',
        min=0,
        max=100,
        step=1,
        value=50,
    ),
    
    html.Div(id='glu-output-container'),

    dcc.Slider(
        id='glu-slider',
        min=0,
        max=100,
        step=1,
        value=50,
    ),
    
    html.Div(id='sugar-output-container'),

    dcc.Slider(
        id='sugar-slider',
        min=0,
        max=100,
        step=1,
        value=50,
    ),

    html.Div(id='fat-output-container'),

    dcc.Slider(
        id='fat-slider',
        min=0,
        max=100,
        step=1,
        value=50,
    ),

    html.Div(id='sat-output-container'),

    dcc.Slider(
        id='sat-slider',
        min=0,
        max=100,
        step=1,
        value=50,
    ),

    html.Div(id='salt-output-container'),

    dcc.Slider(
        id='salt-slider',
        min=0,
        max=100,
        step=1,
        value=50,
    ),

    html.Button('Submit', id='submit-val', n_clicks=0),
    html.Div(id='container-button-basic',
             children='Enter a value and press submit')
])

@app.callback(
    dash.dependencies.Output('prot-output-container', 'children'),
    [dash.dependencies.Input('prot-slider', 'value')])
    
def update_output(value):
    return 'Proteines "{}" pour 100g '.format(value)

@app.callback(
    dash.dependencies.Output('glu-output-container', 'children'),
    [dash.dependencies.Input('glu-slider', 'value')])
    
def update_output(value):
    return 'Glucides "{}" pour 100g '.format(value)

@app.callback(
    dash.dependencies.Output('sugar-output-container', 'children'),
    [dash.dependencies.Input('sugar-slider', 'value')])
    
def update_output(value):
    return 'Dont sucres "{}" pour 100g '.format(value)

@app.callback(
    dash.dependencies.Output('fat-output-container', 'children'),
    [dash.dependencies.Input('fat-slider', 'value')])
    
def update_output(value):
    return 'Graisses "{}" pour 100g '.format(value)

@app.callback(
    dash.dependencies.Output('sat-output-container', 'children'),
    [dash.dependencies.Input('sat-slider', 'value')])
    
def update_output(value):
    return 'Dont graisses saturées "{}" pour 100g '.format(value)

@app.callback(
    dash.dependencies.Output('salt-output-container', 'children'),
    [dash.dependencies.Input('salt-slider', 'value')])
    
def update_output(value):
    return 'Sel "{}" pour 100g '.format(value)

@app.callback(
    dash.dependencies.Output('kcal-output-container', 'children'),
    [dash.dependencies.Input('kcal-slider', 'value')])
    
def update_output(value):
    return 'Kcal "{}" pour 100g '.format(value)

@app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Input('submit-val', 'n_clicks')],
    [dash.dependencies.Input('kcal-slider', 'value')],
    [dash.dependencies.Input('fat-slider', 'value')],
    [dash.dependencies.Input('sat-slider', 'value')],
    [dash.dependencies.Input('glu-slider', 'value')],
    [dash.dependencies.Input('sugar-slider', 'value')],
    [dash.dependencies.Input('prot-slider', 'value')],      
    [dash.dependencies.Input('salt-slider', 'value')])

def update_output(n_clicks, kcal, fat, sat, glu, sugar, prot, salt):
  changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
  if 'submit-val' in changed_id:         

      temp["energy_kcal_100g"] = [kcal]
      temp["proteins_100g"] = [prot]
      temp["carbohydrates_100g"] = [glu]
      temp["sugars_100g"] = [sugar]
      temp["fat_100g"] = [fat]
      temp["saturated_fat_100g"] = [sat]
      temp["salt_100g"] = [salt]

      X = temp.values

      temp_scaled = std_scale.transform(X)

      y_pred = model.predict(temp_scaled)

      pred = labelencoder.inverse_transform(y_pred)

      if pred == "a":
        return html.Img(src="https://raw.githubusercontent.com/xavierbarbier/nutri-score/main/img/Nutri-score-a.png", width=255)

      if pred == "b":
        return html.Img(src="https://raw.githubusercontent.com/xavierbarbier/nutri-score/main/img/Nutri-score-b.png", width=255)

      if pred == "c":
        return html.Img(src="https://raw.githubusercontent.com/xavierbarbier/nutri-score/main/img/nutri-score-c.jpg", width=255)

      if pred == "d":
        return html.Img(src="https://raw.githubusercontent.com/xavierbarbier/nutri-score/main/img/nutri-score-d.png", width=255)

      if pred == "e":
        return html.Img(src="https://raw.githubusercontent.com/xavierbarbier/nutri-score/main/img/Nutri-Score-e.jpg", width=255)


