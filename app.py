from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home_page():
    return render_template('index.html')


@app.route('/auth')
def auth_page():
    return render_template('auth.html')


if __name__ == '__main__':
    app.run(debug=True)
