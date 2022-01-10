# This package provides  an api for a grid front end to request transformed and aggregated data sets.

The api is written generically so that one server can handle multiple different data sets without any modifications beyond how the data is loaded from the database (or otherwise). It is built around handling the requests from an [ag-grid](https://www.ag-grid.com/) front end client, but could easily be generalized to handle requests from other front ends.

The ag-grid endpoint takes a Pandas dataframe and the corresponding ag-grid request and performs the transformations to the dataframe specified in the request, returning a dictionary formatted as expected by ag-grid.

The source code is available [here](https://github.com/slindal/pdgrid/tree/main/)

## Supported ag-grid features
Pagination, Grouping, Sorting, Aggregrations, Asynchronous fetching of set filter values, Filtering (text, numbers, text sets. Not datetype at the moment), 

## Requirements
Python 3.7, 3.8 or 3.9 (tested with 3.8 and 3.9). Does not work with 3.10 as numpy build still hasn't been released for 3.10.

## Installation:

From source:
```bash
$ git clone git@github.com:slindal/pdgrid.git
$ cd pdgrid
$ python3.9 -m venv env
$ . env/bin/activate
$ python setup.py install
```

Using package manager (in a python3 venv):
```bash
$ python -m pip install pdgrid
```

## Running an example server
The example server provided [here](https://github.com/slindal/pdgrid/tree/main/examples) is set up to be a python version of the laravel server provided in this example (https://github.com/shuheb/ag-grid-angular-laravel-mysql).

Set up mysql database and add a table:
```bash
$ cd examples
$ msyql -u root
$ mysql> create database sample_data;
$ mysql> source ./create_athletes.sql;
```

Install the python packages needed to run the server:
```bash
$ python -m pip install -r server_requirements.txt
```

Finally start up the server (from example directory):
```bash
$ export FLASK_APP=server
$ python -m flask run --port=8000
```

If you have started up the front end client (follow readme here: https://github.com/shuheb/ag-grid-angular-laravel-mysql/blob/main/client/README.md) from the laravel example you should be able to see data at http://localhost:4200/

## Using other data
In order to serve another dataset you just have to provide a different loading function for the data. No other changes will be necessary on the server side, provided you have updated the front end client to request the corresponding data set.
