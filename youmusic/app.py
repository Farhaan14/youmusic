import random
from flask import Flask, render_template, request, redirect, url_for
from songRecommender import *
from moodAnalyzer import *

counter = -1

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

sequence = [
    'How are your companions getting together with your desires?',
    'Did you have a good day today?',
    'Did bad things happen to you today?',
    'Would you be able to quickly clarify about your day?',
    'Are there any stresses that you need to talk about?',
    'Is there something annoying you? Would you share it with me?',
]

random.shuffle(sequence)

def greeting(name):
    greetings = [
        'How are you today ' + name +'?',
        'Howdy ' + name + ' how are you feeling?',
        "What's up " + name +'?',
        'Greetings ' + name +', are you well?',
        'How are things going ' + name +'?'
    ]
    return greetings[random.randint(0, len(greetings)-1)]

def goodbye(name):
    goodbyes = [
	'Good talking to you ' + name + 'I gotta go now',
	'Goodbye ' + name + ' I gotta go now',
    'It was pleasant conversing with you. You can talk with me whenever you want. Bye ' + name + '!',
    'It was extremely decent conversing with you and I trust that now you feel better subsequent to conversing with me. Best of fortunes for your future ' + name + '!'
    ]
    return goodbyes[random.randint(0, len(goodbyes)-1)]


playlist_creator = "Dimish"
playlist_id = "2tLMUKxKJXjYV79iPhQzon"

answers = []
name = ""

@app.route("/get", methods=["GET","POST"])
def chatbot_response():
    global counter
    global answers
    global name
    counter += 1
    out = counter

    msg = request.form["msg"]

    if out == 0:
        name = msg
        response = greeting(name)

    elif out > 0 and out < len(sequence):
        response = sequence[out - 1]
        answers.append(msg)

    elif out == len(sequence):
        mood = analyzeMood(answers)
        playlist_df = getRecommendations(playlist_creator, playlist_id)
        recommended_df = playlist_df[playlist_df['mood']==mood]
        response = 'Recommended Songs: '
        response += "<br/><br/><span class='song-name'>"
        responsedf = recommended_df[['track_name', 'artist']].agg(' - '.join, axis=1)
        responselist = responsedf.values.tolist()[:5]
        response += "</span><br/><span class='song-name'>".join(responselist)
        response += "</span><br/><br/>"
        response += goodbye(name)

    else:
        response = "Shutting Down"

    return response

if __name__ == "__main__":
    app.run()