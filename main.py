import json
from yandex_geocoder import Client
from geopy.distance import lonlat, distance
import folium
from flask import Flask

FILE_WITH_BARS_DATA = "moscow_bars_data.json"
NUMBER_OF_NEAREST_BARS = 5


def open_bars_data_file(filename):
    with open(filename, "r", encoding="cp1251") as bars_file:
        return json.load(bars_file)


def get_distance(bar):
    return bar['distance']


def get_nearest_bars(bars):
    bars_list = []
    for bar in bars:
        longitude = bar['geoData']['coordinates'][0]
        latitude = bar['geoData']['coordinates'][1]
        bar_coordinatates = (longitude, latitude)
        bar_details = {
                    'title': bar['Name'],
                    'longitude': bar['geoData']['coordinates'][0],
                    'latitude': bar['geoData']['coordinates'][1],
                    'distance': distance(lonlat(*user_coordinates), lonlat(*bar_coordinatates)).km
        }
        bars_list.append(bar_details)

    sorted_bars = sorted(bars_list, key=get_distance)
    return sorted_bars[:NUMBER_OF_NEAREST_BARS]


def open_map_file():
    with open('index.html') as file:
        return file.read()


def put_bars_on_the_map(nearest_bars):
    for bar in nearest_bars:
        bar_coordinatates = [bar['latitude'], bar['longitude']]
        bar_title = bar['title']
        bar_tooltip = bar['distance']
        folium.Marker(bar_coordinatates, popup=bar_title, tooltip=bar_tooltip).add_to(bars_map)
    bars_map.save('index.html')


if __name__ == '__main__':
    user_location = input('Где вы находитесь?: ')
    user_coordinates = Client.coordinates(user_location)
    bars_map = folium.Map(location=(user_coordinates[1], user_coordinates[0]), zoom_start=15)

    put_bars_on_the_map(get_nearest_bars(open_bars_data_file(FILE_WITH_BARS_DATA)))

    app = Flask(__name__)
    app.add_url_rule('/', 'map', open_map_file)
    app.run('0.0.0.0')
