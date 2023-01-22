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

    
def order_delivery_schedule():
    file_path = base_path + "ketabkala_new.json"
    df = pd.read_json(file_path)
    order_delivery = pd.json_normalize(df['order_delivery_schedule']).dropna() 
    return order_delivery

def deliver():
    df_schedule = pd.DataFrame(order_delivery_schedule())
    delivery_schedule = df_schedule['delivery_schedule']
    df_of_delivery = pd.json_normalize(delivery_schedule)
    return df_of_delivery

def count():
    count = deliver().dropna()
    return count    
def df_of_day1():
    df_of_day1 = (pd.json_normalize(count().iloc[0]).dropna())
    return df_of_day1
def df_of_day2():
    df_of_day2 = (pd.json_normalize(count().iloc[150]).dropna())
    return df_of_day2
def date_of_schedule_cl_1():
    date_of_schedule_cl_1 = df_of_day1()['date'].map(lambda x: x.lstrip('')).dropna().drop_duplicates()
    return date_of_schedule_cl_1
def date_of_schedule_1():
    date_of_schedule_1 = date_of_schedule_cl_1().map(lambda l:l.lstrip('')).dropna().drop_duplicates()
    return date_of_schedule_1
def date_of_schedule_cl():
    date_of_schedule_cl = df_of_day2()['date'].map(lambda x: x.lstrip('')).dropna().drop_duplicates()
    return date_of_schedule_cl
def date_of_schedule():
    date_of_schedule = df_of_day2()['date'].map(lambda x: x.lstrip('')).dropna().drop_duplicates()
    return date_of_schedule
def count_of_orders_1():
    count_of_orders_1 = df_of_day1()['count']
    return count_of_orders_1   
def count_of_orders():
    count_of_orders = (df_of_day2()['count'])
    return count_of_orders   
    
    
    
    
def orders_chart():
    fig = go.Figure()
    fig.add_trace(go.Bar(x=date_of_schedule_cl_1(), y=count_of_orders_1(),
                        name='سفارشات برنامه ریزی شده روز اول'))
    fig.add_trace(go.Bar(x=date_of_schedule_cl(), y=count_of_orders(),
                        name='آخرین روز سفارشات برنامه ریزی شده'))
    fig.update_layout(
        title=" سفارشات برنامه ریزی شده ",
        xaxis_title="تاریخ",
        yaxis_title="کل سفارشات برنامه ریزی شده برای تحویل ",
        legend_title="خطوط",
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
        title=" سفارشات برنامه ریزی شده برای تحویل ",
        linecolor="#BCCCDC",
        # tickformat=".2%",
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
        color="white",
    )
    )
    return fig

def today_orders():
    file_path = base_path + "main_page.csv"
    df = pd.read_csv(file_path, na_values="x")
    today_orders = df['today_orders']
    return today_orders





Dataset = list(zip(today_orders(), time_new()))
df_orders = DataFrame(data = Dataset, columns = ['orders', 'date']).drop_duplicates()
orders = df_orders.sort_values(by='orders',ascending=True)

def chart_violin():
    fig = go.Figure(data=[go.Violin(
                x=orders['date'], y=orders['orders'],
                
                # text=df_orders['orders'],
                # textposition='auto',
                # histfunc='avg'
            )])

    fig.update_layout(
            title="میانگین سفارشات در چهار روز",
            xaxis_title="تاریخ",
            yaxis_title="سفارشات",
            legend_title="میانگین سفارشات در جهار روز",
                template="plotly_dark",
        hovermode="x",
        hoverdistance=100,  
        spikedistance=1000,  
        xaxis=dict(
            showgrid=True,
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
            showgrid=True,
            title="سفارشات",
            linecolor="#BCCCDC",
            showspikes=True,
            spikesnap="cursor",
            spikethickness=1,
            spikedash="dot",
            spikecolor="#999999",
            spikemode="across",
        ),
    )
    font=dict(
            family="b mitra, monospace",
            size=18,
            color="black"
        )
    

    return fig

def chart_box():
    fig = go.Figure(data=[go.Box(
                x=orders['date'], y=orders['orders'],
                
                # text=df_orders['orders'],
                # textposition='auto',
                # histfunc='avg'
            )])

    fig.update_layout(
            title="میانگین سفارشات در چهار روز",
            xaxis_title="تاریخ",
            yaxis_title="سفارشات",
            legend_title="میانگین سفارشات در جهار روز",
                template="plotly_dark",
        hovermode="x",
        hoverdistance=100,  
        spikedistance=1000,  
        xaxis=dict(
            showgrid=True,
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
            showgrid=True,
            title="سفارشات",
            linecolor="#BCCCDC",
            showspikes=True,
            spikesnap="cursor",
            spikethickness=1,
            spikedash="dot",
            spikecolor="#999999",
            spikemode="across",
        ),
    )
    font=dict(
            family="b mitra, monospace",
            size=18,
            color="black"
        )
    

    return fig

