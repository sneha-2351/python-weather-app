from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.form['city']
    api_key = "b270d03ff3676c128cd71aef57bcd9da"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    data = response.json()

    if data.get("cod") == 200:
        temperature = data["main"]["temp"]
        weather = data["weather"][0]["description"]
        return {
            'success': True,
            'city': city,
            'temperature': temperature,
            'weather': weather
        }
    else:
        return {
            'success': False,
            'error': data.get("message", "Unknown error")
        }

if __name__ == '__main__':
    app.run(debug=True)