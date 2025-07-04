# Descrevendo os dados

- FUNA (pq: parquet)
  - **Target**: $(13135, 4)$
    - int64: 3 colunas (DMStimL, DMTime, PreOrd)
    - string: 1 coluna (IDCode)
  - **Desc**: $(774, 32)$
    - float64: 28 colunas
      - $\{NC, SA, SS, CA\} \times \{AnsCsum, PreOrdmax, AnsCprop, timeCmean, timeCmedian, IES\}$
      - $\{NCRT\} \times \{slopeNumDis, interceptNumDis, slopeNumRatio\}$
    - category: 1 coluna $\{grade\}$
    - string: 3 colunas $\{IDCode, sex, language\}$
- Curran (sav: Statistical Package for the Social Sciences|pq: parquet)
  - **Data**: $(405, 15)$
    - float64: 14 colunas
      - $\{anti, read\} \times \{1, 2, 3, 4\}$
      - $\{homecog, homeemo, id, kidage, momage, nmis\}$
    - category: 1 coluna $\{kidgen\}$
  - **Long**: $(1393, 14)$
    - float64: 13 colunas
      - $\{kidage\} \times \{\varnothing, 6, c, sq, tv\}$
      - $\{anti, homecog, homeemo, id, momage, occasion, occasion2, read\}$
    - category: 1 coluna $\{kidgen\}$

## Descrevendo o código

- Main parâmetros:
  - **Padrão**:
    - datasets_names=['desc']
    - synthetic_params=None: Nunca ocorre, a função inclusive nem existe
    - date: dia da execução
    - data_name: 'FUNA' ou 'Curran'
    - data_from: input path
    - output_to: output path
  - **sim_params**:
    - b=[4]: quantidade de quantis
    - w=[20]: critério de parada do dbs
    - d: profundidade da hierarquia
    - q: quantidade de grupos
    - model: modelos de estimativas
    - dbs=[False]: Se True (nunca é), aplica _description-based selection_ ao preparar o Beam
    - wcs=[True]: Se true (sempre é), aplica _cover-based selection_ ao preparar o Beam
    - gamma: vetor de pesos
    - dp=[False]: Se True (nunca é), aplica _dominance pruning_ no Beam Search
    - md=['without']: influences selection in ss
    - min_size=0.05: tamanho mínimo do subgrupo
  - **extra_info**:
    - target_column_names: lista de nomes das colunas destino. Sempre os mesmos pra FUNA e Curran
    - sample: determina se será feita uma amostragem
    - sample_prop: proporção da amostragem
    - case_based_target=False: if True only select first available row of every case
    - run_redun_metrics: executa métricas de redundância
    - run_beam_search=True: executa busca em feixe
    - make_dfd: Se True, cria uma Distribuição de Falsas Descobertas
    - m: range para percorrer a distribuição de falsos descobertas
