from flask import Flask, render_template
import numpy as np
import pandas
import matplotlib.pyplot as plt

import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from price_calculator_all import get_price_chart
from html_price_receiver import receive_update

import subprocess
from multiprocessing import Process
import time


# Create the flask app
app = Flask(__name__)

# Create global variables that are required within several routes
fig = None
entries = None
p = None

# Route for the graph. The matplotlib figure will be converted to a png file and 
# inserted as an image in the webpage.
@app.route('/cmpg/plot.png')
def plot_png():
    global fig
    global entries
    if fig is None:
        fig, entries = get_price_chart()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

# Route for the app. Renders the html template with the given parameters.
@app.route('/cmpg')
def cardmarket_price_getter():
    global fig
    global entries
    global p

    # If the downloader task was not started yet, start it.
    if p is None:
        p = Process(target=downloader_task)
        p.start()

    # Receive the price information
    fig, entries = get_price_chart()
    return render_template('index.html', name="Double Masters 2022", entries=entries)


# Task for the downloader. Will update every hour.
def downloader_task():
    while True:
        receive_update()
        time.sleep(60 * 60)

if __name__ == '__main__':
    # Main will only be called when executed directly.
    p = Process(target=downloader_task)
    p.start()
    app.run(debug = True)
