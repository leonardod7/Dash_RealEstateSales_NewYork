
# -----------------Importanto bibliotecas------------------- #
from dash import dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash_bootstrap_templates import load_figure_template

# -----------------Importanto arquivos------------------- #
from styles.styles_graphs import *

# -----------------Importanto o template de cor------------------- #
load_figure_template(["slate"])

# -----------------Criano o Gráfico------------------- #


fig = go.Figure()
fig.update_layout(
)


# -----------------Criano o Componente------------------- #
map = dbc.Row([
            dcc.Graph(id="map-graph", figure=fig)
            ], style=map_style)







# def plot_countries_by_population(year):
#     fig = go.Figure()
#     fig.add_bar(x=year_df['Country Name'], y=year_df[year])
#     fig.layout.title = f'Top twenty countries by population - {year}'
#     fig.update_layout(
#         paper_bgcolor = "#2d3339", # cor de preenchimento do papel onde o gráfico está
#         plot_bgcolor = "#2d3339", # cor da área de plotagem do gráfico
#         title_font_color= "#ffcc00",  # cor do título
#         font_color = "#ffcc00",  # cores do eixo x e y
#         clickmode = "select", # funcionalidade para selecionar cada barra
#         colorway = ["#ffcc00"]
#     )
#
#     return fig