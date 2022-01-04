# This package provides an api for a grid front end to request transformed and aggregated data sets.
It is built around handling the requests from an ag-grid front end client, but cold easily be generalized to handle requests from other front ends. 

 
## Installation:
from source:
```bash
python setup.py install
```

or using package manager:
```bash
pip install pdgrid
```

## Running an example server
The example server provided is set up to be a python version of the laravel server provided here: (https://github.com/shuheb/ag-grid-angular-laravel-mysql).

Follow the steps in that example to set up a working front end client and to create a mysql database.

Assuming you have a mysql server set up with a database called sample_data create and populate the tables with:
```bash
$ cd examples
$ mysql -u user -p < create_athletes.sql
```

Install the python packages needed to run the server:
```bash
pip install -r server_requirements.txt
```

And now start up the server:

```bash
$ export FLASK_APP=server
$ python -m flask run --port=8000
```

If you have started up the front end client from the laravel example you should be able to see data at http://localhost:4200/

## Using other data
In order to serve another dataset you just have to provide a different loading function for the data. No other changes will be necessary on the pdgrid side, provided you have updated the front end server to request the corresponding data set.

## What is not supported

The pivod featere has not yet been implemented.



Contact me if you'd like help to build a custom server for your needs: svein.lindal@gmail.com

