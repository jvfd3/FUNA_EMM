# Defining graph

- Estrutura Principal:
  1. `main.py` - Ponto de entrada principal do aplicativo
  2. Módulos de Experimento (azul) - Responsáveis por análise, recuperação de dados e processamento de resultados
  3. Módulos de Beam Search (verde) - Implementam o algoritmo de busca em feixe para descoberta de padrões
  4. Módulos de Constraints (laranja) - Aplicam restrições e filtros
  5. Módulos de Preprocessamento (roxo) - Processam dados de entrada
  6. Bibliotecas Externas (amarelo claro) - numpy, pandas, scikit-learn, scipy, joblib
  7. Arquivos de Dados (rosa) - Arquivos parquet processados
- Fluxo de Dependências:
  - O `main.py` chama principalmente `analysis.py` e `save_and_store_result.py`
  - O módulo de análise coordena a recuperação de dados e execução do beam search
  - O beam search é o núcleo do algoritmo, usando vários módulos auxiliares para qualidades, refinamentos, parâmetros e medidas
  - Os constraints aplicam filtros e pruning durante o processo
  - Os dados são preprocessados pelos módulos FUNA e depois consumidos pelos módulos de experimento

```mermaid
flowchart LR
    %% Main application entry point
    main[main.py]

    %% Core modules
    subgraph "experiment/"
        exp_analysis[analysis.py]
        exp_ssr[save_and_store_result.py]
        exp_retrieve[retrieve_rw_data.py]
        exp_retrieve_funa[retrieve_funa.py]
        exp_retrieve_curran[retrieve_curran.py]
        exp_process[process_result.py]
        exp_dfd[distribution_false_discoveries.py]
        exp_pwlf[pwlf.py]
    end


    %% Beam search modules
    subgraph "beam_search/"
        bs_qualities[qualities.py]
        bs_beam[beam_search.py]
        bs_parameters[parameters.py]
        bs_measures[measures.py]
        bs_prepare[prepare_beam.py]
        bs_select[select_subgroup.py]
        bs_summarize[summarize.py]
        bs_refine_func[refinements_functions.py]
        bs_refinements[refinements.py]


      %% Constraints modules
      subgraph "constraints/"
          const_constraints[constraints.py]
          const_dominance[dominance_pruning.py]
          const_desc_sel[desc_based_selection.py]
          const_cover_sel[cover_based_selection.py]
      end
    end

    %% Data preprocessing modules
    subgraph "data_input/FUNA"
        data_funa_preprocess[preprocess_main.py]
        data_funa_desc[preprocess_into_desc.py]
        data_funa_long[preprocess_into_long.py]
        data_funa_wide[preprocess_into_wide.py]
        data_funa_functions[preprocess_functions.py]
    end


    %% External libraries
    subgraph External Libraries
        numpy[numpy]
        pandas[pandas]
        sklearn[scikit-learn]
        scipy[scipy]
        joblib[joblib]
    end

    %% Data files
    data_desc[("`**Data Files**
    desc.pq
    target.pq
    wide.pq
    long.pq`")]


    %% Experiment module dependencies
    exp_analysis --> exp_retrieve
    exp_analysis --> bs_beam
    exp_analysis --> exp_dfd
    exp_analysis --> exp_ssr

    %% Main dependencies
    main --> exp_ssr
    main --> exp_analysis

    exp_retrieve --> exp_retrieve_funa
    exp_retrieve --> exp_retrieve_curran

    exp_ssr --> exp_process

    %% Beam search dependencies
    bs_beam --> bs_qualities
    bs_beam --> bs_refinements
    bs_beam --> bs_select
    bs_beam --> bs_prepare
    bs_beam --> bs_summarize
    bs_beam --> const_dominance
    bs_beam --> const_constraints

    bs_qualities --> bs_parameters
    bs_qualities --> bs_select
    bs_qualities --> const_constraints


    bs_measures --> exp_pwlf
    bs_measures --> bs_select


    bs_prepare --> const_desc_sel
    bs_prepare --> const_cover_sel
    bs_parameters --> bs_measures
    bs_refinements --> bs_refine_func

    %% Data preprocessing dependencies
    data_funa_preprocess --> data_funa_functions
    data_funa_preprocess --> data_funa_desc
    data_funa_preprocess --> data_funa_long
    data_funa_preprocess --> data_funa_wide

    %% Data flow
    data_funa_preprocess --> data_desc
    exp_retrieve_funa --> data_desc
    exp_retrieve_curran --> data_desc

    %% External library dependencies
    exp_analysis --> numpy
    exp_analysis --> pandas

    bs_beam --> joblib
    bs_measures --> sklearn
    bs_measures --> scipy

    exp_dfd --> joblib
    exp_pwlf --> scipy

    data_funa_functions --> sklearn

    %% Styling
    classDef mainModule fill:#ff9999,stroke:#333,stroke-width:2px,color:#000
    classDef expModule fill:#99ccff,stroke:#333,stroke-width:2px,color:#000
    classDef beamModule fill:#99ff99,stroke:#333,stroke-width:2px,color:#000
    classDef constModule fill:#ffcc99,stroke:#333,stroke-width:2px,color:#000
    classDef dataModule fill:#cc99ff,stroke:#333,stroke-width:2px,color:#000
    classDef extLib fill:#ffffcc,stroke:#333,stroke-width:2px,color:#000
    classDef dataFile fill:#ffccff,stroke:#333,stroke-width:2px,color:#000

    class main mainModule
    class exp_analysis,exp_ssr,exp_retrieve,exp_retrieve_funa,exp_retrieve_curran,exp_process,exp_dfd,exp_pwlf expModule
    class bs_beam,bs_qualities,bs_refinements,bs_parameters,bs_measures,bs_prepare,bs_select,bs_summarize,bs_refine_func beamModule
    class const_constraints,const_dominance,const_desc_sel,const_cover_sel constModule
    class data_funa_preprocess,data_funa_functions,data_funa_desc,data_funa_long,data_funa_wide dataModule
    class numpy,pandas,sklearn,scipy,joblib extLib
    class data_desc dataFile
```

## Parâmetros

A função `main_test_cases` permite selecionar diferentes cenários de execução para a função central `main`, que é responsável por executar análises em um conjunto de dados. A principal diferença entre cada caso de teste reside nos parâmetros passados para a função `main`, especialmente nos dicionários `sim_params` (parâmetros de simulação) e `extra_info` (informações adicionais).

A função `main` cria um diretório de saída e um arquivo de saída vazio para os resultados. Se `synthetic_params` for `None`, ela executa a análise de dados, caso contrário, uma análise sintética (embora esta última opção seja comentada com "It never occurs", indicando que não é utilizada atualmente). No final, o arquivo de resultados é atualizado.

Todos os casos de teste utilizam as seguintes configurações comuns:

- `output_path`: 'output/DescriptiveLearning'
- `current_date`: '20250630'
- `input_data_path`: 'data_input'
- Parâmetros de simulação comuns: `'b':`, `'w':`, `'dbs': [False]`, `'wcs': [True]`, `'dp': [False]`, `'md': ['without']`, `'min_size': [0.05]`.
- Informações extras comuns: `'case_based_target': False`, `'run_beam_search': True`.
- `datasets_names`: Sempre `['desc']` em todos os casos de teste.

A tabela abaixo compara as **diferenças chave** entre cada um dos casos de teste, destacando os parâmetros que variam:

| Caso de Teste | `data_name` | `sim_params['model']`                                            | `sim_params['d']` | `sim_params['q']` | `sim_params['gamma']` | `sim_params['alpha']` | `target_column_names`                     | `sample` | `sample_prop` | `run_redun_metrics` | `make_dfd` | `m`  | `startorder` | `maxorder` | `prefclass` |
| :------------ | :---------- | :--------------------------------------------------------------- | ----------------: | ----------------: | :-------------------- | :-------------------- | :---------------------------------------- | :------- | :------------ | :------------------ | :--------- | :--- | :----------- | :--------- | :---------- |
| `choice_1a`   | FUNA        | ['subrange_ll', 'subrange_ssr', 'subrange_ssrb']                 |                   |              [10] | [0.1, 0.5, 0.9]       | N/A                   | ['DMTime', 'IDCode', 'PreOrd', 'DMStimL'] | True     | 0.05          | True                | False      | None | N/A          | N/A        | N/A         |
| `choice_1b`   | FUNA        | ['subrange_ll', 'subrange_ssr', 'subrange_ssrb', 'subrange_fit'] |                   |              [10] | [0.1, 0.5, 0.9]       | N/A                   | ['DMTime', 'IDCode', 'PreOrd', 'DMStimL'] | True     | 0.05          | False               | True       | 50   | N/A          | N/A        | N/A         |
| `choice_1c`   | FUNA        | ['subrange_ssrb']                                                |                   |              [20] | [0.5]                 | N/A                   | ['DMTime', 'IDCode', 'PreOrd', 'DMStimL'] | False    | None          | False               | False      | None | N/A          | N/A        | N/A         |
| `choice_2a`   | FUNA        | ['subrange_bic']                                                 |               [5] |              [10] | [0.5, 0.9]            | N/A                   | ['DMTime', 'IDCode', 'PreOrd', 'DMStimL'] | True     | 0.05          | True                | True       | 2    | 0            | 3          | N/A         |
| `choice_2b`   | FUNA        | ['subrange_ssr']                                                 |            [3, 5] |              [10] | [0.1, 0.5, 0.9]       | N/A                   | ['DMTime', 'IDCode', 'PreOrd', 'DMStimL'] | True     | 0.05          | True                | True       | 50   | N/A          | N/A        | N/A         |
| `choice_2c`   | Curran      | ['reg_ssr', 'reg_ssrb', 'reg_bic']                               |            [3, 5] |              [10] | [0.1, 0.5, 0.9]       | [0.05]                | ['read', 'id', 'occasion', 'kidagetv']    | None     | N/A           | True                | True       | 2    | 0            | 3          | None        |
| `choice_2d`   | FUNA        | ['subrange_bic']                                                 |               [3] |              [20] | [0.5]                 | N/A                   | ['DMTime', 'IDCode', 'PreOrd', 'DMStimL'] | False    | 0.05          | False               | False      | 2    | 0            | 3          | N/A         |
| `choice_3`    | Curran      | ['reg_ssr', 'reg_ssrb', 'reg_bic']                               |            [3, 5] |              [10] | [0.1, 0.5, 0.9]       | [0.05]                | ['read', 'id', 'occasion', 'kidagetv']    | None     | N/A           | False               | True       | 50   | 0            | 3          | None        |
| `choice_4`    | FUNA        | ['subrange_bic']                                                 |            [3, 5] |              [10] | [0.1, 0.5, 0.9]       | N/A                   | ['DMTime', 'IDCode', 'PreOrd', 'DMStimL'] | True     | 0.05          | False               | True       | 50   | 0            | 3          | N/A         |

**Observações Adicionais sobre as Diferenças:**

- **Conjunto de Dados (`data_name`)**: A maioria dos casos de teste utiliza o conjunto de dados **'FUNA'**, com exceção de `choice_2c` e `choice_3`, que utilizam o conjunto de dados **'Curran'**.
- **Modelos de Simulação (`sim_params['model']`)**:
  - Casos 'FUNA' utilizam modelos com o prefixo 'subrange\_' (e.g., 'subrange_ll', 'subrange_ssr', 'subrange_ssrb', 'subrange_fit', 'subrange_bic').
  - Casos 'Curran' utilizam modelos com o prefixo 'reg\_' (e.g., 'reg_ssr', 'reg_ssrb', 'reg_bic').
- **Parâmetros `d` e `q`**: Variam para testar diferentes profundidades de hierarquia (`d`) e quantidade de grupos (`q`) para os modelos.
- **Valores de `gamma`**: A maioria dos casos testa múltiplos valores de `gamma` ([0.1, 0.5, 0.9]), enquanto `choice_1c` e `choice_2d` testam um único valor ([0.5]).
- **Parâmetro `alpha`**: É introduzido apenas para os modelos de regressão ('reg\_') nos casos de teste que usam o dataset 'Curran' (`choice_2c` e `choice_3`), com o valor `[0.05]`.
- **Nomes das Colunas Alvo (`target_column_names`)**: Mudam de `['DMTime', 'IDCode', 'PreOrd', 'DMStimL']` para 'FUNA' para `['read', 'id', 'occasion', 'kidagetv']` para 'Curran'.
- **Amostragem (`sample` e `sample_prop`)**:
  - Muitos casos utilizam amostragem (`sample: True`) com uma proporção de `0.05`.
  - `choice_1c` não usa amostragem (`sample: False`) e `sample_prop` é `None`.
  - `choice_2d` não usa amostragem (`sample: False`), mas `sample_prop` ainda é definido como `0.05`.
  - `choice_2c` e `choice_3` definem `sample` como `None` e não especificam `sample_prop`.
- **Métricas de Redundância (`run_redun_metrics`)**: Alguns casos executam as métricas de redundância (`True`), enquanto outros as desativam (`False`).
- **Criação de DFD (`make_dfd` e `m`)**: Alguns casos ativam a criação de um DFD (`True`) com diferentes valores de `m` (2 ou 50), enquanto outros não criam DFD (`False`) e `m` é `None`.
- **Parâmetros de Ordem (`startorder` e `maxorder`)**: Presentes nos casos `choice_2a`, `choice_2c`, `choice_2d`, `choice_3` e `choice_4`, com `startorder: 0` e `maxorder: 3`.
- **`prefclass`**: Este parâmetro é relevante e definido como `None` apenas nos casos que utilizam o dataset 'Curran' (`choice_2c` e `choice_3`).
- **Nota específica para `choice_2b`**: O código inclui um comentário indicando que esta escolha "do ssr again, with 1/ef instead of ef", sugerindo uma alteração interna na lógica de cálculo do SSR que não é visível diretamente nos parâmetros da função `main`.
