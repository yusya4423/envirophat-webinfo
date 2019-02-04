#!/usr/bin/env python3

from flask import Flask, render_template, jsonify
import envirophat
import os

HTTP_PORT = int(os.environ.get('HTTP_PORT', '5000'))

app = Flask(__name__)

@app.route('/environ')
def showEnviron():
    result = {
        'error': True,
        'results': {
            'altitude': None,
            'tempture': None,
            'pressure': None,
            'light': None,
            'color': (None, None, None),
            'leds': None
        },
    }

    try:
        result['results']['tempture'] = envirophat.weather.temperature()
        result['results']['altitude'] = envirophat.weather.altitude()
        result['results']['pressure'] = envirophat.weather.pressure(unit='hPa')
        result['results']['light'] = envirophat.light.light()
        result['results']['color'] = envirophat.light.rgb()
        result['results']['leds'] = bool(envirophat.leds.status)
        result['error'] = False

    except Exception as e:
        result['altitude'] = e.message

    return jsonify(result)

@app.route('/led/<state>')
def leds(state):
    if state.lower() == 'on':
        envirophat.leds.on()
        return jsonify(result=True)

    envirophat.leds.off()
    return jsonify(result=False)

@app.route('/')
def home():
   return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=HTTP_PORT, threaded=True)
