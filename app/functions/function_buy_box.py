import pandas as pd
import numpy as np
from conf import configs as conf
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.express as px
from datetime import date, datetime
from pandas import DataFrame 


base_path = "./data/"



def get_digi_data():
    file_path = base_path + "main_page.csv"
    df = pd.read_csv(file_path, na_values="x")
    return df

def start_time():
    file_path = base_path + "ketabkala_new.json"
    df = pd.read_json(file_path)
    start_time = (df['start_time'])
    return start_time


    
def time_new():
    sd = pd.json_normalize(start_time())
    time = sd['$date.$numberLong'].dropna()
    time_list = time.to_list()


    new_time = []
    for x in time_list:
        converted = datetime.fromtimestamp(int(x)/1000)
        
        new_time.append(converted)

    Dataset = list(zip(new_time))
    df_time_make = DataFrame(data = Dataset, columns = ['time']).astype(str)

    number_df = df_time_make['time'].str.split(':').apply(lambda l: l[0])
    dd = number_df.str.split('15').apply(lambda x: x[0])

    dd_df = pd.DataFrame(dd)
    df_time_new =  dd_df.apply(lambda x: x['time'][:10], axis = 1).astype(str)
    
    return df_time_new
    
    
def buy_box_winner_variants():
    file_path = base_path + "main_page.csv"
    df = pd.read_csv(file_path, na_values="x")
    buy_box_winner_variants = df['buy_box_winner_variants']    
    
    return buy_box_winner_variants
    
def buy_box_loser_variants():
    file_path = base_path + "main_page.csv"
    df = pd.read_csv(file_path, na_values="x")
    buy_box_loser_variants = df['buy_box_loser_variants']
    
    return buy_box_loser_variants

def buy_box():
    fig = go.Figure(layout=conf.layout_simple)
    fig.add_trace(go.Histogram(x=time_new(), y=buy_box_winner_variants(),
                        histfunc='avg',
                        textposition='auto',
                        text = buy_box_winner_variants(),
                        name="میانگین برد"))
    fig.add_trace(go.Histogram(x=time_new(), y=buy_box_loser_variants(),
                        histfunc='avg',
                        textposition='auto',
                        text = buy_box_loser_variants(),
                        name='میانگین باخت'))
    fig.update_layout(
        title="برد باخت ",
        xaxis_title="تاریخ",
        yaxis_title= "buy box",
        legend_title="خطوط",
        font=dict(
            family="b mitra, monospace",
            size=18,
            color="white"
        )
    )
    return fig