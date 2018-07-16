# Pseudo processing data pipeline for csv file format.
Based on concepts applied to retail Scanner Data 

## Goal(s) 

* Provide basic funtionality of all processing steps.
* Provide standalone python processing framework.
* Enable benchmarking
* Enable validation of results
* Compare result and benchmarks to existing processes
* Minimize external libraries
* Reduce use of SAS, Windows and any non-OSS tool

Additional Libraries (what is required in the venv)

* Python3
* numpy
* matplotlib
* TBA: pandas, scikit (for KDE and splines)

### Monitoring and persistency are key features.

* Enable file splitting and file conversion.
* Enable histogram creation and storage
* Enable merging of files and histograms

### Clear seperation of tasks

* Tasks can be connected into a pipeline via some transform.
* Initially will be a simple python example script.
* Each tasks should be able to run on different platforms, 
* e.g. linux, hadoop, pachyderm, DataHub (MIT) 

### Known Tasks

* Read csv file
* Parse row
* Define schema
* Check schema against row in csv file
* Store columns into arrays
* Store arrays in histograms
* Store histograms to file
* Split input file to output dataset
* Convert to various file types

* Read dataset as input
* Rerun above steps with new dataset

* Generate model from data
* Output model 
* Output synthetic data set
* Rerun above steps on synthetic data

* Read dataset as input
* Create analysis algorithm
* Create a map step
* Create a reduce step
* Create an iterative step
* Store map output
* Store reduce output
* Store results of iterative step (e.g. model)
* Apply model to dataset for validation


### Requirements:
* Error Handling
* Logging
* Profiling
* Testing 
* doctest
* unittest
* example script
* Juypter notebook

### Meta Data

* Persistent meta data object to describe the schema or record layout.
* Stort metadata object in database, lookup related to dataset
* Use meta data instance for Schema Checking
* Use the meta data instance for configuring a monitoring class?

#### Schema Checking

* Checks length of row in data set.
* Checks individual data types.
* Enable reading row by bytes.
* Logs failures, indicates row and item
* Handle by exceptions or just throwing errors?
* Exceptions will cause program to abort.

### File Handling

* Read chunks of data into memory.
* Process per-line.
* Yields a row in csv file.
* row is a list, require passing bytes?
* Data conversion

### Data Quality and Monitoring

* Retain column data in histograms.
* Store histograms.
* Merge histograms (e.g. hadd).

### Data Generation

* Use of DataSynthesizer
* Additional libraries -- numpy, scipy, pandas, dateutil

### Data Analysis
Easily provide data so analyst needs simple class instance
Can a single class handle map steps and reduce steps?
Lists of data handles can be used for input and output

class AnalysisClass():
    __init__(input):
        '''
        input can be a list of files, e.g. glob directory
        '''
        self.data = pd.(input)
    __exec__()
        '''
        Custom analysis code, anything with a DataFrame
        '''
        ... do some analysis
    __finalize__(output)
        output can be a list of data
        convert self.data to standard format

Example Usage
Jupyter notebook included (can replace the example.py code)
    
## Data Processing Summary of typical admin scanner data
1. Data chunking -- read 1 million rows from sasbdat file
2. Data conversion -- convert sasbdat chunk to msgpack format
3. Map 
    * Process each converted file (can be parallelized).
    * Reads msgpack file.
    * Reads code map file (MCH0 to NAPCS).
    * Outputs two aggregated files in msgpack format.
    * Map Product description to internal code classification, add code column to msgpack input pd.
    * Store any missing codes from description.
    * Add regional sales columns to pd.
    * Add brand sales to pd.
    * Groupby code and sum, store to output.
    * Groupby Postal code and city and sum, store to output (csv).
4. Reduce Step
    Concat all files from NAPCS or Postal code
    Create single data frame groupby and sum (NAPCS or Postal Code)

## References    
Data Processing and schema for csv files references:
csv
Python Cookbook 8.13 -- Implementing a Data Model or Type System
http://blog.districtdatalabs.com/simple-csv-data-wrangling-with-python
https://github.com/frictionlessdata/tableschema-py

plotting
https://github.com/janpipek/physt
