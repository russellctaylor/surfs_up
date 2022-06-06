import datetime as dt
import numpy as np
import pandas as pd

# SQLAlchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
# Flask dependencies
from flask import Flask, jsonify
# Setup Database
engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
#create a variable for each of the classes so that we can reference them later
Measurement = Base.classes.measurement
Station = Base.classes.station
#create a session link from Python to our database
session = Session(engine)
#define our Flask app , create a Flask application called "app."
app = Flask(__name__)
#9.5.2 Create the Welcome Route
#define the welcome route



@app.route("/")
#create a function welcome() with a return statement. 
#add the precipitation, stations, tobs, and temp routes that we'll need for this module into our return statement. 
def welcome():
    return('''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

#9.5.3 Precipitation Route
@app.route("/api/v1.0/precipitation")
#create the precipitation() function.
#def precipitation():
    #return
#add the line of code that calculates the date one year ago from the most recent date in the database
#write a query to get the date and precipitation for the previous year.
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)
#create a dictionary with the date as the key and the precipitation as the value. To do this, we will "jsonify" our dictionary. Jsonify() is a function that converts the dictionary to a JSON file.
# jsonify() gives the file structure 

#9.5.4 Stations Route
#return a list of all the stations.
@app.route("/api/v1.0/stations")

def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

#9.5.5 Monthly Temperature Route
@app.route("/api/v1.0/tobs")
#calculate the date one year ago from the last date in the database
#query the primary station for all the temperature observations from the previous year. 
# unravel the results into a one-dimensional array and convert that array into a list. Then jsonify the list and return our results
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
#9.5.6 Statistics Route
#create a route for our summary statistics report
#this route is different from the previous ones in that we will have to provide both a starting and ending date. 
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
#create a function called stats() to put our code in.
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)



if __name__ == '__main__':
    app.run()


