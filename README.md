# Análise de Compra e Venda de Imóveis da cidade de São Paulo

## Problema de negócio
O principal desafio da House Rocket reside na otimização de capital ao tomar decisões sobre compra e venda de imóveis. A empresa precisa maximizar seus lucros identificando imóveis subvalorizados para compra e determinando o preço de venda ideal.

O mercado imobiliário é complexo e o valor de um imóvel é afetado por inúmeras variáveis como localização, área, e ano de construção.

Neste caso, você é apresentado a um conjunto de dados de amostra sobre transação de imóveis na cidade de São Paulo. É seu desafio entender os dados, encontrar oportunidades e insights de negócios e propor qualquer ação orientada a dados para auxiliar a empresa a identificar as melhores oportunidades de investimento e maximizar o lucro.

Como Cientista de Dados, o seu objetivo é: fazer uma análise descritiva dos imóveis e construir um modelo de Machine Learning (Regressão) capaz de prever o valor de transação de imóveis permitindo que a House Rocket otimize sua estratégia de compra e o preço de revenda dos imóveis.

## Contexto
A House Rocket é uma empresa focada em "House Flipping" (comprar, reformar e vender imóveis rapidamente para lucro) e atua na cidade de São Paulo.

O time de aquisição de imóveis precisa tomar decisões rápidas sobre quais propriedades comprar e por qual preço, enquanto o time de vendas precisa determinar um preço de mercado justo e competitivo. Ambas as decisões são baseadas em estimativas subjetivas e em dados desorganizados.

Nesse contexto, o Cientista de Dados é essencial para coletar, analisar e entregar um modelo que quantifique o valor real do imóvel, a fim de ajudá-la a aumentar o faturamento nas próximas campanhas.

OBS: este é um cenário fictício

## Premissas de análise
- Todos os imóveis com status_IPTU cancelado foram removidos por não representar um ativo viável de compra.
- Todos os imóveis que não apresentaram registros de tipo de financiamento foram 'categorizados' como Não Informados.
- Foram retirados 10,83% de outliers da base de dados original
- A análise utilizou de dados sinteticos, mas instrusivos do [Kaggle](https://www.kaggle.com/datasets/balkry/2023-so-paulo-real-estate-transactions-data)

## Estratégia da solução
O método Fato-Dimensão foi usado para desenvolver a análise de dados da campanha de Marketing.

Nesse modelo, os fatos representam eventos quantitativos — como interações ou vendas — enquanto as dimensões descrevem atributos contextuais, como cliente, produto ou data, permitindo consultas mais rápidas, agregações eficientes e melhor visualização dos padrões de comportamento dos clientes.

### Passo 1: Resumir o contexto em uma pergunta aberta
As perguntas abertas são um tipo de demanda muito comum em análise de dados no qual a demanda possui N possíveis soluções e cabe ao Analista de Dados avaliar as possibilidades e escolher a alternativa com o maior retorno com o menor esforço possível. Para essa análise foi definida a seguinte pergunta aberta:

**Quais imóveis o CEO da House Rocket deveria comprar?**

### Passo 2: Transformar a pergunta aberta em fechada
As perguntas fechadas são um tipo de demanda muito comum em análise de dados. Essa demanda contém todos os detalhes da análise de dados e direciona o analista exatamente para o que precisa ser feito. Geralmente, a pergunta fechada é a escolha de uma solução entre todas as alternativas possíveis, feita por um profissional mais Senior da área.

Para essa análise, foi definida a seguinte pergunta fechada:

**Quais são as características ideais dos imóveis para aquisição?**

### Passo 3: Definição da coluna Fato
O Fato é a coluna de interesse que representa o ponto focal da análise. Nesse caso, a coluna "valor_transacao" representa o valor da aquisição do imóvel e será o objetivo da nossa análise, dado que o problema envolve aumento do faturamento na próxima campanha de compra e venda de imóveis.

### Passo 4: Identificação das Dimensões
As colunas foram agrupadas em dimensões comuns que fornecem mais detalhes sobre o Fato que será analisado. Foram organizadas as seguintes dimensões:

1. Localização
  - id_iptu: identificador do imóvel no cadastro do IPTU.
  - cep: representa o Código de Endereçamento Postal do imóvel.
  - numero_endereco: numeração do imóvel no seu respectivo logradouro.
  - tipo_logradouro: tipo do logradouro.
  - nome_logradouro: nome do logradouro.
  - endereco_completo: endereço completo com tipo e nome.
  - distrito: subdivisão do Município.
  - zona
  - latitude
  - longitude

2. Tempo
  - data_transacao: data do instrumento particular ou escritura pública por meio da qual o negócio jurídico está sendo formalizado.

3. Imóvel
  - matricula_imovel: número da matrícula (ou transcrição) do imóvel transacionado.
  - status_IPTU: sinaliza se determinado imóvel está ativo ou cancelado no cadastro do IPTU (Cadastro Imobiliário Fiscal).
  - area_terreno_m²: área do terreno em m²
  - frente_m: medida, em metros, da frente do imóvel para o logradouro.
  - fracao_ideal: Percentual atribuído a cada unidade autônoma em relação à área (de terreno) do condomínio.
  - area_construida_m²: área construída em m².
  - cod_uso_IPTU: código relativo à finalidade preponderante a que o imóvel se destina
  - desc_uso_IPTU: identifica a finalidade preponderante a que o imóvel se destina.
  - cod_padrao_IPTU: código relativo ao tipo e padrão da construção.
  - desc_padrao_IPTU: identifica tipo relacionado ao código de padrão da construção.
  - ano_construcao: indica o ano do término da construção.
  - valor_imovel: valor total do imóvel

4. Transação
  - natureza_transacao: indica o tipo de negócio jurídico por meio do qual o imóvel está sendo transmitido.
  - valor_ref_mercado: valor divulgado pela Prefeitura, que servirá como parâmetro inicial no processo de obtenção da base de cálculo do ITBI.
  - proporcao_transmitida: parte do imóvel (em percentual) que está sendo transmitido.
  - valor_ref_proporcional: valor que será comparado com o Valor de Transação para se chegar à base de cálculo do ITBI.
  - base_calculo_ITBI 
  - tipo_financiamento: modalidade de financiamento vinculado à aquisição do imóvel
  - valor_financiado: valor do financiamento concedido pelo banco ou instituição financeira para aquisição do imóvel.
  - cartorio: cartório de Registro de Imóvel responsável pela matrícula (ou transcrição) do imóvel transacionado.

### Passo 5: Hipóteses Analíticas

#### Dimensão Localização

- 1: A média do valor de transacao por distrito é maior do que a média geral da cidade, indicando áreas de maior valorização.

- 2: Imóveis próximos a centros comerciais e a eixos de transporte possuem um valor de transação maior do que imóveis situados mais afastados dessas áreas centrais e vias principais.

- 3: Imovéis cuja razão entre area construída e area do terreno possuem um valor de transação maior para o uso 'Residencial' do que para 'Industrial' no mesmo distrito.

#### Dimensão Imóvel

- 4: A média do valor de transacao para imóveis com area construida acima de 200m² é maior do que para os imóveis com área construída menor.

- 5: A soma do valor de transacao (total transacionado) por tipo de financiamento 'Minha Casa Minha Vida' é maior do que as transações dos outros tipos de financiamento.

- 5: O Valor Médio da Transação em endereços próximos a Avenida é, em média, pelo menos 20% maior do que em endereços próximos a Rua.

- 6: Qual tipo de imóvel representa o maior valor de transação médio, e quais são os tipos mais frequentes nas transações?

#### Dimensão Tempo

- 7: O mês de dezembro apresenta um número maior transações em comparação com os demais meses do ano.

- 8: O preço médio do valor de transação dos imóveis apresentou uma tendência de crescimento ao longo dos meses ou trimestres do período coberto pelos dados.

### Passo 6: Critérios de Priorização
Critério 1: Impacto para a o negócio

Critério 2: Viabilidade e Disponibilidade dos Dados

Critério 3: Insight Acionável

### Passo 7: Priorização das Hipóteses Analíticas
Hipótese 1. Imovéis cuja razão entre area construída e area do terreno por finalidade possuem um valor de transação maior para o uso 'Residencial' do que para 'Industrial' no mesmo distrito.
![hipotese1](https://github.com/user-attachments/assets/aa8afd0b-aafc-400e-b5cd-87b8b88a896b)

Hipótese 2. A média do valor de transação para imóveis com area construida acima de 200m² é maior do que para os imóveis com área construída menor.
![hipotese2](https://github.com/user-attachments/assets/1810730a-787f-42bf-894f-bb2329f26461)

Hipótese 3. A soma do valor de transacao (total transacionado) por tipo de financiamento 'Minha Casa Minha Vida' é maior do que as transações dos outros tipos de financiamento.
![hipotese3](https://github.com/user-attachments/assets/1e80844e-039f-4a1e-b2d8-e6c15251b66d)

Hipótese 4. Qual tipo de imóvel representa o maior valor de transação médio, e quais são os tipos mais frequentes nas transações?
![hipotese4](https://github.com/user-attachments/assets/c2296ee3-50f2-4fa1-a17e-56ef61b7d09d)

Hipótese 5. O mês de dezembro apresenta um número maior transações em comparação com os demais meses do ano.
![hipotese5](https://github.com/user-attachments/assets/f1b94e41-0b73-434d-bf3c-4e2b1f2ccb13)

### Resultados

#### Conclusão
Os imóveis com maior potencial de revenda são:
  - Tipo do Imóvel: Apartamentos em Condominio ou Residências.
  - Tamanho: com área construída acima de 200m².
  - Tempo: os meses de Maio, Agosto e Dezembro são ideais para otimizar a velocidade de revenda.


### Próximos Passos

1. Realizar uma análise preditiva para o preço de compra dos imóveis.
2. Explorar mais características dos imóveis, como calcular o impacto da distância entre centros comerciais e a eixos de transporte no preço do imóvel.
3. Automatizar a coleta e a análise para acompanhamento.
4. Montar um dashboard de acompanhamento das métricas das futuras campanhas.
