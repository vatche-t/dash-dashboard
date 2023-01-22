from dash import html
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from datetime import date
from functions import logic as log
from conf import configs as conf
from functions import function_buy_box as func
import dash_auth
from users import USERNAME_PASSWORD_PAIRS

def buy_box_variants():


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





    basic_data = dbc.Row(
        [
            dbc.Col(
                dcc.Graph(
                    figure=func.buy_box(),
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
            html.H4(" آنالیز بای باکس کتاب کالا", style=TEXT_STYLE),
            html.Hr(),
            navbar,
            html.Hr(),
            basic_data,
            html.Hr(),
            html.Hr(),
            html.H5(" مقایسه بای باکس کتاب کالا", style=TEXT_STYLE),
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
    app.title = "Ketabkala آنالیز آمار"
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
        if pathname == '/buy_box':
            return buy_box_variants()
        else:
            return main_page


    @app.callback(Output('buy_box', 'figure'), Input('intermediate-value','data'))
    def update_graph(df):
        
        df = func.get_digi_data
        
        fig = func.buy_box
        return fig

       

    return main_page