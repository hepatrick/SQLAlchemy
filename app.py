from flask import Flask, jsonify
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def index():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start> <br/>"
        f"/api/v1.0/<start>/<end> <br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date, Measurement.station, Measurement.prcp).\
    filter(Measurement.date > "2016-08-23").all()
    
    # Define the list
    station_precipitation = []
    for Measurement.date, Measurement.station, Measurement.prcp in results:
        precip_dict = {}
        precip_dict["date"] = Measurement.date
        precip_dict["station"] = Measurement.station
        precip_dict["prcp"] = Measurement.prcp
        station_precipitation.append(precip_dict)
    
    return jsonify(station_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    station_list = session.query(Measurement.station).distinct()        
    return jsonify([station[0] for station in station_list])

@app.route("/api/v1.0/tobs")
def tobs():
    last_year_tobs = (session.query(Measurement.tobs).\
    filter(Measurement.date >= "2016-08-23").all())
    
    return jsonify(last_year_tobs)

if __name__ == '__main__':
    app.run(debug=True)