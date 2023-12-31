# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YDR42_qv51QKL5CD1yyEvGU7VS3SI4JL
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd

df_alim = pd.read_csv('/content/drive/MyDrive/Epsi/Atelier composants métier/Projet/export_alimconfiance@dgal.csv', sep=';')

df_alim.shape

df_alim.head()

df_alim.columns

df_alim[['filtre', 'ods_type_activite']]

df_alim.head()

import matplotlib.pyplot as plt

#set(df_alim['APP_Libelle_activite_etablissement'].values)

from collections import Counter
count = Counter(df_alim['APP_Libelle_activite_etablissement'])

count.most_common()

count.most_common()[0][1]

list_etab = [x[0] for x in count.most_common() if x[1] > 100]

df_alim = df_alim[df_alim['APP_Libelle_activite_etablissement'].isin(list_etab)].reset_index()

df_alim.to_csv('/content/drive/MyDrive/Epsi/Atelier composants métier/Projet/data_formated.csv', index=False)

df_alim.columns

df_alim.dtypes

from datetime import datetime
import pytz

def convert_to_timestamp(dt):
  date_time_str = dt

  date_time_obj = datetime.fromisoformat(date_time_str)

  timestamp = date_time_obj.timestamp()

  return timestamp

#df_alim['Date_inspection'] = df_alim.apply

list_date = list(df_alim['Date_inspection'].values)

timestamps = []

for dt in list_date:
  timestamp = convert_to_timestamp(dt)
  timestamps.append(timestamp)

df_alim['Date_inspection_timestamp'] = timestamps

df_alim.Date_inspection_timestamp = df_alim.Date_inspection_timestamp.astype(int)

#Labelisation des valeurs

from sklearn.preprocessing import LabelEncoder

label_encoder = LabelEncoder()

# Encoder la chaîne de caractère
df_alim['Synthese_eval_sanit'] = label_encoder.fit_transform(df_alim['Synthese_eval_sanit'])

df_alim['APP_Libelle_activite_etablissement'] = label_encoder.fit_transform(df_alim['APP_Libelle_activite_etablissement'])
df_alim['Libelle_commune'] = label_encoder.fit_transform(df_alim['Libelle_commune'])

X = df_alim[['APP_Libelle_activite_etablissement','Libelle_commune', 'Date_inspection_timestamp']]
y = df_alim[['Synthese_eval_sanit']]

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

#Division de notre jeu de données en jeu d'entraînement et de test
train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)

from sklearn.ensemble import RandomForestClassifier

#Utilisation du Random Forest Classifier pour de la classification
rf_model = RandomForestClassifier(random_state = 100)


rf_model.fit(train_X, train_y)

#On test les performances de notre modèle avec les données de test
results_predicted = rf_model.predict(val_X)

#Validation du modèle
print("Accuracy:",round(accuracy_score(val_y, results_predicted),2))
print("Precision:",round(precision_score(val_y, results_predicted, average='weighted'),2))
print("Recall:",round(recall_score(val_y, results_predicted, average='weighted'),2))
print("F1:",round(f1_score(val_y, results_predicted, average='weighted'),2))