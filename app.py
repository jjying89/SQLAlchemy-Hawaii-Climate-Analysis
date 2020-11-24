import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
M = Base.classes.measurement
S = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
#create app
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
#create home page
#list available routes
@app.route("/")
def home():
    return (
        f"Welcome to the home page!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )

#precipitation data
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)

    results = session.query(M.date, M.prcp).\
        order_by(M.date).all()

    session.close()

    precipitation = []

    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        precipitation.append(prcp_dict)

    return jsonify(precipitation)

#list of stations
@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)

    results = session.query(S.station, S.name).all()

    session.close()

    return jsonify(results)

#date and temp data of the most active station for the last year
@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)

    #most active station is USC00519281
    #last year date starts from 2016-08-23

    results = session.query(M.date, M.tobs).\
        filter(M.station == 'USC00519281').\
        filter(M.date >= '2016-08-23').\
        order_by(M.date).all()

    session.close()

    temp = []

    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        temp.append(tobs_dict)

    return jsonify(temp)

#temp data with a given start date
@app.route("/api/v1.0/<start>")
def temp_start(start):
    
    session = Session(engine)

    results = session.query(func.min(M.tobs), func.avg(M.tobs), func.max(M.tobs)).\
        filter(M.date >= start).all()
        
    session.close()

    start_results = []

    for tmin, tavg, tmax in results:
        start_dict = {}
        start_dict['tmin'] = tmin
        start_dict['tavg'] = tavg
        start_dict['tmax'] = tmax
        start_results.append(start_dict)

    return jsonify(start_results)

#temp data with a given start and end date
@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start, end):
    
    session = Session(engine)

    results = session.query(func.min(M.tobs), func.avg(M.tobs), func.max(M.tobs)).\
        filter(M.date >= start).\
        filter(M.date <= end).all()
    
    session.close()
    
    start_end_results = []

    for tmin, tavg, tmax in results:
        start_end_dict = {}
        start_end_dict['tmin'] = tmin
        start_end_dict['tavg'] = tavg
        start_end_dict['tmax'] = tmax
        start_end_results.append(start_end_dict)

    return jsonify(start_end_results)


# Define main behavior
if __name__ == "__main__":
    app.run(debug=True)





