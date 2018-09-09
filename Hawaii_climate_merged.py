
# matplotlib notebook
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
inspector = inspect(engine)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

measurement = session.query(Measurement).first()
measurement.__dict__

# Design a query to retrieve the last 12 months of precipitation data and plot the results
# Calculate the date 1 year ago from today
year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
#year_ago
# Perform a query to retrieve the data and precipitation scores between 8/24/2016 and 8/23/2017 and arrange by date
precip_query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).\
group_by(Measurement.date).order_by((Measurement.date).asc()).all()

precip_query

# Save the query results as a Pandas DataFrame and set the index to the date column
precip_df = pd.DataFrame(precip_query)
#precip_df.head()
precipitation = precip_df.set_index("date")
precipitation.columns = ['Precipitation']
precipitation.head()


# Use Pandas Plotting with Matplotlib to plot the data
precipitation.plot()
plt.tight_layout()
# Rotate the xticks for the dates
plt.xticks(rotation=45)
plt.show()

#Use Pandas to calculate the summary statistics for the precipitation data
precipitation.describe()

station = session.query(Station).first()
station.__dict__

# How many stations are available in this dataset?
station_count = session.query(Station).count()
station_count

# What are the most active stations?
# List the stations and the counts in descending order.
station_activity = session.query(Station.station, Station.name, func.count(Measurement.tobs)).\
group_by(Measurement.station).filter(Station.station ==  Measurement.station).group_by(Measurement.station).\
order_by(func.count(Measurement.tobs).desc()).all()

station_activity

# Using the station id from the previous query, calculate the lowest temperature recorded, 
# highest temperature recorded, and average temperature most active station?
active_station = session.query(Measurement.station, Station.name, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
filter(Measurement.station == 'USC00519281').all()

active_station

# Choose the station with the highest number of temperature observations.
# Query the last 12 months of temperature observation data for 'Waikiki' station
waikiki = session.query(Measurement.station, Measurement.tobs).filter(Measurement.date >= year_ago).filter(Measurement.station == 'USC00519281').all()

waikiki

# Create dataframe for Waikiki station data
waikiki_df = pd.DataFrame(waikiki)
waikiki_df.head()

# Plot 'waikiki' station observations as histogram
waikiki_df.plot.hist(bins=12)
plt.ylabel("Frequency")
plt.title("Waikiki Station Temperature Observation")
plt.tight_layout()
plt.show()
