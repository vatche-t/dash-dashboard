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
    df_time = df_time_new.values.astype('datetime64[ns]')
    
    return df_time_new

    
def total_lost_sales():
    file_path = base_path + "main_page.csv"
    df = pd.read_csv(file_path, na_values="x")
    total_lost_sale_IRR_30_last_days = df['total_lost_sale_IRR_30_last_days']
    return total_lost_sale_IRR_30_last_days

def df_lost():
    Dataset = list(zip(total_lost_sales(), time_new()))
    df_lost = DataFrame(data = Dataset, columns = ['orders', 'date'])
    return df_lost

def sold_this_week_IRR():
    file_path = base_path + "main_page.csv"
    df = pd.read_csv(file_path, na_values="x")
    s = df['sold_this_week_IRR']
    sold_this_week_IRR = s.apply(lambda x: int(x.split()[0].replace(',', ''))).apply(lambda x: '%.5f' % x)
    return sold_this_week_IRR


def sold_last_month_IRR():
    file_path = base_path + "main_page.csv"
    df = pd.read_csv(file_path, na_values="x")
    s = df['sold_last_month_IRR']
    sold_last_month_IRR = s.apply(lambda x: int(x.split()[0].replace(',', ''))).apply(lambda x: '%.5f' % x)
    return sold_last_month_IRR
def sold_last_week_IRR():
    file_path = base_path + "main_page.csv"
    df = pd.read_csv(file_path, na_values="x")
    s = df['sold_last_week_IRR']
    sold_last_week_IRR = s.apply(lambda x: int(x.split()[0].replace(',', ''))).apply(lambda x: '%.5f' % x)
    return sold_last_week_IRR

def  sold_table():
    Dataset = list(zip(sold_this_week_IRR(), sold_last_week_IRR(),sold_last_month_IRR(),time_new()))
    df_sold = DataFrame(data = Dataset, columns = ['فروش این هفته به ریال', 'فروش هفته قبل به ریال','فروش ماه پیش به ریال','تاریخ'])
    return df_sold.max()



def lost_chart():
    fig = px.scatter(df_lost(), x="date", y="orders")
    fig.add_hline(y=4, line_width=2, line_dash='dash')
    fig.update_layout(
    title="میزان فروش از دست داده در سی روز آخر",
    xaxis_title="تاریخ",
    yaxis_title="میزان فروش از دست داده",
    legend_title="میانگین تبلیغات در چهار روز گذشته",
    
    template="plotly_dark",
    # plot_bgcolor="#FFFFFF",
    hovermode="x",
    hoverdistance=100,  
    spikedistance=1000,  
    xaxis=dict(
        title="تاریخ",
        linecolor="#BCCCDC",
        showspikes=True,
        spikesnap="cursor",
        spikethickness=1,
        spikedash="dot",
        spikecolor="#999999",
        spikemode="across",
    ),
    yaxis=dict(
        title="میزان فروش از دست داده",
        linecolor="#BCCCDC",
        tickformat=".2%",
        showspikes=True,
        spikesnap="cursor",
        spikethickness=1,
        spikedash="dot",
        spikecolor="#999999",
        spikemode="across",
    ),
    font=dict(
        family="b mitra, monospace",
        size=18,
        color="white"
    )
)
    return fig

