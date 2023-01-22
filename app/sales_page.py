from dash import html
import dash
from dash import html
from dash import dcc
from dash import dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from datetime import date
from functions import logic as log
from conf import configs as conf
from functions import function_sales as func
import dash_auth
from users import USERNAME_PASSWORD_PAIRS


def sales():


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
                    dbc.DropdownMenuItem("صفحه فروش", href='/sales_page'),
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

    # table = dash_table.DataTable(
    #     id = 'table',
    #     columns = [{"name": i, "id": i} for i in func.sold_table().columns],
    #     data = func.sold_table().to_dict('records'),
    # )
    
    
    table = dbc.Table.from_dataframe(func.sold_table(),
                      bordered=True,
                      index=True)

    info_bar = html.Div(
        id="summary",
    )


    basic_data = dbc.Row(
        [
            dbc.Col(
                dcc.Graph(
                    figure=func.lost_chart(),
                    id="buy_box",
                    style={"height": "70vh"},
                    config=conf.tool_config,
                ),
                md=12,
            ),
        ]
    )




    #Layout

    main_page = html.Div(
        [
            html.Hr(),
            html.H4(" آنالیز فروش کتاب کالا", style=TEXT_STYLE),
            html.Hr(),
            navbar,
            html.Hr(),
            table,
            html.Hr(),
            basic_data,
            html.Hr(),
            html.Hr(),
            html.H5(" مقایسه فروش کتاب کالا", style=TEXT_STYLE),
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
        if pathname == '/sales_page':
            return sales()
        else:
            return main_page


    
    # #scatterPLot
    # @app.callback(
    #     dash.dependencies.Output("basic-chart", "figure"),
    #     [
    #         dash.dependencies.Input("report", "value"),
    #         dash.dependencies.Input("start-date", "date"),
    #     ],
    # )
    # def basic_report():
    #     fig = func.basic_chart()
    #     return fig

   

    return main_page


