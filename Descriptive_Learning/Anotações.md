# Anotações

## Target DataFrame

| IDCode       | PreOrd | DMStimL | DMTime |
| :----------- | -----: | ------: | -----: |
| f3fa-bako357 |      2 |       4 |    199 |
| f3fa-bako357 |      4 |       8 |   1105 |
| f3fa-bako357 |      6 |       3 |   2552 |
| f3fa-bako357 |      9 |       1 |   1085 |
| f3fa-bako357 |     15 |       1 |   1245 |

## Description DataFrame

| IDCode       | NCAnsCsum | NCPreOrdmax | NCAnsCprop | NCtimeCmean | NCtimeCmedian |    NCIES | NCRTslopeNumDis | NCRTinterceptNumDis | NCRTslopeNumRatio | ... |    SSIES | CAAnsCsum | CAPreOrdmax | CAAnsCprop | CAtimeCmean | CAtimeCmedian |    CAIES | sex | grade | language |
| :----------- | --------: | ----------: | ---------: | ----------: | ------------: | -------: | --------------: | ------------------: | ----------------: | --: | -------: | --------: | ----------: | ---------: | ----------: | ------------: | -------: | --: | ----: | -------: |
| f3fa-bako357 |  0.916667 |        52.0 |   0.916667 |    0.124587 |      0.170089 | 0.028049 |        0.394925 |            0.351265 |          0.426656 | ... | 0.164063 |  0.125000 |    0.103093 |   0.712610 |    0.007415 |      0.131664 | 0.072136 |   f |     3 |        f |
| f3fa-bane815 |  0.937500 |        52.0 |   0.937500 |    0.167398 |      0.257034 | 0.043245 |        0.399024 |            0.379670 |          0.432475 | ... | 0.169072 |  0.142857 |    0.113402 |   0.736559 |    0.008396 |      0.148368 | 0.083764 |   f |     3 |        f |
| f3fa-baqy06  |  0.979167 |        52.0 |   0.979167 |    0.095500 |      0.168568 | 0.025484 |        0.390103 |            0.333689 |          0.425932 | ... | 0.162923 |  0.392857 |    0.268041 |   0.843887 |    0.007508 |      0.134676 | 0.072919 |   f |     3 |        f |
| f3fa-boky29  |  0.979167 |        52.0 |   0.979167 |    0.133777 |      0.214449 | 0.033593 |        0.382825 |            0.369720 |          0.413448 | ... | 0.166809 |  0.321429 |    0.237113 |   0.780466 |    0.007677 |      0.139506 | 0.076798 |   f |     3 |        f |
| f3fa-bolu326 |  0.979167 |        52.0 |   0.979167 |    0.139183 |      0.221039 | 0.034758 |        0.384475 |            0.372100 |          0.414247 | ... | 0.167288 |  0.232143 |    0.175258 |   0.765830 |    0.007797 |      0.137927 | 0.075934 |   f |     3 |        f |

### Datatypes

- **float64**
  1. NCAnsCsum
  2. NCPreOrdmax
  3. NCAnsCprop
  4. NCtimeCmean
  5. NCtimeCmedian
  6. NCIES
  7. NCRTslopeNumDis
  8. NCRTinterceptNumDis
  9. NCRTslopeNumRatio
  10. NCRTinterceptNumRatio
  11. SAAnsCsum
  12. SAPreOrdmax
  13. SAAnsCprop
  14. SAtimeCmean
  15. SAtimeCmedian
  16. SAIES
  17. SSAnsCsum
  18. SSPreOrdmax
  19. SSAnsCprop
  20. SStimeCmean
  21. SStimeCmedian
  22. SSIES
  23. CAAnsCsum
  24. CAPreOrdmax
  25. CAAnsCprop
  26. CAtimeCmean
  27. CAtimeCmedian
  28. CAIES
- **category**
  - grade
- **string**
  - IDCode
  - sex
  - language
