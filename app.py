import os
from flask import Flask, render_template, Response
import country_data


from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
import io

app = Flask(__name__)

# import io
# from flask import Response
# import numpy as np


@app.route('/')
def home():
    countries_list = country_data.sorted_country
    countries_data = country_data.CountriesData
    heat_map_url = countries_data.heat_map()
    return render_template('home.html', countries=countries_list, data=countries_data, heat_map_url=heat_map_url)


@app.route('/countries/<name>')
def country_info(name):
    countrydetails = country_data.CountryDetails(name)
    return render_template('country_info.html', country=name, countrydetails=countrydetails)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)
