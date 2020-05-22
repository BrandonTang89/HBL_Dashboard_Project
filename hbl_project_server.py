from flask import *
import csv
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    return ('Hello, World!')

@app.route('/<class_name>')
def class_name(class_name):
    class_set = {"1A","1B","1C","1D","1E","2A","2B","2C","2D","2E","3A","3B","3C","3D","3E","4A","4B","4C","4D","4E","120","119","220","219","320","319","420","419","520","519","620","619","720","719","820","819","920","919","1020","1019","1120","1119","1220","1219","1320","1319","1420","1419","1520","1519","1620","1619","1720","1719","1820","1819","1920","1919","2020","2019","2120","2119","2220","2219","2320","2319","2420","2419"}
    if not class_name in class_set:
        return ("Invalid Class")

    return render_template("dashboard.html", class_name=class_name)


@app.route('/update')
def update_form():
    return render_template("update_form.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='3000', debug=True)