from flask import Flask
from flask import render_template, request, redirect, session, url_for
import requests
import json
import os
from dotenv import load_dotenv
import datetime
import locale
import random

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

register_url = "https://best-routes.herokuapp.com/user/register"
login_url = "https://best-routes.herokuapp.com/user/login"
logout_url = "https://best-routes.herokuapp.com/user/quit"
get_all_routes = "https://best-routes.herokuapp.com/routes/avia"
track_routes_url = "https://best-routes.herokuapp.com/user/track/avia"
track_trips_url = "https://best-routes.herokuapp.com/user/track/avia/trip"


@app.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == "POST":
        departureCode = request.form.get('departureCode')
        arrivalCode = request.form.get('arrivalCode')
        departureDate = request.form.get('departureDate')
        adult = request.form.get('adult')
        child = request.form.get('child')
        infant = request.form.get('infant')
        if request.form.get('serviceClass') == "Эконом":
            serviceClass = "Y"
        else:
            serviceClass = "C"
        count = -1
        search_params = {
            'departureCode': departureCode,
            'arrivalCode': arrivalCode,
            'departureDate': departureDate,
            'adult': adult,
            'child': child,
            'infant': infant,
            'serviceClass': serviceClass,
            'count': count
        }
        response = requests.request("GET", get_all_routes, params=search_params)
        response_dict = response.json().get('result')

        return render_template('base.html', routes=response_dict, length=len(response_dict))
    else:
        return render_template('base.html')


@app.route('/account', methods=['GET', 'POST'])
def index_page():
    if request.method == "POST":
        response_dict = get_routes()
        return render_template('index.html', routes=response_dict, length=len(response_dict))
    else:
        return render_template('index.html')


@app.route('/account/track', methods=['GET', 'POST'])
def track():
    if request.method == 'POST':
        response_dict = get_routes()
        return render_template('index.html', routes=response_dict, length=len(response_dict))
    else:
        headers = {
            'Token': session['token']
        }

        track_response = requests.request("GET", track_routes_url, headers=headers)
        track_response_dict = track_response.json().get('result')
        return render_template('track.html', routes=track_response_dict)


@app.route('/account/track/delete/<int:route_id>', methods=['GET', 'POST'])
def delete_routes(route_id):
    delete_route_url = "https://best-routes.herokuapp.com/user/track/avia/" + str(route_id)
    headers = {
        'Token': session['token']
    }

    response = requests.request("DELETE", delete_route_url, headers=headers)

    print(response.text)

    return redirect(url_for('track'))


@app.route('/account/track/trips', methods=['GET', 'POST'])
def track_trips():
    if request.method == 'POST':
        response_dict = get_routes()
        return render_template('index.html', routes=response_dict, length=len(response_dict))
    else:
        headers = {
            'Token': session['token']
        }

        track_tris_response = requests.request("GET", track_trips_url, headers=headers)
        track_response_dict = track_tris_response.json().get('result')
        print(track_response_dict)
        return render_template('trips.html', routes=track_response_dict)


@app.route('/account/track/trips/delete/<int:trip_id>', methods=['POST', 'GET'])
def delete_trip(trip_id):
    delete_trip_url = "https://best-routes.herokuapp.com/user/track/avia/trip/" + str(trip_id)
    headers = {
        'Token': session['token']
    }

    response = requests.request("DELETE", delete_trip_url, headers=headers)

    print(response.text)
    return redirect(url_for('track_trips'))


@app.route('/account/logout')
def logout():
    payload = {}
    headers = {
        'Token': session['token']
    }

    response = requests.request("POST", logout_url, headers=headers, data=payload)

    print(response.text, "logout")
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def auth_page():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        headers = {"Content-Type": "application/json"}
        payload = json.dumps({"email": email, "password": password})

        response = requests.request("POST", login_url, headers=headers, data=payload)
        print(response.json()['status'])
        if response.json()['status'] == "OK":
            session['token'] = str(response.json()['token'])
            print(session['token'])
            return redirect('/account')
        else:
            return render_template('auth.html')
    else:
        return render_template('auth.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        headers = {"Content-Type": "application/json"}
        payload = json.dumps({"email": email, "password": password})

        response = requests.request("POST", register_url, headers=headers, data=payload)
        print(response.text)
        if response.json()['status'] == "OK":
            session['token'] = str(response.json()['token'])
            print(session['token'])
            return redirect('/account')
        else:
            render_template('register.html')
    else:
        return render_template('register.html')


def get_routes():
    departureCode = request.form.get('departureCode')
    arrivalCode = request.form.get('arrivalCode')
    departureDate = request.form.get('departureDate')
    adult = request.form.get('adult')
    child = request.form.get('child')
    infant = request.form.get('infant')
    if request.form.get('serviceClass') == "Эконом":
        serviceClass = "Y"
    else:
        serviceClass = "C"
    count = -1
    search_params = {
        'departureCode': departureCode,
        'arrivalCode': arrivalCode,
        'departureDate': departureDate,
        'adult': adult,
        'child': child,
        'infant': infant,
        'serviceClass': serviceClass,
        'count': count
    }
    response = requests.request("GET", get_all_routes, params=search_params)
    response_dict = response.json().get('result')

    track_params = {
        'departureCode': departureCode,
        'departure': "Город",
        'arrivalCode': arrivalCode,
        'arrival': "Город",
        'departureDate': departureDate,
        'adult': adult,
        'child': child,
        'infant': infant,
        'serviceClass': serviceClass,
        'baseMinCost': response_dict[0]['minPrice']
    }

    date_1 = datetime.datetime.strptime(departureDate, "%Y-%m-%d")
    date_2 = date_1 + datetime.timedelta(days=random.randint(1, 90))

    track_trips_params = {
        'departureCode': departureCode,
        'departure': "Город",
        'arrivalCode': arrivalCode,
        'arrival': "Город",
        'departureDate1': departureDate,
        'departureDate2': str(date_2.date()),
        'adult': adult,
        'child': child,
        'infant': infant,
        'serviceClass': serviceClass,
        'baseMinCost1': response_dict[0]['minPrice'],
        'baseMinCost2': response_dict[0]['minPrice']
    }
    headers = {
        'Token': session['token']
    }
    track_response = requests.request("POST", track_routes_url, headers=headers, params=track_params)
    track_trip_response = requests.request("POST", track_trips_url, headers=headers, params=track_trips_params)
    print(track_response.text)
    print(track_trip_response.text)
    return response_dict



def date_m(date):
    formatted_date = datetime.datetime.fromisoformat(date)

    return str(formatted_date)


if __name__ == '__main__':
    app.run(debug=True)
