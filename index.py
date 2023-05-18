
# Importanto bibliotecas ==============================================================================================
from dash.dependencies import Input, Output
import dash_mantine_components as dmc
import plotly.express as px
from app import app
import numpy as np

# Importanto Arquivos =================================================================================================
from components._map import *
from components._histogram import *
from components._controllers import *
from backend.data_preprocessing import *


# Importanto o Template ===============================================================================================
load_figure_template(["slate"])


# app =================================================================================================================
app.layout = dbc.Container([

        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Img(className="logoD7", src=app.get_asset_url("logoD7PAR_Branca.png"), style=logoD7_Style),
                    html.H1('Business Transformation - Business Modelling',style=h1_1_style),
                    html.H1('Corporate Finance & Artificial Intelligence', style=h1_2_style),
                    html.H2('Data Science Team', style=h2_1_style),
                        ]) #style={'position': 'fixed', 'top':0, 'letf':0, 'z-index': 1 }
                    ], md=12, style={'margin-left': '0%'})
                ]),
        html.Hr(style=hr_1_styles),

        dbc.Row([
            dbc.Col([
                html.Div(children=[
                    dbc.Row([
                        dbc.Col([controllers], md=3),
                        dbc.Col([
                            dbc.Row(
                                html.Div([map], style=div_map)
                                    ),
                            html.Br(),
                            dbc.Row(
                                html.Div([hist])
                                    ),
                            ],md=9)
                            ])
                        ])
                    ], md=12)
                ]),

        html.Hr(style=hr_1_styles),

        dbc.Row([
            dbc.Col([
                dmc.Blockquote("Everything we hear is an opinion, not a fact. Everything we see is a perspective, not the truth.",
                               cite="- Marcus Aurelius , Meditations", style=blockquote_style)
                    ], md=12)
                ]),
        ], fluid=True)


# Callbacks ===========================================================================================================
@app.callback([Output(component_id='hist-graph', component_property='figure'),
                Output(component_id='map-graph', component_property='figure')],
                [Input(component_id='location-dropdown', component_property='value'), # Estamos pegando o valor do primeiro dropdonw
                Input(component_id='slider-square-size', component_property='value'), # Estamos pegando o valor do slider
                Input(component_id='dropdown-color', component_property='value'), # Estamos pegando o valor do segundo dropdown
])
def update_hist(location, square_size, color_map):
    if location is None:
        df_intermediate = df_data.copy()
    else:
        size_limit = slider_size[square_size] if square_size is not None else df_data["GROSS SQUARE FEET"].max()
        df_intermediate = df_data[df_data["BOROUGH"] == location] if location != 0 else df_data.copy()
        df_intermediate = df_intermediate[df_intermediate["GROSS SQUARE FEET"] <= size_limit]

# Histogram ===========================================================================================================
    hist_fig = px.histogram(data_frame=df_intermediate,
                            x=color_map,
                            opacity=0.9,
                            nbins=70,
                            color_discrete_sequence=["#ffcc00"],# cor das barras
                            title="Distribuição")
    hist_fig.update_layout(
        showlegend=False,
        title_font_color="#ffcc00",  # cor do título
        font_color="#ffcc00",  # cores do eixo x e y
        paper_bgcolor='rgba(0,0,0,0)'
        )

# Map =================================================================================================================
    px.set_mapbox_access_token(open("keys/mapbox_key").read()) # inserimos a chave de acesso para uso do mapbox

    # O grande objetivo dos ajustes de cores abaixo é deixarmos a distribuição de cores mais homogenea, mais agradável de visualizar
    colors_rgb = px.colors.sequential.Cividis
    df_quantiles = df_data[color_map].quantile(np.linspace(0, 1, len(colors_rgb))).to_frame() # criando uma escala
    df_quantiles = round((df_quantiles - df_quantiles.min()) / (df_quantiles.max() - df_quantiles.min()) * 10000) / 10000 # Normalizando os dados
    # df_quantiles.iloc[-1] = 1
    df_quantiles["colors"] = colors_rgb
    df_quantiles.set_index(color_map, inplace=True)
    color_scale = [[i, j] for i, j in df_quantiles["colors"].iteritems()]

    map_fig = px.scatter_mapbox(df_intermediate, title= 'Mapa de Imóveis no Distrito de Nova York',
                                lat="LATITUDE", lon="LONGITUDE", color=color_map, size="size_m2",
                                size_max=20, zoom=10, opacity=0.4)

    map_fig.update_coloraxes(colorscale=color_scale)
    map_fig.update_layout(mapbox=dict(center=go.layout.mapbox.Center(lat=mean_lat, lon=mean_long)),
            title_font_color="#ffcc00",  # cor do título
            paper_bgcolor='rgba(0,0,0,0)')

# return da Função ====================================================================================================
    return hist_fig, map_fig



if __name__ == '__main__':
    app.run_server(debug=True)























# TODO: color scale:
#  source: https://plotly.com/python/builtin-colorscales/


# TODO: Map: Conseguimos crirar mapas sem se cadastrar e usar o mapbox, porém, não ficam tão bonitos!
# Para viabilizar, criamos uma pasta keys que conterá um arquivo sem extensão com a chave
# source: https://www.mapbox.com
# key source: https://account.mapbox.com
# TODO: A definição dessa regra permite que ele possa plotar os pontos do gráfico e viabilizar o desenho:
#  px.set_mapbox_access_token(open("keys/mapbox_key").read()) # inserimos a chave de acesso para uso do mapbox
# size="size_m2": coluna que ele vai utlizar para se referenciar em temros de size
# map_fig.update_layout(mapbox=dict(center=go.layout.mapbox.Center(lat=mean_lat, lon=mean_long)): Qual latitude e longitude para centralizarmos o gráfico
# colorcar fundo do mapa transparente: paper_bgcolor='rgba(0,0,0,0)'     source: https://stackoverflow.com/questions/29968152/setting-background-color-to-transparent-in-plotly-plots


# TODO: IMPORTANTE: @app.callback([Output(component_id='hist-graph', component_property='figure')],
# Quando definimos que o Output retornará uma lista de Outputs (pois ele esta dentro dos colchetes, o return da função no caso vai esperar que tenham mais elementos de retorno e não somente 1.
# Observe que ao fazermos o return hist_fig, como passamos o output dentro de uma lista, ele espera que passamos mais de um elemento de retorno no return.

# @app.callback([Output(component_id='hist-graph', component_property='figure')],
#               [Input(component_id='location-dropdown', component_property='value'),
#               .......
# ])
# def update_hist(location, square_size, color_map):
#     ....
#     return hist_fig

# Para resolvermos isso, quando temos apenas um retorno (return de 1 elemento), devemos tirar o Output de entro da lista
# @app.callback(Output(component_id='hist-graph', component_property='figure'),
#               [Input(component_id='location-dropdown', component_property='value'),
#               .......
# ])
# def update_hist(location, square_size, color_map):
#     ....
#     return hist_fig
#
# Se não fizermos esse ajuse, ele estará iterando por uma lista



# TODO: def update_hist(location, square_size, color_map): Essa função vai permitir saber que tipo de gráfico queremos utilizar
# square_size = tamaho do apartamento, color_map: cores do gráfico
# Observe que Location aparece dentro do dropbox como do tipo string. Porém, quando formos trabalhar com essa informação, precisaremos trabalhar com a variável do tipo numérica
# Uma coisa importante a ressaltar é que sempre que o dash é inicializado, ele faz com que todas as funções sejam inicializadas, ele joga os valores para cada uma delas e testa a execução delas.
# No começo das funções nem sempre as variáveis já estão definidas. As vezes, elas são passadas como NONE. Então precisamos lidar com essa forma dentro da função, para que toda vez que elas forem passadas não retornar nenhum tipo de erro.

# TODO: size_limit = slider_size[square_size] if square_size is not None else df_data["GROSS SQUARE FEET"].max(): Vai receber a posição que foi passada no square_size
#  quando passamos slider_size[square_size] estamos pegando a posição dos valores
# no slider, pois no slider temos 0, 1, 2, 3, 4

# TODO: margin=go.layout.Margin(l=10, r=0, t=0, b=50):
# l: left; r: right; t: top; b: bottom
# Observe que em map, foi usado a seguinte forma: fig.update_layout(template="slate"). Nesse caso do histograma, está sendo feito uma outra forma ( com o objetivo de mostrar que temos outra opção)
# mas poderíamos fazer o mesmo formato que o do map.
# Abaixo, opçõs de layout:

# fig = go.Figure()
#     fig.update_layout(template="slate")
#
# hist_fig = px.histogram(df_intermediate, x=color_map, opacity=0.75)
# hist_layout = go.Layout(
#     margin=go.layout.Margin(l=10, r=0, t=0, b=50),
#     showlegend=False,
#     template="plotly_dark",  # slate
#     paper_bgcolor="rgba(0, 0, 0, 0)")
# hist_fig.layout = hist_layout

# TODO: Esse update vai receber o localion (primeiro dropdown), a metragem (slider) e a variável de analise (dropdown)

# def update_hist(location, square_size, color_map):
#     if location is None:
#         df_intermediate = df_data.copy()



# TODO: Histograma
# # poderíamos colocar: paper_bgcolor = "rgba(0, 0, 0, 0)"
# # margin=go.layout.Margin(l=10, r=0, t=0, b=50),
# # paper_bgcolor = "#2d3339",  # cor de preenchimento do papel onde o gráfico está
# # plot_bgcolor = "#2d3339",  # cor da área de plotagem do gráfico
# # title_font_color = "#ffcc00",  # cor do título
# # font_color = "#ffcc00",  # cores do eixo x e y
# # clickmode = "select",  # funcionalidade para selecionar cada barra
# # colorway = ["#ffcc00"],


# TODO: surce:
#  Plotly: https://plotly.com/python/histograms/
# Para usarmos o mapa dessa aplicação, deveremos utilizar o link do mapbox para pegar a chave de acesso:
# Mapbox: https://account.mapbox.com
# Dependendo da quantidade de requisições, pode ser que ele peça uma licença paga