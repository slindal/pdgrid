# This package provides an api for a grid front end to request transformed and aggregated data sets.
It is built around handling the requests from an ag-grid front end client, but could easily be generalized to handle requests from other front ends. 

## Requirements
Python 3.7 < 3.10 (tested with 3.8 and 3.9). Does not work with 3.10 as numpy build still hasn't been released for 3.10.
 
## Installation:
from source:
```bash
cd pdgrid
python setup.py install
```

or using package manager:
```bash
pip install pdgrid
```

## Running an example server
The example server provided is set up to be a python version of the laravel server provided here: (https://github.com/shuheb/ag-grid-angular-laravel-mysql).

Assuming you have a mysql server set up:
```bash
$ cd examples
$ msyql -u root
$ mysql> create database sample_data;
$ mysql> source ./create_athletes.sql;
```

Install the python packages needed to run the server:
```bash
pip install -r server_requirements.txt
```

And now start up the server (from example directory):

```bash
$ export FLASK_APP=server
$ python -m flask run --port=8000
```

If you have started up the front end client (follow readme here: https://github.com/shuheb/ag-grid-angular-laravel-mysql/blob/main/client/README.md) from the laravel example you should be able to see data at http://localhost:4200/

## Using other data
In order to serve another dataset you just have to provide a different loading function for the data. No other changes will be necessary on the server side, provided you have updated the front end client to request the corresponding data set.

## What is not supported
The pivot feature has not yet been implemented.


Contact me if you'd like help to build a custom server for your needs: svein.lindal@gmail.com

