from flask import Flask, render_template, request, session, jsonify
import os
import json
import random

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


@app.route('/category/<string:category_name>', methods=['GET', 'POST'])
def category(category_name):
    action = request.form.get('action') if request.method == 'POST' else None
    with open(f'categories/{category_name}', 'r') as f:
        category = json.load(f)

    # Get previous, current and remaining phrases from session
    previous_phrases = session.get('previous_phrases', [])
    current_phrase = session.get('current_phrase')
    remaining_phrases = session.get('remaining_phrases', category['entries'])

    # Initial load of the category page
    if current_phrase is None:
        current_phrase = random.choice(remaining_phrases)
        remaining_phrases.remove(current_phrase)

    elif action == 'Next':
        # When all phrases have been shown, reset
        if not remaining_phrases:
            remaining_phrases = category['entries']

        # Don't add to previous_phrases on first phrase
        if current_phrase is not None:
            previous_phrases.append(current_phrase)

        current_phrase = random.choice(remaining_phrases)
        remaining_phrases.remove(current_phrase)

    elif action == 'Previous' and previous_phrases:
        remaining_phrases.append(current_phrase)
        current_phrase = previous_phrases.pop()

    session['previous_phrases'] = previous_phrases
    session['current_phrase'] = current_phrase
    session['remaining_phrases'] = remaining_phrases

    # AJAX Request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(current_phrase=current_phrase)
    # Normal Request
    else:
        return render_template('category.html', category=category, current_phrase=current_phrase)


@app.route('/times_up')
def times_up():
    return render_template('times_up.html')


if __name__ == '__main__':
    app.run(debug=True)
