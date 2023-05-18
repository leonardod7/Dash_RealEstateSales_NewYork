
# -----------------Importanto bibliotecas------------------- #
from dash import dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash_bootstrap_templates import load_figure_template


# -----------------Importanto arquivos------------------- #
from styles.styles_graphs import *


# Importando o Template---------------------------------------------------------------------------------------------- #
load_figure_template(["slate"])


# Criano a figura e Instânciando ele-------------------------------------------------------------------------------- #
def fig_hist():
    fig = go.Figure()
    fig.update_layout()
    return fig

fig_hist = fig_hist()


# -----------------Criano o Componente------------------- #
hist = dbc.Row([
            dcc.Graph(id="hist-graph", figure=fig_hist)
            ], style=hist_style)






# TODO: Observe que estamos apenas criando a figura e colocando ela posicionada na linha. Não estamos criando o gráfico, muito menos formatando ele

