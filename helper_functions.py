import pandas as pd
from sqlalchemy import create_engine


# function to save data for later use in sqllite
def save_data(df, table, database_filename):
    """
    save databasefile in given database file
    """
    
    engine = create_engine('sqlite:///{}'.format(database_filename))
    df.to_sql(table, engine, index=False, if_exists='replace')

def load_data(database_filepath):
    """
    loads the data from given database
    Input: database filename
	Output: prices_db, stations_db
    """
    # load data from database
    engine = create_engine('sqlite:///{}'.format(database_filepath))
    df = pd.read_sql_table('Prices', engine)
    st = pd.read_sql_table('Stations', engine)
   
    return df, st
	

# function for getting special station and gas typ out of the data
def get_data4uid(prices_pd, uid, typ):
    """
    Give the typ data for given uid
    Input: prices Dataframe, uid, typ
    Output: Dataframe"""
    data_uid = pd.DataFrame(prices_pd[prices_pd['station_uuid'] == uid][['date', typ]])
    
    #set datetime for date column
    data_uid.date = pd.to_datetime(data_uid.date, utc=True)
    data_uid.set_index('date', inplace=True)
       
    return data_uid