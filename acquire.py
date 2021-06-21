import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import acquire
import math
from env import user, host, password


###############acquire#################


def get_connection(database, user=user, host=host, password=password):
    '''get URL with user, host, and password from env '''
    
    return f"mysql+pymysql://{user}:{password}@{host}/{database}"
    
    
def cache_sql_data(df, database):
    '''write dataframe to csv with title database_query.csv'''
    
    df.to_csv(f'{database}_query.csv',index = False)
        

def get_sql_data(database,query):
    ''' check if csv exists for the queried database
        if it does read from the csv
        if it does not create the csv then read from the csv  
    '''
    
#    if os.path.isfile(f'{database}_query.csv') == False:   # check for the file
        
    df = pd.read_sql(query, get_connection(database))  # create file 
        
    cache_sql_data(df, database) # cache file
        
    return pd.read_csv(f'{database}_query.csv') # return contents of file


def get_zillow_data():
    ''' acquire zillow data'''
    
    query = '''

    select * 
    from predictions_2017

    left join properties_2017 using(parcelid)
    left join airconditioningtype using(airconditioningtypeid)
    left join architecturalstyletype using(architecturalstyletypeid)
    left join buildingclasstype using(buildingclasstypeid)
    left join heatingorsystemtype using(heatingorsystemtypeid)
    left join propertylandusetype using(propertylandusetypeid)
    left join storytype using(storytypeid)
    left join typeconstructiontype using(typeconstructiontypeid)

    where latitude is not null

    and longitude is not null

    '''

    database = "zillow"
    
    df = get_sql_data(database,query) # create/read csv for query
    
    df = df.sort_values('transactiondate').drop_duplicates('parcelid',keep='last') # drop duplicate parcelids keeping the latest
    
    return df 

