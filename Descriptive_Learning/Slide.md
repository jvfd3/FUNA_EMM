# Descrevendo os dados

- FUNA
  - Target: $(13135, 4)$
    - int64: 3 colunas (DMStimL, DMTime, PreOrd)
    - object: 1 coluna (IDCode)
  - Desc: $(774, 32)$
    - float64: 28 colunas
      - $\{NC, SA, SS, CA\} \times \{AnsCsum, PreOrdmax, AnsCprop, timeCmean, timeCmedian, IES\}$
      - $\{NCRT\} \times \{slopeNumDis, interceptNumDis, slopeNumRatio\}$
    - category: 1 coluna $\{grade\}$
    - string: 3 colunas $\{IDCode, sex, language\}$
- Curran
  - Data: $(405, 15)$
    - float64: 14 colunas
      - $\{anti, read\} \times \{1, 2, 3, 4\}$
      - $\{homecog, homeemo, id, kidage, momage, nmis\}$
    - category: 1 coluna $\{kidgen\}$
  - Long: $(1393, 14)$
    - float64: 13 colunas
      - $\{kidage\} \times \{\varnothing, 6, c, sq, tv\}$
      - $\{anti, homecog, homeemo, id, momage, occasion, occasion2, read\}$
    - category: 1 coluna $\{kidgen\}$

## Descrevendo o código

-
