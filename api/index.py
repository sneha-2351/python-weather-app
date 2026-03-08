from http.server import BaseHTTPRequestHandler
import urllib.parse
import json
import requests

# Embedded HTML content
HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather App</title>
    <style>
        body {font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin:0;padding:0;display:flex;justify-content:center;align-items:center;min-height:100vh;color:#333;}
        .container {background:rgba(255,255,255,0.9);padding:2rem;border-radius:10px;box-shadow:0 8px 32px rgba(31,38,135,0.37);backdrop-filter:blur(4px);border:1px solid rgba(255,255,255,0.18);max-width:400px;width:100%;text-align:center;}
        h1{color:#4a5568;margin-bottom:1.5rem;} form{margin-bottom:1.5rem;} input[type="text"]{padding:0.75rem;border:2px solid #e2e8f0;border-radius:5px;font-size:1rem;width:70%;margin-right:0.5rem;transition:border-color 0.3s;box-sizing:border-box;} input[type="text"]:focus{outline:none;border-color:#667eea;} button{padding:0.75rem 1.5rem;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;border:none;border-radius:5px;font-size:1rem;cursor:pointer;transition:transform 0.2s;} button:hover{transform:translateY(-2px);} #weather-result{margin-top:1.5rem;padding:1rem;background:rgba(255,255,255,0.8);border-radius:5px;} #weather-result h2{margin:0 0 0.5rem 0;color:#2d3748;} #weather-result p{margin:0.5rem 0;font-size:1.1rem;} #error-message{margin-top:1rem;color:#e53e3e;font-weight:bold;} .hidden{display:none;}
    </style>
</head>
<body>
    <div class="container">
        <h1>🌤️ Weather App</h1>
        <form id="weather-form">
            <input type="text" id="city-input" placeholder="Enter city name" required>
            <button type="submit">Get Weather</button>
        </form>
        <div id="weather-result" class="hidden">
            <h2 id="city-name"></h2>
            <p id="temperature"></p>
            <p id="weather-description"></p>
        </div>
        <div id="error-message" class="hidden"></div>
    </div>
    <script>
        document.getElementById('weather-form').addEventListener('submit', function(e){
            e.preventDefault();
            const city = document.getElementById('city-input').value;
            const btn = e.target.querySelector('button');
            btn.disabled=true; btn.textContent='Loading...';
            fetch('/get_weather',{
                method:'POST',
                headers:{'Content-Type':'application/x-www-form-urlencoded'},
                body:'city='+encodeURIComponent(city)
            })
            .then(res=>res.json())
            .then(data=>{
                if(data.success){
                    document.getElementById('city-name').textContent=data.city;
                    document.getElementById('temperature').textContent=`Temperature: ${data.temperature}°C`;
                    document.getElementById('weather-description').textContent=`Weather: ${data.weather}`;
                    document.getElementById('weather-result').classList.remove('hidden');
                    document.getElementById('error-message').classList.add('hidden');
                } else {
                    document.getElementById('error-message').textContent=`Error: ${data.error}`;
                    document.getElementById('error-message').classList.remove('hidden');
                    document.getElementById('weather-result').classList.add('hidden');
                }
            })
            .catch(()=>{
                document.getElementById('error-message').textContent='An error occurred. Please try again.';
                document.getElementById('error-message').classList.remove('hidden');
                document.getElementById('weather-result').classList.add('hidden');
            })
            .finally(()=>{btn.disabled=false; btn.textContent='Get Weather';});
        });
    </script>
</body>
</html>'''

class handler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type='text/html'):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.end_headers()

    def do_GET(self):
        if self.path == '/' or self.path.startswith('/?'):
            self._set_headers()
            self.wfile.write(HTML.encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(b'Not Found')

    def do_POST(self):
        if self.path == '/get_weather':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode()
            params = urllib.parse.parse_qs(body)
            city = params.get('city', [''])[0]
            if not city:
                self._set_headers(400, 'application/json')
                self.wfile.write(json.dumps({'success': False, 'error': 'City name required'}).encode())
                return
            api_key = 'b270d03ff3676c128cd71aef57bcd9da'
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
            try:
                resp = requests.get(url, timeout=5)
                data = resp.json()
                if data.get('cod') == 200:
                    temp = round(data['main']['temp'],1)
                    weather = data['weather'][0]['description'].capitalize()
                    result = {'success': True, 'city': city, 'temperature': temp, 'weather': weather}
                else:
                    result = {'success': False, 'error': data.get('message','City not found')}
            except Exception:
                result = {'success': False, 'error': 'Failed to fetch data'}
            self._set_headers(200, 'application/json')
            self.wfile.write(json.dumps(result).encode())
        else:
            self._set_headers(404)
            self.wfile.write(b'Not Found')
