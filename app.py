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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
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
        precipitation.append(prcp.dict)

    return jsonify(precipitation) #NOT WORKING

#list of stations
@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)

    stations = session.query(S.station, S.name).all()

    session.close()

    return jsonify(stations)

#date and temp data of the most active station for the last year
@app.route("/api/v1.0/tobs")
def tobs():
    

    return 

@app.route("/api/v1.0/<start>")
def start():
    

    return 

@app.route("/api/v1.0/<start>/<end>")
def start_end():
    

    return 


# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)
