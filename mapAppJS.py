#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps, Map
import argparse


#get input csv file
parser = argparse.ArgumentParser()

parser.add_argument("--file", "-f", type=str, required=True)
args = parser.parse_args()



# require Flask-GoogleMaps (https://github.com/rochacbruno/Flask-GoogleMaps)
app = Flask(__name__)
api_key = 'AIzaSyAUniICLcrb9_Xjpg3Gxfi3AEkoF0ZG8iQ' # change this to your api key
# get api key from Google API Console (https://console.cloud.google.com/apis/)
GoogleMaps(app, key=api_key) # set api_key
devices_data = {} # dict to store data of devices
devices_location = {} # dict to store coordinates of devices
# use sqlalchemy or something to store things in database

@app.route('/', methods=['GET', 'POST'])
def index():
    # json_data = request.get_json(silent=True)
    # get json request

    json_data = { # for testing
        'user' : {
            'x' : 40.4406,
            'y' : -79.9959
        },
        'user2' : {
            'x' : 40.46,
            'y' : -79.94
        },
        'devices' : [
            {
                'id' : '0001',
                'x' : 37.5077121,
                'y' : 127.0624397,
                'data' : 'something'
            }
        ]
    }

    user_location = (json_data['user']['x'], json_data['user']['y'])
    user_location2 = (json_data['user2']['x'], json_data['user2']['y'])

    # json example : { 'user' : { 'x' : '300' , 'y' : '300' } }
    # get user_location from json & store as turple (x, y)

    devices_data[str(json_data['devices'][0]['id'])] = (
        json_data['devices'][0]['data']
    )

    devices_location[str(json_data['devices'][0]['id'])] = (
        json_data['devices'][0]['x'],
        json_data['devices'][0]['y']
    )
    # json example : { 'devices' : { 'id' : '0001', x' : '500', 'y' : '500' }, { ... } }
    # get device_location from json & store turple (x, y) in dictionary with device id as key
    # use for statements or something to get more locations from more devices

    circle = { # draw circle on map (user_location as center)
        'stroke_color': '#ff7d33',
        'stroke_opacity': .5,
        'stroke_weight': 5,
        # line(stroke) style
        'fill_color': '#ff7d33',
        'fill_opacity': .4,
        # fill style
        'center': { # set circle to user_location
            'lat': user_location[0],
            'lng': user_location[1]
        },
        'radius': 1500 # circle size (50 meters)
    }

    circle2 = { # draw circle on map (user_location as center)
        'stroke_color': '#ff7d33',
        'stroke_opacity': .5,
        'stroke_weight': 5,
        # line(stroke) style
        'fill_color': '#ff7d33',
        'fill_opacity': .4,
        # fill style
        'center': { # set circle to user_location
            'lat': user_location2[0],
            'lng': user_location2[1]
        },
        'radius': 500 # circle size (50 meters)
    }

    map = Map(
        identifier = "map", varname = "map",
        # set identifier, varname
        lat = user_location[0], lng = user_location[1],
        # set map base to user_location
        zoom = 15, # set zoomlevel
        #markers = [
        #    {
        #        'lat': devices_location['0001'][0],
        #        'lng': devices_location['0001'][1],
        #        'infobox': devices_data['0001']
        #    }
        #],
        # set markers to location of devices
        circles = [circle,circle2] # pass circles
    )

    return render_template('map.html', map=map) # render template
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/pastPredictions')
def pastPredictions():
    return render_template('pastPredictions.html')

@app.route('/predictionsProcess')
def predictionsProcess():
    return render_template('predictionProcess.html')

@app.route('/currentPredictions')
def currentPredictions():
    return render_template('currentPredictions.html')

@app.route('/getdata', methods=['GET', 'POST'])
def getdata():
    json_data = requests.get.args('json')
    return json_data
    # you can use this to get request with strings and parse json
    # put data in database or something

if __name__ == '__main__':
    app.run(debug = True) # run app
