from flask import Flask
from flask import render_template, request, redirect, url_for
import requests
import json

app = Flask(__name__)

register_url = "https://best-routes.herokuapp.com/user/register"
login_url = "https://best-routes.herokuapp.com/user/login"


@app.route('/', methods=['GET', 'POST'])
def home_page():
    return render_template('index.html')


@app.route('/auth', methods=['GET', 'POST'])
def auth_page():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        headers = {"Content-Type": "application/json"}
        payload = json.dumps({"email": email, "password": password})

        response = requests.request("POST", login_url, headers=headers, data=payload)
        print(response.text)
        return redirect('/')
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
        return redirect('/')
    else:
        return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
