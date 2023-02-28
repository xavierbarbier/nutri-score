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
    html.Div([
        html.Div([          
            html.Img(src="https://get.apicbase.com/wp-content/uploads/2020/08/nutriscore-logo.png",
            style={ 'height':'30%', 'width':'30%'}),
            html.H5('Prédiction Nutri-Score'),
            html.Plaintext('By Xavier Barbier - @xavbarbier'),

    
           
        ], className="three columns"),

  # col 2
  html.Div([
            
      html.Div(id='kcal-output-container'),
    
    dcc.Dropdown(
       np.arange(0,900,1),
       450,
       id='kcal-slider',
          
    ),


    html.Div(id='prot-output-container'),
    
    dcc.Dropdown(
       np.arange(0,100,1),
       50,
       id='prot-slider'
        
    ),
    
    html.Div(id='glu-output-container'),

    dcc.Dropdown(
       np.arange(0,100,1),
       50,
       id='glu-slider'
       
    ),
    
    html.Div(id='sugar-output-container'),

    dcc.Dropdown(
       np.arange(0,100,1),
       50,
       id='sugar-slider'

    ),

       html.Div(id='fat-output-container'),

    dcc.Dropdown(
       np.arange(0,100,1),
       50,
       id='fat-slider'
        
    ),

    html.Div(id='sat-output-container'),

    dcc.Dropdown(
       np.arange(0,100,1),
       50,
       id='sat-slider'
        
    ),

    html.Div(id='salt-output-container'),

    dcc.Dropdown(
       np.arange(0,100,1),
       50,
       id='salt-slider'
    ),
    
            
        ], className="four columns"),
        

  # col 3
        html.Div([
            
 
    html.Button('Submit', id='submit-val', n_clicks=0),

    html.Div(id='container-button-basic',
             children='Enter a value and press submit')
    
            
        ], className="four columns"),
        ], className="row")
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
    total =  fat  + glu +  prot + salt
    
    if total > 100:
      return html.Div([ html.Plaintext('Erreur de saisie : '),
                       html.Plaintext('total des informations nutritionnelles pour 100g > 100')])
    
    if sat > fat:
      return html.Div([ html.Plaintext('Erreur de saisie : graisses saturées > graisses')])

    if sugar > glu:
      return html.Div([ html.Plaintext('Erreur de saisie : sucres > glucides')])

    else :
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
        return html.Div([
                html.Img(src="https://raw.githubusercontent.com/xavierbarbier/nutri-score/main/img/Nutri-score-a.png", width=255),
                html.Plaintext('Prédiction faite sur la base de 242 710 exemples.'),
                html.Plaintext('Précision de 80%'),
                html.Plaintext('Données: Open Food Facts'),
                dcc.Link('https://fr.openfoodfacts.org/ ', href='https://fr.openfoodfacts.org/ ' , target='_blank')])
        
        

      if pred == "b":
        return html.Div([
                html.Img(src="https://raw.githubusercontent.com/xavierbarbier/nutri-score/main/img/Nutri-score-b.png", width=255),
                html.Plaintext('Prédiction faite sur la base de 242 710 exemples.'),
                html.Plaintext('Précision de 80%'),
                html.Plaintext('Données: Open Food Facts'),
                dcc.Link('https://fr.openfoodfacts.org/ ', href='https://fr.openfoodfacts.org/ ' , target='_blank')])
        
        

      if pred == "c":
        return html.Div([
                html.Img(src="https://raw.githubusercontent.com/xavierbarbier/nutri-score/main/img/nutri-score-c.jpg", width=255),
                html.Plaintext('Prédiction faite sur la base de 242 710 exemples.'),
                html.Plaintext('Précision de 80%'),
                html.Plaintext('Données: Open Food Facts'),
                dcc.Link('https://fr.openfoodfacts.org/ ', href='https://fr.openfoodfacts.org/ ' , target='_blank')])
        
        

      if pred == "d":
        return html.Div([
                html.Img(src="https://raw.githubusercontent.com/xavierbarbier/nutri-score/main/img/nutri-score-d.png", width=255),
                html.Plaintext('Prédiction faite sur la base de 242 710 exemples.'),
                html.Plaintext('Précision de 80%'),
                html.Plaintext('Données: Open Food Facts'),
                dcc.Link('https://fr.openfoodfacts.org/ ', href='https://fr.openfoodfacts.org/ ' , target='_blank')])

        

      if pred == "e":
        return html.Div([
                html.Img(src="https://raw.githubusercontent.com/xavierbarbier/nutri-score/main/img/Nutri-Score-e.jpg", width=255),
                html.Plaintext('Prédiction faite sur la base de 242 710 exemples.'),
                html.Plaintext('Précision de 80%'),
                html.Plaintext('Données: Open Food Facts'),
                dcc.Link('https://fr.openfoodfacts.org/ ', href='https://fr.openfoodfacts.org/ ' , target='_blank')])


