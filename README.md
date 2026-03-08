# Python Weather App

A simple weather application built with Python and Flask, featuring a beautiful HTML/CSS frontend.

## Features

- Get current weather information for any city
- Clean, responsive web interface
- Real-time weather data from OpenWeatherMap API
- Deployed on Vercel for production use

## Setup (Local Development)

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   python app.py
   ```

3. Open your browser and go to `http://127.0.0.1:5000/`

## Deployment to Vercel

1. Install Vercel CLI:
   ```
   npm install -g vercel
   ```

2. Deploy:
   ```
   vercel
   ```

3. Follow the prompts to deploy your project

## Project Structure

```
python-weather-app/
├── api/
│   └── index.py          # Vercel serverless function
├── templates/
│   └── index.html        # Frontend HTML
├── static/
│   └── styles.css        # CSS styling
├── app.py                # Local development Flask app
├── vercel.json           # Vercel configuration
└── requirements.txt      # Python dependencies
```

## Usage

Enter a city name in the input field and click "Get Weather" to see the current temperature and weather conditions.
