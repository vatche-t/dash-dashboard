import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from datetime import date
from functions import logic as log
from conf import configs as conf
from functions import functions as func
import dash_auth
from sales_page import sales
from buy_box_pages import buy_box_variants
from order_page import order 
from users import USERNAME_PASSWORD_PAIRS

#stylemodifications

CONTENT_STYLE = {
    "margin-left": "2rem",
    "margin-right": "2rem",
}

TEXT_STYLE = {"textAlign": "center"}

DROPDOWN_STYLE = {"textAlign": "left"}


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
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("صفحه بای باکس ", href='/buy_box'),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("صفحه سفارشات ", href='/orders'),
            ],
        ),
    ],
    brand="صفحه اصلی",
    brand_href="/",  
    sticky="top",  
    color="dark",  
    dark=True,  
)



#DropDown - Datepicker
report_select = dbc.Row(
    [
        dbc.Col(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            id="report",
                            options=[
                                {
                                    "label": label,
                                    "value": value,
                                }
                                for value, label in log.digi_list_abbrev.items()
                            ],
                     
                            value="all_orders",
                        ),
                    ],
                    className="dash-bootstrap",
                ),
            ],
            md=6,
        ),
        dbc.Col(
            [
                html.Div(
                    [
                        dcc.DatePickerSingle(
                            id="start-date",
                            min_date_allowed=date(2022, 10, 19),
                            initial_visible_month=date(2022, 11, 5),
                            date=date(2022, 10, 19),
                        ),
                    ],
                    className="dash-bootstrap",
                )
            ],
            
            md=2,
        ),
    ]
)



info_bar = html.Div(
    id="summary",
)


basic_data = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="basic-chart",
                style={"height": "70vh"},
                config=conf.tool_config,
            ),
            md=12,
        ),
    ]
)


baseline_data = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="change-from-baseline-chart",
                style={"height": "70vh"},
                config=conf.tool_config,
            ),
            md=6,
        ),
        dbc.Col(
            dcc.Graph(
                id="change-from-period-chart",
                style={"height": "70vh"},
                config=conf.tool_config,
            ),
            md=6,
        ),
    ]
)




#Layout

main_page = html.Div(
    [
        html.Hr(),
        html.H4(" آنالیز آمار کتاب کالا", style=TEXT_STYLE),
        html.Hr(),
        navbar,
        html.Hr(),
        report_select,
        html.Hr(),
        info_bar,
        html.Hr(),
        basic_data,
        html.Hr(),
        baseline_data,
        html.Hr(),
        html.H5(" مقایسه آمار کتاب کالا", style=TEXT_STYLE),
        html.Hr(),
    ],
    style=CONTENT_STYLE,
)


#App

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.CYBORG],
)
app.config.suppress_callback_exceptions = True
app.title = " آنالیز آمار کتاب کالا"
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)
auth = dash_auth.BasicAuth(
    app,
    USERNAME_PASSWORD_PAIRS
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == '/sales':
        return sales()
    if pathname == '/buy_box':
        return buy_box_variants()
    if pathname == '/orders':
        return order()
    else:
        return main_page


 
#scatterPLot
@app.callback(
    dash.dependencies.Output("basic-chart", "figure"),
    [
        dash.dependencies.Input("report", "value"),
        dash.dependencies.Input("start-date", "date"),
    ],
)
def basic_report(report, init_date):
    #date
    if init_date is not None:
        date_object = date.fromisoformat(init_date)
        date_string = date_object.strftime("%Y-%m-%d")

    # Filter
    df = func.get_report_from_digi_data(log.digi_df, report)
    df1 = func.get_report_after_date_digi_data(df, date_string)

    df2 = func.get_release_after_date_digi_data(df1, date_string)

   
    df2 = func.add_report_long_names(df2)
    long_name = df2.report_long_name.iloc[0]

    fig = func.basic_chart(df2, long_name)
    return fig


# Baseline Chart 
@app.callback(
    dash.dependencies.Output("change-from-baseline-chart", "figure"),
    [
        dash.dependencies.Input("report", "value"),
        dash.dependencies.Input("start-date", "date"),
    ],
)
def change_from_baseline_report(report, init_date):
    if init_date is not None:
        date_object = date.fromisoformat(init_date)
        date_string = date_object.strftime("%Y-%m-%d")

    df = func.get_report_from_digi_data(log.digi_df, report)
 #برای کارکرد از روی تاریخ انتخاب شده
    df1 = func.get_report_after_date_digi_data(df, date_string)
    df2 = func.get_latest_data(df1)
    df2 = func.period_change(df2)
    df2 = func.add_report_long_names(df2)
    long_name = df2.report_long_name.iloc[0]
    fig = func.baseline_change_chart(df2, long_name)

    return fig


@app.callback(
    dash.dependencies.Output("change-from-period-chart", "figure"),
    [
        dash.dependencies.Input("report", "value"),
        dash.dependencies.Input("start-date", "date"),
    ],
)
def change_from_period_report(report, init_date):
    if init_date is not None:
        date_object = date.fromisoformat(init_date)
        date_string = date_object.strftime("%Y-%m-%d")
#برای کارکرد از روی تاریخ انتخاب شده
    df = func.get_report_from_digi_data(log.digi_df, report)
    df1 = func.get_report_after_date_digi_data(df, date_string)
    df2 = func.get_latest_data(df1)
    df2 = func.period_change(df2)
    df2 = func.add_report_long_names(df2)
    long_name = df2.report_long_name.iloc[0]

    fig = func.periodic_change_chart(df2, long_name)
    return fig



# Period Chart
@app.callback(
    dash.dependencies.Output("category-period-chart", "figure"),
    [
        dash.dependencies.Input("report", "value"),
        dash.dependencies.Input("start-date", "date"),
    ],
)
def category_period_report(report, init_date):
    if init_date is not None:
        date_object = date.fromisoformat(init_date)
        date_string = date_object.strftime("%Y-%m-%d")

 
    fig = func.category_chart_perodic(log.digi_df, report, date_string)

    return fig



@app.callback(
    dash.dependencies.Output("category-baseline-chart", "figure"),
    [
        dash.dependencies.Input("report", "value"),
        dash.dependencies.Input("start-date", "date"),
    ],
)
def category_baseline_report(report, init_date):
    if init_date is not None:
        date_object = date.fromisoformat(init_date)
        date_string = date_object.strftime("%Y-%m-%d")

    fig = func.category_chart_baseline(log.digi_df, report, date_string)

    return fig


@app.callback(
    dash.dependencies.Output("summary", "children"),
    [dash.dependencies.Input("report", "value")],
)
def dashboard_summary_numbers(report):

    df1 = func.get_report_from_digi_data(log.digi_df, report)


    df2 = df1.iloc[-1:]


    return html.Div(
        dbc.Row(
            [
                dbc.Col(
                    dbc.Alert(
                        [
                            html.H6("آخرین تاریخ: "),
                            html.H6(df2.report_date.dt.strftime("%m/%d/%Y")),
                        ],
                        color="light",
                    ),
                    md=2,
                ),
                dbc.Col(
                    dbc.Alert(
                        [
                            html.H6("آخرین نسخه: "),
                            html.H6(df2.release_date.dt.strftime("%m/%d/%Y")),
                        ],
                        color="success",
                    ),
                    md=2,
                ),
                dbc.Col(
                    dbc.Alert(
                        [
                            html.H6("آخرین داده ها: "),
                            html.H6(df2.report_data),
                        ],
                        color="primary",
                    ),
                    md=2,
                ),
            ]
        )
    )





if __name__ == "__main__":
 
    app.run_server(debug=False, host="0.0.0.0", port=80, dev_tools_hot_reload=True)

