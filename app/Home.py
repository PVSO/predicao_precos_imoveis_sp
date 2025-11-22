import os
import pandas as pd
import plotly.express as px
import streamlit as st

caminho_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
caminho_arquivo = os.path.join(caminho_base, 'data', 'processed', 'dados.parquet')
df = pd.read_parquet(caminho_arquivo)

st.set_page_config(
    page_title='Dashboard de compra e venda de imóveis na cidade de São Paulo',
    page_icon='📚',
    layout='wide',
    initial_sidebar_state='collapsed'
)

st.title("🎲 Dashboard de Análise de compra e venda de imóveis na cidade de São Paulo")
st.markdown("Explore os dados de de compra e venda de imóveis na cidade de São Paulo.")

st.markdown('---')

if not df.empty:
    total_transacoes = df.shape[0]
    valor_medio_transacao = df['valor_transacao'].mean().round(2)
    total_distritos = len(df['distrito'].unique())

    financiamentos_nao_desejados = ['Não Informado', '0.Não_informado']

    # Filtra o DataFrame, mantendo apenas os tipos de financiamento conhecidos
    df_ativo = df.loc[~df['tipo_financiamento'].isin(financiamentos_nao_desejados)].copy()

    df_financiamentos_agregado = df_ativo.groupby('tipo_financiamento')['valor_transacao'].sum().reset_index()
    df_financiamentos_agregado.columns = ['Tipo de Financiamento', 'Valor Total Transacionado']

    # Classifica para melhor visualização (do maior para o menor)
    df_financiamentos_agregado = df_financiamentos_agregado.sort_values(by='Valor Total Transacionado', ascending=False)

    financiamento_principal = df_financiamentos_agregado['Valor Total Transacionado'].idxmax()

    # Usa o índice para buscar os valores na linha correspondente
    nome_financiamento_principal = df_financiamentos_agregado.loc[financiamento_principal, 'Tipo de Financiamento']

else:
    total_transacoes, valor_medio_transacaot, total_distritos, nome_financiamento_principal = '', '', '', ''

col1, col2, col3 = st.columns(3)
col4 = st.container()
col1.metric("Total de Transações", f"{total_transacoes}")
col2.metric("Valor Médio de Transação", f"R$ {valor_medio_transacao}")
col3.metric("Total de distritos", f"{total_distritos}")
col4.metric("Principal meio de financiamento", f"{nome_financiamento_principal}")

st.markdown('---')

col_graf = st.container()
col_graf1, col_graf2 = st.columns(2)
col_graf3, col_graf4 = st.columns(2)

with col_graf:
    if not df.empty:
        GRUPO_RESIDENCIAL = [
            'RESIDENCIA', 'APTO_CONDO_FRACAO', 'CORTIÇO', 'GARAGEM_UA_COND_RES',
            'RESIDENCIA_COLETIVA', 'MISTO_PREDOM_RESID', 'PREDIO_RESIDENCIAL',
            'FLAT_RESIDENCIAL', 'PREDIO_APTO_S_CONDO_MISTO_RES'
        ]

        GRUPO_INDUSTRIAL = [
            'INDÚSTRIA', 'ARMAZÉNS_DEPOSITOS', 'OFICINA', 'POSTO DE SERVIÇO'
        ]

        def simplificar_uso(uso):
            if uso in GRUPO_RESIDENCIAL:
                return 'RESIDENCIAL'
            elif uso in GRUPO_INDUSTRIAL:
                return 'INDUSTRIAL'
            else:
                return 'OUTROS'

        df['grupo'] = df['desc_uso_IPTU'].apply(simplificar_uso)

        df_filtrado = df[df['grupo'].isin(['RESIDENCIAL', 'INDUSTRIAL'])].copy()

        df_filtrado['razao_area'] = df_filtrado['area_construida_m²'] / df_filtrado['area_terreno_m²']

        df_distrito = df_filtrado.groupby(['distrito', 'grupo']).agg(
            valor_medio_transacao=('valor_transacao', 'mean'),
            razao_area_media=('razao_area', 'mean')
        ).reset_index()

        fig = px.scatter(
            df_distrito,
            x='razao_area_media',
            y='valor_medio_transacao',
            color='grupo',       # Cor por uso (Residencial vs Industrial)
            size='valor_medio_transacao', # O tamanho do ponto reflete o Valor Médio (ênfase)
            hover_data=['grupo', 'valor_medio_transacao', 'razao_area_media'],
            title='Hipótese 1: Valor Médio de Transação vs. Razão Média Área Construída/Terreno',
            labels={
                'razao_area_media': 'Razão Média (Área Construída / Terreno)',
                'valor_medio_transacao': 'Valor Médio de Transação (R$)',
                'grupo': 'Grupo de Imóveis'
            },
            color_discrete_map={'RESIDENCIAL': '#005f73', 'INDUSTRIAL': '#ae2012'}, # Cores personalizadas
            trendline='ols',
        )

                
        fig.update_layout(
            margin=dict(
                t=80, b=150
            ),
            yaxis=dict(
                zeroline=True,
                zerolinecolor='black',
                zerolinewidth=1.5,
            ),
            xaxis=dict(
                zeroline=True,
                zerolinecolor='black',
                zerolinewidth=1.5,
            )
        )

        fig.add_annotation(
            text= "A hipótese é FALSA, pois:<br>A dispersão de imóveis Industriais acima de imóveis Residenciais mostra que os imóveis Industriais podem transacionar<br>por um valor significamente maior do que imóveis Residenciais na maioria dos distritos",
            xref="paper", yref="paper",
            x=0, y=-0.5,  # posição abaixo do gráfico
            showarrow=False,
            font=dict(size=12),
            align="left"
        )

        st.plotly_chart(fig, use_container_width=True, key='Gráfico do Valor Médio de Transação vs. Razão Média Área Construída/Terreno')

    else:
        st.warning('Não foi possível exibir o gráfico da Hipótese 1')

with col_graf1:
    if not df.empty:
        
        limite_area = 200

        def categorizar_area(area):
            if area > limite_area:
                return f'Acima de {limite_area} m²'
            else:
                return f'Até {limite_area} m²'

        df['categoria_area'] = df['area_construida_m²'].apply(categorizar_area)

        # Agrega o Fato: Calcula o Valor Médio da Transação para cada categoria
        df_agregado = df.groupby('categoria_area')['valor_transacao'].mean().reset_index()
        df_agregado.columns = ['Categoria de Área', 'Valor Médio de Transação']

        # Ordena o DataFrame para melhor visualização (Geralmente a categoria menor vem primeiro)
        df_agregado = df_agregado.sort_values(by='Valor Médio de Transação', ascending=False)

        df_agregado['Valor Médio de Transação BR'] = df_agregado['Valor Médio de Transação'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

        fig = px.bar(
            df_agregado,
            x='Categoria de Área',
            y='Valor Médio de Transação',
            color='Categoria de Área',
            title=f'Valor Médio de Transação por Área Construída',
            text='Valor Médio de Transação BR',
            labels={
                'Valor Médio de Transação': 'Valor Médio de Transação (R$)',
                'Categoria de Área': 'Tamanho do Imóvel'
            },
            color_discrete_map={
                f'Acima de {limite_area} m² (Grande)': '#0077b6',
                f'Até {limite_area} m² (Pequeno/Médio)': '#90e0ef'
            }
        )

        fig.update_layout(
            margin=dict(
                t=80,b=150
            ),
            yaxis_tickformat='.2s', # Formata o eixo Y em notação abreviada (ex: 1M para 1.000.000)
            hovermode='x unified',
            yaxis=dict(
                showgrid=True,
                gridcolor='black',
                gridwidth=1,
                range=[0, df_agregado['Valor Médio de Transação'].max() * 1.2],
                zeroline=True,
                zerolinecolor='black',
                zerolinewidth=1.5,
            )
        )
        fig.add_annotation(
            text= "A hipótese é VERDADEIRA, pois:<br>A média do valor de transação para imóveis com area construida acima de 200m² é R$ 15.462,94<br>maior do que para imóveis com área construída menor",
            xref="paper", yref="paper",
            x=0, y=-0.5,  # posição abaixo do gráfico
            showarrow=False,
            font=dict(size=12),
            align="left"
        )

        # Define o formato do eixo Y para R$
        fig.update_yaxes(
            tickprefix='R$ '
        )
        st.plotly_chart(fig, use_container_width=False, key='Gráfico do Valor Médio de Transação por Área Construída')

    else:
        st.warning('Não foi possível exibir o gráfico da Hipótese 2')

with col_graf2:
    if not df.empty:
        # Hipótese 3. A soma do valor de transacao (total transacionado) por tipo de financiamento
        # 'Minha Casa Minha Vida' é maior do que as transações dos outros tipos de financiamento.

        # Selecionando apenas os tipos_financiamento conhecidos
        financiamentos_nao_desejados = ['Não Informado', '0.Não_informado']

        # Filtra o DataFrame, mantendo apenas os tipos de financiamento conhecidos
        df_ativo = df.loc[~df['tipo_financiamento'].isin(financiamentos_nao_desejados)].copy()

        df_financiamentos_agregado = df_ativo.groupby('tipo_financiamento')['valor_transacao'].sum().reset_index()
        df_financiamentos_agregado.columns = ['Tipo de Financiamento', 'Valor Total Transacionado']

        # Classifica para melhor visualização (do maior para o menor)
        df_financiamentos_agregado = df_financiamentos_agregado.sort_values(by='Valor Total Transacionado', ascending=False)

        df_financiamentos_agregado['Valor Total Transacionado BR'] = df_financiamentos_agregado['Valor Total Transacionado'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

        fig = px.bar(
            df_financiamentos_agregado,
            x='Tipo de Financiamento',
            y='Valor Total Transacionado',
            title='Valor Total Transacionado por Tipo de Financiamento',
            text='Valor Total Transacionado BR'
        )

        fig.add_annotation(
            text= "A hipótese é FALSA, pois:<br>O tipo de financiamento que possui o maior valor total transacionado é o Sistema Financeiro de Habitação<br><br>OBS:<br>Além dos tipos de financiamentos apresentados no gráfico, a base de dados apresentou 85031 registros sem valor categorizados como 'Não Informado', que gerou<br>um valor total transacionado de R$ 26.526.964.157,70.<br>Essa 'categoria' de financiamento não foi plotada a fim de garantir uma comparação mais fiel e focada nos tipos de financiamento ativos e conhecidos",
            xref="paper", yref="paper",
            x=0, y=-1.1,  # posição abaixo do gráfico
            showarrow=False,
            font=dict(size=12),
            align="left"
        )

        fig.update_layout(
            margin=dict(
                t=90, b=200
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='black',
                gridwidth=1,
                range=[0, df_financiamentos_agregado['Valor Total Transacionado'].max() * 1.2],
                zeroline=True,
                zerolinecolor='black',
                zerolinewidth=1.5,
            )
        )

        # Adiciona formatação monetária ao texto da barra do eixo Y
        fig.update_yaxes(
            tickprefix='R$ '
        )

        st.plotly_chart(fig, use_container_width=False, key='Gráfico do Valor Total Transacionado por Tipo de Financiamento')

    else:
        st.warning('Não foi possível exibir o gráfico da Hipótese 3')

with col_graf3:
    if not df.empty:
        # Hipótese 4. Qual tipo de imóvel representa o maior valor de transação médio, e quais são
        # os tipos mais frequentes nas transações?

        tipos_validos = df['desc_uso_IPTU'].value_counts().nlargest(10).index # Pegando os 10 mais frequentes
        df_analise = df[df['desc_uso_IPTU'].isin(tipos_validos)].copy()

        # 3. Calcular as Métricas
        # Usamos o 'median' (mediana) para o preço, pois é mais robusto que a média em preços de imóveis.
        analise_tipo = df_analise.groupby('desc_uso_IPTU').agg(
            valor_medio=('valor_transacao', 'median'),
            frequencia=('id_iptu', 'count')
        ).reset_index()

        # 4. Calcular Frequência Percentual (para rótulos)
        total_transacoes = analise_tipo['frequencia'].sum()
        analise_tipo['percentual'] = (analise_tipo['frequencia'] / total_transacoes) * 100

        analise_tipo['valor_medio_BR'] = analise_tipo['valor_medio'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

        # 5. Ordenar o DataFrame pelo Valor Médio (para visualização)
        analise_tipo = analise_tipo.sort_values(by='valor_medio', ascending=False)

        analise_tipo.columns = [
            'desc_uso_IPTU', 'Valor Médio de Transação', 'frequencia', 'percentual', 'valor_medio_BR'
        ]

        # ----------------------------------------------------
        # 📊 Geração do Gráfico com Plotly
        # ----------------------------------------------------

        # Criação do gráfico de barras (Valor Médio)
        fig = px.bar(
            analise_tipo,
            x='desc_uso_IPTU',
            y='Valor Médio de Transação',
            text='valor_medio_BR',
            title='Valor Mediano de Transação por Tipo de Imóvel e Frequência de Vendas',
            labels={
                'desc_uso_IPTU': 'Tipo de Imóvel (Uso IPTU)',
            },
        )

        # Ajuste fino para os eixos e rótulos
        fig.update_layout(
            xaxis={'categoryorder':'total descending'},
            yaxis_tickformat='.2s', # Formata o eixo Y em notação abreviada (ex: 1M para 1.000.000)
            hovermode='x unified',
            yaxis=dict(
                showgrid=True,
                gridcolor='black',
                gridwidth=1,
                range=[0, analise_tipo['Valor Médio de Transação'].max() * 1.2],
                zeroline=True,
                zerolinecolor='black',
                zerolinewidth=1.5,
            )
        )
        st.plotly_chart(fig, use_container_width=False, key='Gráfico do Valor Mediano de Transação por Tipo de Imóvel e Frequência de Vendas')

    else:
        st.warning('Não foi possível exibir o gráfico da Hipótese 4')

with col_graf4:
    if not df.empty:
        # Hipótese 5. O mês de dezembro apresenta um número maior transações em comparação com os demais
        # meses do ano.

        # convertendo o tipo de data_transacao para datetime
        df['data_transacao'] = pd.to_datetime(df['data_transacao'])

        df['mes'] = df['data_transacao'].dt.month

        df_agregado = df.groupby('mes').size().reset_index(name='contagem_transacoes')
        df_agregado.columns = ['Mês', 'Número de Transações']

        mes_renomear = {
            1: 'Jan',
            2: 'Fev',
            3: 'Mar',
            4: 'Abr',
            5: 'Mai',
            6: 'Jun',
            7: 'Jul',
            8: 'Ago',
            9: 'Set',
            10: 'Out',
            11: 'Nov',
            12: 'Dez',
        }

        df_agregado['Mês'] = df_agregado['Mês'].map(mes_renomear)

        fig = px.bar(
            df_agregado,
            x='Mês',
            y='Número de Transações',
            # Ordena o eixo X corretamente pelo número do mês (Dimensão Tempo)
            category_orders={'Mês Nome': [mes_renomear[i] for i in range(1, 13)]},
            title='Volume de Transações por Mês do Ano',
            text='Número de Transações',
            labels={
                'Número de Transações': 'Total de Transações',
            }
        )

        fig.update_layout(
            yaxis_tickformat='.2s', # Formata o eixo Y em notação abreviada (ex: 1M para 1.000.000)
            hovermode='x unified',
            yaxis=dict(
                showgrid=True,
                gridcolor='black',
                gridwidth=1,
                range=[0, df_agregado['Número de Transações'].max() * 1.2],
                zeroline=True,
                zerolinecolor='black',
                zerolinewidth=1.5,
            )
        )
        fig.add_annotation(
            text= "A hipótese é FALSA, pois:<br>Os meses de Agosto e Maio apresentam um número de transações maior do que o mês de Dezembro",
            xref="paper", yref="paper",
            x=0, y=-.5,  # posição abaixo do gráfico
            showarrow=False,
            font=dict(size=12),
            align="left"
        )

        fig.update_layout(
            margin=dict(
                t=80,b=150
            ),
            yaxis_tickformat='.2s', # Formata o eixo Y em notação abreviada (ex: 1M para 1.000.000)
            hovermode='x unified',
            yaxis=dict(
                showgrid=True,
                gridcolor='black',
                gridwidth=1,
                range=[0, df_agregado['Número de Transações'].max() * 1.4],
                zeroline=True,
                zerolinecolor='black',
                zerolinewidth=1.5,
            )
        )

        st.plotly_chart(fig, use_container_width=False, key='Gráfico do Volume de Transações por Mês do Ano')

    else:
        st.warning('Não foi possível exibir o gráfico da Hipótese 5')
