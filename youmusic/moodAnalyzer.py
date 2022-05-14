import lettria

api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhbmFseXRpY0lkIjoiNjI2OGY5ZjUzMzY4MmUwMDI4NzJlOTI1IiwicHJvamVjdElkIjoiNjI2OGY5ZjUzMzY4MmUwMDI4NzJlOTI3Iiwic3Vic2NyaXB0aW9uSWQiOiI2MjY4ZjllMjE3NGE3MDAwMzVhMGI1ZjYiLCJpYXQiOjE2NTEwNDY5NzUsImV4cCI6MTY5OTQzMDk3NX0.xVb03qzvsmTbXysULJjo57IKHce5rCraHoRlpmxlQwI'
nlp = lettria.NLP(api_key)

def analyzeMood(sentence):

    nlp.add_document(sentence)

    get_emotion = nlp.get_emotion
    allsemotion = [s.emotion for s in nlp.subsentences][0]

    result1 = next((i for i, v in enumerate(allsemotion) if v[0] == "happiness"), None)
    result2 = next((i for i, v in enumerate(allsemotion) if v[0] == "sadness"), None)


    if result1 != None:
        happiness = allsemotion[result1][1]
    else:
        happiness = 0
    if result2 != None:
        sadness = allsemotion[result2][1]
    else:
        sadness = 0

    if sadness > happiness:
        mood = 1

    elif happiness > sadness:
        mood = 2

    else:
        mood = 0

    return mood 
 