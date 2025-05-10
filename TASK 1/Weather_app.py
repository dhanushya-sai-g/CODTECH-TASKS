from flask import Flask, render_template, request, redirect, url_for
import datetime as dt
import requests



BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?'
API_KEY = '4a37e8862a13304eabd06a39eff22f64'

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/submit', methods=['POST','GET'])
def submit():
    city = request.form['city']
    url = BASE_URL+"appid="+API_KEY+"&q="+city
    response = requests.get(url).json()
    def kelvin_to_celsius(kelvin):
        celsius = kelvin - 273.15
        return celsius

    Lat = response['coord']['lat']
    Long = response['coord']['lon']

    weather = response['weather'][0]['main']
    description = response['weather'][0]['description']

    temperature = kelvin_to_celsius(response['main']['temp'])
    feels_like = kelvin_to_celsius(response['main']['feels_like'])
    min_temp = kelvin_to_celsius(response['main']['temp_min'])
    max_temp = kelvin_to_celsius(response['main']['temp_max'])

    humidity = response['main']['humidity']

    visibility = response['visibility']/1000

    wind_speed = response['wind']['speed']

    timezone = response['timezone']

    sunrise_utc = response['sys']['sunrise']
    sunset_utc = response['sys']['sunset']

    sunrise_local = dt.datetime.utcfromtimestamp(sunrise_utc + timezone)
    sunset_local = dt.datetime.utcfromtimestamp(sunset_utc + timezone)

    current_time=response['dt']
    current_local = dt.datetime.utcfromtimestamp(current_time+timezone)
    return render_template('visual.html', city=city, weather=weather, description=description, temperature=temperature, feels_like=feels_like, min_temp=min_temp, max_temp=max_temp, humidity=humidity, visibility=visibility, wind_speed=wind_speed, sunrise_local=sunrise_local, sunset_local=sunset_local, current_local=current_local)











if __name__ == '__main__':
    app.run(debug=True)