# This package provides a higly performant api for a grid front end to request transformed and aggregated data sets.

The api is written generically so that one server can handle multiple different data sets without any modifications beyond how the data is loaded from the database (or otherwise). It is built around handling the requests from an [ag-grid](https://www.ag-grid.com/) front end client, but could easily be generalized to handle requests from other front ends.

The ag-grid endpoint takes a Pandas dataframe and the corresponding ag-grid request and performs the transformations to the dataframe specified in the request, returning a dictionary formatted as expected by ag-grid.


The source code is available [here](https://github.com/slindal/pdgrid/tree/main/)

# Performance
When benchmarked against a purpose-built Java server PDGrid generally outperformed Java. In some cases by a large factor, depending on the size of the data set. Pandas is extremely performant when performing grouping, aggregation, filtering and sorting commands. The biggest bottleneck in most cases will be the loading of the data from db or otherwise. By caching the data in Apache Parquet format this can be speeded up significantly (see example [here](https://github.com/slindal/pdgrid/tree/main/examples)).

## Supported ag-grid features
Pagination, Grouping, Sorting, Aggregrations, Asynchronous fetching of set filter values, Filtering (text, numbers, text sets. Not datetype at the moment), 

Pivot support, Datetype filtering will be added next. 

## Requirements
Python 3.8 or 3.9.

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
No changes are necessary on the server side, beyond changing the function that loads the data from database or elsewhere. The front end client must be updated to handle any changes to the data set.
