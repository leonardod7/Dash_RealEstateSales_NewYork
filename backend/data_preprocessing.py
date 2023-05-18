##
import pandas as pd

df_data = pd.read_csv("dataset/cleaned_data.csv", index_col=0)
print(df_data)

# Vamos calcular duas variáveis, latitude e longitude média, para conseguirmos centralizar o nosso mapa naquele ponto
mean_lat = df_data["LATITUDE"].mean()
mean_long = df_data["LONGITUDE"].mean()

# Metragem em pé-quadrado para metro quadrado
df_data["size_m2"] = df_data["GROSS SQUARE FEET"] / 10.764

# Vamos excluir valores que não possuem ano
df_data = df_data[df_data["YEAR BUILT"] > 0]

# Formatando a coluna de data como datetime. O pandas originalmente reconheceu ela como string (objeto). Substituímos essa formatação de coluna nela mesmo
df_data["SALE DATE"] = pd.to_datetime(df_data["SALE DATE"])

# Alguns imóveis estão com metragem muito grande. Esse conjunto de dados vai desde a venda de kitnets até pavilhões gigantescos, estádios de futebol
# Dessa forma, esses valores extremos causam uma distorção na visualização e comparação dos dados.
# Vamos assumir algumas premissa:

# Quando a metragem for maior que 10.000, diremos que é 10.000
df_data.loc[df_data["size_m2"] > 10000, "size_m2"] = 10000

# Quando o preco for maior que 50 milhões, o preço será 50 milhões
df_data.loc[df_data["SALE PRICE"] > 50000000, "SALE PRICE"] = 50000000

# Quando o preco for menor que 10 mil dólares, o preço será 10 mil dólares
df_data.loc[df_data["SALE PRICE"] < 100000, "SALE PRICE"] = 100000
