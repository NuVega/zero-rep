from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    fact = None

    if request.method == 'POST':
        response = requests.get('https://catfact.ninja/fact')
        if response.status_code == 200:
            data = response.json()
            fact = data.get('fact')
        else:
            fact = "Не удалось получить факт о котиках."

    return render_template('index.html', fact=fact)

if __name__ == "__main__":
    app.run(debug=True)