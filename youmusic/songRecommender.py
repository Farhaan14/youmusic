import spotipy
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time
import numpy as np
import joblib

def analyze_playlist(creator, playlist_id, sp):
    
    playlist_features_list = ["artist", "album", "track_name", "track_id", 
                             "danceability", "energy", "key", "loudness", "mode", "speechiness","acousticness",
                             "instrumentalness", "liveness", "valence", "tempo", "duration_ms", "time_signature"]
    playlist_df = pd.DataFrame(columns = playlist_features_list)
    
    playlist_features = {} 

    playlist = sp.user_playlist_tracks(creator, playlist_id)["items"]

    for track in playlist:

        playlist_features["artist"] = track["track"]["album"]["artists"][0]["name"]
        playlist_features["album"] = track["track"]["album"]["name"]
        playlist_features["track_name"] = track["track"]["name"]
        playlist_features["track_id"] = track["track"]["id"]
       

        audio_features = sp.audio_features(playlist_features["track_id"])[0] 
        for feature in playlist_features_list[4:]:
            playlist_features[feature] = audio_features[feature]

        track_df = pd.DataFrame(playlist_features, index = [0])
        playlist_df = pd.concat([playlist_df, track_df], ignore_index = True)
        
    return playlist_df

def get_track_features(id, sp):
    meta = sp.track(id)
    album_cover = meta['album']['images'][0]['url']
    track_info = [album_cover]
    return track_info

def getRecommendations(artist_id, playlist_id):
    auth_manager = SpotifyClientCredentials(
        client_id = 'f6343bebebba4e3a84520d2cb79a53e8',
        client_secret = 'ad836bec7b934b94b0b298e70f7f9ec0'
        )
    sp = spotipy.Spotify(auth_manager=auth_manager)

    playlist_df = analyze_playlist(artist_id, playlist_id, sp)

    track_id=[]

    for i in range(len(playlist_df)) :
        track_id.append(playlist_df.iloc[i, 3])

    track_img=[]
    for i in range(len(track_id)) :
        track_img.append(get_track_features(track_id[i], sp))

    df2=pd.DataFrame(track_img)
    df2.columns=['image']

    playlist_df = playlist_df.join(df2)

    playlist_df=playlist_df.drop(playlist_df.columns[[1, 3, 6, 8, 11, 14, 15, 16]], axis=1)
    playlist_df = playlist_df[["artist","track_name","image" ,"energy",	"danceability",	"loudness",	"liveness",	"valence",	"acousticness",	"speechiness"]]

    playlist_df.danceability=playlist_df.danceability.astype(float)
    playlist_df.energy=playlist_df.energy.astype(float)
    playlist_df.liveness=playlist_df.liveness.astype(float)
    playlist_df.valence=playlist_df.valence.astype(float)
    playlist_df.loudness=playlist_df.loudness.astype(float)
    playlist_df.speechiness=playlist_df.speechiness.astype(float)
    playlist_df.acousticness=playlist_df.acousticness.astype(float)

    joblib_file = "C:/Users/Admin/Desktop/6th Sem/Project/IoT/Music Fit/models/newrandomforestmodel.pkl"  
    joblib_model = joblib.load(joblib_file)

    final_song=[]
    for n in range(len(playlist_df)):
        arr=playlist_df.iloc[n].to_numpy()
        tarr=list(arr)
        X_test=[tarr[3:]]
        y_pred = joblib_model.predict(X_test)
        final_song.append(y_pred)

    df3 = pd.DataFrame(final_song)
    df3.columns=['mood']
    playlist_df = playlist_df.join(df3)

    return playlist_df