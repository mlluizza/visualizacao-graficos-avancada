import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc

df = pd.read_csv('ecommerce_estatistica.csv')

df['Qtd_Vendidos'] = pd.to_numeric(df['Qtd_Vendidos'], errors='coerce').fillna(0).astype(int)

# Gráfico de Histograma 
fig1 = px.histogram(df, x='Nota', nbins=20, title='Distribuição das Notas de Avaliação')

#Gráfico de Dispersão
fig2 = px.scatter(df, x='Preço', y='Nota', size='Qtd_Vendidos', color='Marca', title='Nota vs Preço (tamanho indica quantidade vendida)', hover_data=['Título'])

# Gráfico de calor
corr = df[['Nota', 'Preço', 'Desconto', 'N_Avaliações', 'Qtd_Vendidos']].corr()
fig3 = px.imshow(corr, text_auto=True, aspect="auto",
                        title='Mapa de Calor: Correlação entre Variáveis')
fig3.update_layout(
    xaxis_title='Variável', 
    yaxis_title='Variável')

# Gráfico de barras
fig4 = px.bar(df.groupby('Marca')['Qtd_Vendidos'].sum().reset_index().sort_values(by='Qtd_Vendidos', ascending=False).head(10), x='Marca', y='Qtd_Vendidos', title='Top 10 Marcas mais Vendidas')

# Gráfico de Pizza
fig5 = px.pie(df, names='Gênero',title='Distribuição por Gênero')
fig5.update_traces(textposition='inside', textinfo='percent+label')

# Gráfico de Regressão
fig6 = px.scatter(df, x='Preço', y='Nota', trendline='ols',
                     title='Regressão Linear: Preço vs Nota')
fig6.update_layout(
    xaxis_title='Preço',
    yaxis_title='Nota Média')



# Criação do app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Visualização de Dados"),
    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig2),
    dcc.Graph(figure=fig3),
    dcc.Graph(figure=fig4),
    dcc.Graph(figure=fig5),
    dcc.Graph(figure=fig6)
])

if __name__ == '__main__':
    app.run(debug=True, port=8050)
