import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib


dataset = pd.read_csv('C:/Users/Admin/Desktop/6th Sem/Project/IoT/Music Fit/datasets/data_moods.csv')


df = dataset['mood'].map({'Happy': 0, 'Sad': 0, 'Energetic': 1, 'Calm':2})
# target_names = ['Happy', 'Sad', 'Energetic', 'Calm']

dataset = dataset.drop('mood',axis = 1)
dataset = dataset.join(df) 


dataset=dataset.drop(dataset.columns[[0,1,2,3,4,5,6,10,15,16,17]], axis=1)
dataset=dataset[['energy', 'danceability', 'loudness', 'liveness', 'valence', 'acousticness', 'speechiness', 'mood']]

X = dataset.iloc[:,0:7].values
y = dataset.iloc[:,7].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 101)

# scaler = StandardScaler()
# X_train = scaler.fit_transform(X_train)
# X_test = scaler.transform(X_test)

classifier = RandomForestClassifier() 
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)
print(accuracy_score(y_test, y_pred))

joblib.dump(classifier, 'C:/Users/Admin/Desktop/6th Sem/Project/IoT/Music Fit/models/newrandomforestmodel.pkl') 

