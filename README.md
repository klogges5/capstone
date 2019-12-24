# Project description
I want to analyze fuel prices in germany and investigate in some forecasting models to predict the fuel price in the future.
Therefore I used the history data available from [Tankerkoenig](https://dev.azure.com/tankerkoenig/_git/tankerkoenig-data), they are available in the azure cloud for private use with the following license
<https://creativecommons.org/licenses/by-nc-sa/4.0/>. 

The blog post is included in repository as pdf [blog](./Forecasting%20of%20Fuel%20prices%20in%20germany.pdf)


## Prerequisites
History Data from [Tankerkoenig History](https://dev.azure.com/tankerkoenig/_git/tankerkoenig-data) if you start in with Data Reading.


## Libraries needed

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



## Instructions
If you downloaded the History Data (2015-2019) from [Tankerkoenig](https://dev.azure.com/tankerkoenig/_git/tankerkoenig-data) you can start with [DataRead-Part](./DataRead.ipynb). And have a look at the Data Structure section below.

For better handling i have created a slice out off the data, one year of data has around 5 GB. So i collected only stations with PLZ beginning with 40. Loaded the data per year and saved the data for the few stations in a sql file for later use. The needed functions for loading and saving data and for getting a dataset for a special station i've put in [helper_functions](./helper_functions.py).

Therefore you can start directly with [DataPreparation](./DataPrep.ipnyb) there i've done some data analysis and graphical plottings with this data. There i read the data from a sqllite database created before [prices_40.sql](./Data/prices_40.sql). There i've put 2 tables inside `Prices` and `Stations`.

For the forecasting i've created an extra jupyter notebook [Forecasting](./Forecasting.ipynb).



## Discussion on the Project
You'll find a discussion of this Project in [Forecasting of Fuel prices in germany](./Forecasting of Fuel prices in germany.pdf)


### Data Structure
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

They are connected via the UUID in both files.


```
def get_data4uid(uid, typ):
    """
    Give the typ data for given uid
    Input: uid, typ
    Output: Dataframe"""
    data_uid = pd.DataFrame(prices_pd[prices_pd['station_uuid'] == uid][['date', typ]])
    
    # has to be changed, but for now utc=True
    data_uid.date = pd.to_datetime(data_uid.date, utc=True)
    
    data_uid.set_index('date', inplace=True)
   
    
    return data_uid
```
