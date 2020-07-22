# Udacity Data Scientist Nanodegree Capstone Project<br>"Forecasting of Fuel prices in Germany"

## Table of Contents

1. [Project Description](#description)
2. [Project Summary](#summary)
3. [Prerequisites](#prerequisites)
4. [Instructions and Files](#instructions)
5. [Discussion on project](#discussion)
6. [Data Structure of Tankerkoenig](#data)
7. [Acknowledgements](#acknowledge)

## Project description <a name = "description"/>
The fuel price is like the stock prices changing heavily on a day, but mostly not with the same amplitude. Therefore I want to have a look at the data and see what’s inside. Furthermore I want to build a forecasting model for the price on daily basis.
Therefore I used the history data available from [Tankerkoenig](https://dev.azure.com/tankerkoenig/_git/tankerkoenig-data "Tankerkoenig Data"), they are available in the azure cloud for private use with the following license
<https://creativecommons.org/licenses/by-nc-sa/4.0/>. 

The blog post is on Medium [Medium Post](https://medium.com/@joerg.meisterjahn/forecast-of-fuel-prices-in-germany-7cba2cfd015b)

## Project Summary <a name = "summary"/>
I've build different SARIMAX models and calculated the mean squared error and R2 Score for each. Also i build a LSTM neural network in addition. The models have promising values as you can see here:

| Model | MSE | R2 Score |
| --- | --- | --- |
| (0,1,1)x(0,1,1,52) | 0.001827971789383413 | -3.891623163418407 |
| (3,1,1)x(3,1,1,52) | 0.000816361372162868 | -1.184569926617356 |
| (3,1,2)x(3,1,2,52) | 0.000982089719322026 | -1.628056323129107 |
| LSTM | 9.64316349699766e-05 | 0.689759056453517 |

But nevertheless predicting a fuel price is not as easy and if you have a closer look to the predictions, you'll see big differences. Or in case of the LSTM, that it is not really predicting the future. The prediction for more days in the future goes to a limit. 

Therefore the models have to be optimized with other features to have better predictions.


## Prerequisites <a name = "prerequisites"/>
History Data from [Tankerkoenig History](https://dev.azure.com/tankerkoenig/_git/tankerkoenig-data) if you start in with Data Reading.


## Libraries needed
I'd used and therefore also recommend to use [Anaconda distribution](https://www.anaconda.com/), because it has most of mentioned libraries included.

You'll need:
- pandas
- glob
- math
- itertools
- matplotlib.pyplot
- plotly
- numpy
- sklearn
- keras
- sqlalchemy
- statsmodels
- pylab



## Instructions and Files <a name = "instructions"/>
If you downloaded the History Data (2015-2019) from [Tankerkoenig](https://dev.azure.com/tankerkoenig/_git/tankerkoenig-data) you can start on the beginning. There I loaded the files and reduced the dataset to a smaller number. The description of the used data structure you can find [below](#data).

For better handling i have created a slice out off the data, one year of data has around 5 GB. So i collected only stations with PLZ beginning with 40. Loaded the data per year and saved the data for the few stations in a sql file for later use. The needed functions for loading and saving data and for getting a dataset for a special station i've put in [helper_functions](./helper_functions.py "helper").

If you don't want to download all the data you can run cell 1 for importing all relevant libraries and go directly to **DataAnalysis** section in the notebook and load the data from the sqllite there i've done some data analysis and plottings with this data. There i read the data from a sqllite database created before [prices_40.sql](./Data/prices_40.sql "SQL Data"). The database consists of 2 tables `Prices` and `Stations`.

The preparation and implementation for building a forecast model follows in the notebook. On my MacbookPro (10 GB RAM) it was not possible to calculate the different ARIMA models in a sequence, even I overwrite everytime the data from previous calculation and give back only the fitted ARIMA model and forecast.


## Discussion on the Project <a name = "discussion"/>
You'll find a discussion of this Project in [Medium Post](https://medium.com/@joerg.meisterjahn/forecast-of-fuel-prices-in-germany-7cba2cfd015b)


### Data Structure of Tankerkoenig <a name = "data"/>
I've put the data in one directory "sprit" and inside this directory there where folder for every year and month. Inside the folders there is a csv-file for every day. So we have
`./sprit/year/month/year-month-day-prices.csv` for example `./sprit/2015/12/2015-12-01-prices.csv`. That is the same structure as it is on [Tankerkoenig](https://dev.azure.com/tankerkoenig/_git/tankerkoenig-data), despite of the `stations.csv`.

```
sprit
+-- stations.csv
+-- 2015
| +-- 01
| | +-- 2015-12-01-prices.csv
| | +-- ...
| +-- 02
| +-- ...
| +-- 12
+-- ...
+-- 2019
| +-- 01
| +-- 02
| +-- ...
| +-- 12
```

Inside the csv the data is structured as follows:

`date,station_uuid,diesel,e5,e10,dieselchange,e5change,e10change`

The corresponding stations are in the `./sprit/stations.csv` file and have the following structure inside:

`uuid,name,brand,street,house_number,post_code,city,latitude,longitude`

They are connected via the UUID in both files, so I've written a function to extract data from the dataframe for specific UUID and type of fuel.


```python
def get_data4uid(uid, typ):
    """
    Give the typ data for given uid
    Input: uid, typ
    Output: Dataframe"""
    data_uid = pd.DataFrame(prices_pd[prices_pd['station_uuid'] == uid][['date', typ]])
    
    data_uid.date = pd.to_datetime(data_uid.date, utc=True)
    
    data_uid.set_index('date', inplace=True)
   
    
    return data_uid
```


## Acknowledgements <a name = "acknowledge"/>

This project is a capstone project for Udacity Data Science nanodegree. Thanks to Udacity preparing me technically on this task with great learning material and projects.
I've to thank [Tankerkoenig](www.tankerkoenig.de) for the open source of data that makes it only possible to create some data analysis.

And last but not least thanks to my family for having great patience in the last months.