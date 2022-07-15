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


app = Flask(__name__)
# variables = pandas.read_csv('C:\\path\\to\\variable.csv')
# price =variables['price']

fig = None
entries = None
p = None

@app.route('/cmpg/plot.png')
def plot_png():
    global fig
    global entries
    if fig is None:
        fig, entries = get_price_chart()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/cmpg')
def cardmarket_price_getter():
    global fig
    global entries
    global p

    if p is None:
        p = Process(target=downloader_task)
        p.start()

    fig, entries = get_price_chart()
    return render_template('index.html', name="Double Masters 2022", entries=entries)


def downloader_task():
    while True:
        receive_update()
        time.sleep(60 * 60)

if __name__ == '__main__':

    p = Process(target=downloader_task)
    p.start()
    app.run(debug = True)
