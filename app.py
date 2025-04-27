from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = "AIzaSyBluQRYMhMMmzloON4zCHXCYtRuI-koZ5E"

def get_top_places(city, place_type, top_n=10):
    geo_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={city}&key={API_KEY}"
    geo_response = requests.get(geo_url).json()
    location = geo_response['results'][0]['geometry']['location']
    lat, lng = location['lat'], location['lng']

    places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=5000&type={place_type}&key={API_KEY}"
    places_response = requests.get(places_url).json()
    results = places_response.get('results', [])

    top_places = sorted(results, key=lambda x: x.get('user_ratings_total', 0), reverse=True)[:top_n]

    return [
        {
            'name': place.get('name'),
            'rating': place.get('rating'),
            'user_ratings_total': place.get('user_ratings_total'),
            'address': place.get('vicinity')
        }
        for place in top_places
    ]

@app.route('/get_top_places', methods=['POST'])
def search_places():
    data = request.get_json()
    city = data.get('city')
    place_type = data.get('place_type')
    return jsonify(get_top_places(city, place_type))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
