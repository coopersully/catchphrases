import json
import os
from random import shuffle, randint

from flask import Flask, render_template, url_for

app = Flask(__name__)
app.secret_key = os.urandom(12)


@app.route('/')
def categories():
    categories = []
    for filename in os.listdir('categories'):
        with open(f'categories/{filename}', 'r') as f:
            category = json.load(f)
            categories.append({
                "name": category["name"],
                "description": category["description"],
                "filename": filename
            })
    return render_template('categories.html', categories=categories)


@app.route('/category/<string:category_name>', methods=['GET'])
def category(category_name):
    with open(f'categories/{category_name}', 'r') as f:
        category = json.load(f)

    # Randomize the order of entries
    shuffle(category['entries'])

    # Get sound url
    sound_url = url_for('static', filename='audio/tick.wav')

    # Generate random timer
    seconds = randint(30, 90)

    return render_template('category.html', category=category, sound_url=sound_url, time=seconds)


@app.route('/times_up')
def times_up():

    # Get sound url
    sound_url = url_for('static', filename='audio/alarm.wav')

    return render_template('times_up.html', sound_url=sound_url)


if __name__ == '__main__':
    app.run(debug=True)
