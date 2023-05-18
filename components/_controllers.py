
# -----------------Importanto bibliotecas------------------- #
from dash import html, dcc
import dash_bootstrap_components as dbc

# -----------------Importanto arquivos------------------- #
from styles.styles_index import *

# -----------------Tratamento de Dados------------------- #

# Essa lista são os números únicos e que representam os distritos no dataframe (coluna BOROUGH - em português, significa distritos)
list_of_locations = {
    "All": 0,
    "Manhattan": 1,
    "Bronx": 2,
    "Brooklyn": 3,
    "Queens": 4,
    "Staten Island ": 5,
}

# Nossa lista de valores para representar todas as metragens
slider_size = [100, 500, 1000, 10000, 10000000]


# -----------------Controles------------------- #
dropdown = dcc.Dropdown(
    id="location-dropdown",
    options=[{"label": i, "value": j} for i, j in list_of_locations.items()],
    value=0,
    placeholder="Select a borought", style=dropdown_style),


# -----------------Criano o Componente------------------- #
controllers = dbc.Row([
                    dbc.Col([
                        html.Div([
                            dcc.Store(id='store-global'),
                            html.H3("Real Estate Sales - NYC", style=h3_style),
                            html.P("""Vendas de imóveis da cidade de Nova York
                            período de 1 ano. """),
                            html.H4("""Distrito""", style=h4_style),
                            dcc.Dropdown(
                                id="location-dropdown",
                                options=[{"label": i, "value": j} for i, j in list_of_locations.items()],
                                value=0,
                                placeholder="Select a borought", style=dropdown_style),
                            html.Br(),
                            html.P("""Metragem (m2)""", style=p_2),
                            dcc.Slider(min=0, max=4, id='slider-square-size', value=4,
                                       marks={i: str(j) for i, j in enumerate(slider_size)}),
                            html.Br(),
                            html.P("""Variável de análise""", style=p_2),
                            dcc.Dropdown(options=[
                                {'label': 'YEAR BUILT', 'value': 'YEAR BUILT'},
                                {'label': 'TOTAL UNITS', 'value': 'TOTAL UNITS'},
                                {'label': 'SALE PRICE', 'value': 'SALE PRICE'},
                            ],value='SALE PRICE', id="dropdown-color", style=dropdown_style)
                        ], style=div_index_style)
                    ])
                ])


# TODO: para conseguirmos preencher de amarelo dentro do dropdown sem extrapolar a largura do botão, colocamos o dropdown, assim como todos os elementos dentro de uma html.Div