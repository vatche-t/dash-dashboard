import pandas as pd
import numpy as np
from conf import configs as conf
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import plotly.express as px
#ساختن دیتا و پلات ها

base_path = "./data/"



def get_digi_data():
    file_path = base_path + "miladi.csv"
    df = pd.read_csv(file_path, na_values="x")
    df.rename(
        {"data": "report_data"},
        axis=1,
        inplace=True,
    )
    df["report_date"] = df["report_date"].values.astype('datetime64[ns]')
    df["release_date"] = df["release_date"].values.astype('datetime64[ns]')

    return df

def create_navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="صفحه ها", 
                children=[
                    dbc.DropdownMenuItem("صفحه اصلی", href='/'), 
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("صفحه فروش", href='/sales'),
                ],
            ),
        ],
        brand="صفحه اصلی",
        brand_href="/",  
        sticky="top",  
        color="dark",  
        dark=True,  
    )

    return navbar

# .values.astype('datetime64[ns]')
def add_report_long_names(df1):
    df = df1.copy()
    for index in df.index:
        if df.loc[index, "report_name"] == "all_orders":
            df.loc[index, "report_long_name"] = " تمام سفارشات"
            df.loc[index, "category"] = "orders ketabkala"
        if df.loc[index, "report_name"] == "buy_box_winners":
            df.loc[index, "report_long_name"] = "برنده بای باکس"
            df.loc[index, "category"] = "buy_box_winners ketabkala"
        if df.loc[index, "report_name"] == "all_promotions":
            df.loc[index, "report_long_name"] = "تمام تخفیفات"
            df.loc[index, "category"] = "all_promotions ketabkala"    

    return df




#specific report
def get_report_from_digi_data(df1, report_name):
    df = df1.copy()
    df = df[df["report_name"] == report_name]
    df.sort_values(by=["report_date"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


# function to pull a specific report_date
def get_report_date_from_digi_data(df1, report_date):
    df = df1.copy()
    df1 = df[df["report_date"] == report_date]
    df.sort_values(by=["report_date"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


#  report_date
#needfixing
def get_report_after_date_digi_data(df1, report_date):
    df = df1.copy()
    df = df[df["report_date"] >= report_date]
    df.sort_values(by=["report_date"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


#specific release_date
#needfixing
def get_release_date_from_digi_data(df1, release_date):
    df = df1.copy()
    df = df[df["release_date"] == release_date]
    df.sort_values(by=["report_date"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


#release_dates after a date
#needfixing
def get_release_after_date_digi_data(df1, release_date):
    df = df1.copy()
    df = df[df["release_date"] >= release_date]
    df.sort_values(by=["report_date"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


#rate change
def period_change(df):
    df["period_change"] = df.report_data.pct_change()
    df["relative_change"] = 1 - df.iloc[0].report_data / df.report_data
    return df


#latest report

def get_latest_data(df1):
    df = df1.copy()
    df = df.sort_values("release_date").groupby("report_date").tail(1)
    df.sort_values(by=["report_date"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df



def get_category_data_from_digi_data(df1, report_name, report_date):
    df = df1.copy()
    master_list = df["report_name"].unique()
    master_list = pd.DataFrame(master_list, columns=["report_name"])
    master_list = add_report_long_names(master_list)
    filtered_list = master_list[master_list["report_name"] == report_name]
    filtered_list = master_list[
        master_list["category"] == filtered_list.category.iloc[0]
    ]

    df_out = pd.DataFrame()
    for index, row in filtered_list.iterrows():
        temp_df = get_report_from_digi_data(df, row.report_name)
        temp_df = get_report_after_date_digi_data(temp_df, report_date)
        temp_df = get_latest_data(temp_df)
        temp_df = period_change(temp_df)
        temp_df = add_report_long_names(temp_df)
        df_out = df_out.append(
            temp_df,
            ignore_index=True,
        )

    df_out["period_change"] = df_out["period_change"].fillna(0)

    return df_out


def basic_chart(df, long_name):
    df["release_int"] = (df.release_date - pd.Timestamp("2022-10-19")) // pd.Timedelta(
        "1s"
    )

    fig = px.scatter(
        df,
        x="report_date",
        y="report_data",
        trendline="lowess",
        color="release_int",
        color_continuous_scale=px.colors.sequential.YlOrRd_r,
        hover_name="report_long_name",
        hover_data={
            "release_int": False,
            "release_date": "| %b %d, %Y",
            "category": True,
        },
    )

    fig.update_layout(
        newshape=dict(line_color="yellow"),
        title=(long_name + ""),
        xaxis_title="",
        yaxis_title="",
        coloraxis_colorbar=dict(
            title="Date<br> -",
            thicknessmode="pixels",
            thickness=50,
            tickmode="array",
            tickvals=df.release_int,
            ticktext=df.release_date.dt.strftime("%m/%d/%Y"),
            ticks="inside",
        ),
    )
    # fig.show()
    return fig


def baseline_change_chart(df, long_name):
    fig = go.Figure(layout=conf
.layout)
    fig.add_traces(
        go.Scatter(
            x=df.report_date,
            y=df.relative_change,
            name="Baseline",
            line_width=2,
            fill="tozeroy",
        )
    )

    fig.add_hline(y=0, line_color="white")
    fig.update_layout(
        newshape=dict(line_color="yellow"),
        title=(long_name + " همه سفارش ها از خط پایه تغییر می کنند"),
        xaxis_title="",
        yaxis_title="",
    )
    # fig.show()
    return fig



def periodic_change_chart(df, long_name):
    fig = go.Figure(layout=conf.layout)
    fig.add_traces(
        go.Scatter(
            x=df.report_date,
            y=df.period_change,
            name="Relative",
            line_width=2,
            fill="tozeroy",
        )
    )

    fig.add_hline(y=0, line_color="white")
    fig.update_layout(
        newshape=dict(line_color="yellow"),
        title=(long_name + " تغییر از دوره قبل"),
        xaxis_title="",
        yaxis_title="",
    )
    # fig.show()
    return fig


if __name__ == "__main__":
    print("functions")
