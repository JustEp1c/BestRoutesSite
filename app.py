from flask import Flask
from flask import render_template, request, redirect, session, url_for
import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime
import locale

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

register_url = "https://best-routes.herokuapp.com/user/register"
login_url = "https://best-routes.herokuapp.com/user/login"
logout_url = "https://best-routes.herokuapp.com/user/quit"
get_all_routes = "https://best-routes.herokuapp.com/routes/avia"
track_routes_url = "https://best-routes.herokuapp.com/user/track/avia"


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
        count = 10
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
        return render_template('base.html', routes=response_dict)
    else:
        return render_template('base.html')


@app.route('/account', methods=['GET', 'POST'])
def index_page():
    if request.method == "POST":
        response_dict = get_routes()
        return render_template('index.html', routes=response_dict)
    else:
        return render_template('index.html')


@app.route('/account/track', methods=['GET', 'POST'])
def track():
    if request.method == 'POST':
        response_dict = get_routes()
        return render_template('index.html', routes=response_dict)
    else:
        pass
    headers = {
        'Token': session['token']
    }

    response = requests.request("GET", track_routes_url, headers=headers)

    print(response.text)
    return render_template('track.html')


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
            return redirect('/index')
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
            return redirect('/index')
        else:
            render_template('register.html')
    else:
        return render_template('register.html')


# @app.route('/user/<string:email>', methods=['GET', 'POST'])
# def user_page():
#     return render_template('user.html')
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
    count = 10
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
        'arrivalCode': arrivalCode,
        'departureDate': departureDate,
        'adult': adult,
        'child': child,
        'infant': infant,
        'serviceClass': serviceClass,
        'baseMinCost': response_dict[0]['minPrice']
    }
    headers = {
        'Token': session['token']
    }
    track_response = requests.request("POST", track_routes_url, headers=headers, params=track_params)
    print(track_response.text)
    return response_dict


def date_m(date):
    formatted_date = datetime.fromisoformat(date)

    return str(formatted_date)


if __name__ == '__main__':
    app.run(debug=True)
