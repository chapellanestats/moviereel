from flask import Flask, render_template
from flask_frozen import Freezer
import requests
from bs4 import BeautifulSoup, SoupStrainer
import json
import pandas as pd
from datetime import date

app = Flask(__name__)

@app.route('/')
def get_moviedata():
    url = "https://www.eventcinemas.com.au/Cinemas/GetSessions"
    today = str(date.today())
    querystring = {"cinemaIds":["53","55","62","66","69"],"date":today}
    payload = ""
    headers = {
        "cookie": "__cf_bm=6cuxt7M_6J5h9YgmPd0503L.ShNfymDkV.N_YNdZsCw-1646572465-0-AY7fmfCnjR3r4jEisapMAKumoubEeOCfFXgL8aqOyYe9gTTg7wFE9GfuP3R92QdvFx9MTv%2FmpnKsHFgUnxlf5og%3D",
        "authority": "www.eventcinemas.com.au",
        "pragma": "no-cache",
        "cache-control": "no-cache",
        "sec-ch-ua": "^\^",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    }
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    jsondata = json.loads(response.text)
    number = (len([item['Name'] for item in jsondata['Data']['Movies']])) 
    testlist = []
    for x in range(0,number):
        base1 = jsondata['Data']['Movies'][x]
        Moviename = base1['Name']
        Movieruntime = base1['RunningTime']
        FirstShowing = base1['FirstSession']
        LastShowing = base1['LastSession']
        length = len([cinema['Name'] for cinema in base1['CinemaModels']])
        #print("Movie:", Moviename)
        info = base1['CinemaModels']
        for cinema in info:
            Locations = cinema['Name']
            #print("Showing at:",Locations)
            for tool in cinema['Sessions']:
                StartTime = tool['StartTime'][-5:]
                Screentype = tool['ScreenType']
                Availability = tool['SeatsAvailable']
                #print("Movie commences at:", StartTime, "Movie is in:", Screentype, "There are", Availability, "seats available currently")
                movieinformation = {
                    'Movie': Moviename,
                    'MovieLength': Movieruntime,
                    'Location': Locations,
                    'Starts': StartTime,
                    'CinemaType': Screentype,
                    'SeatsRemain': Availability
                }
                testlist.append(movieinformation)    
    df = pd.DataFrame(testlist)
    print(df.head(10))
    values = df.values
    headings = df.columns
    return render_template('index.html', headings=headings, data=values)

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()
