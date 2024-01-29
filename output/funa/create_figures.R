library(ggplot2)
library(readxl)
library(tidyverse)
library(purrr)
library(ggpubr)

setwd("C:/Users/20200059/OneDrive - TU Eindhoven/Documents/Github/DescriptionModels/output/funa/")
out <- read_excel("date24012024/output.xlsx")

out

out %>% 
  pivot_longer(
    cols = c(mean_est50, size_id50, CR, jentropy, jsim50, attribute_CR, time_minutes),
    names_to = 'measure', 
    values_to = 'value') %>%
  ggplot(aes(y = value, x = data_key)) +
  geom_bar(stat='identity', position = position_dodge()) + 
  facet_grid(measure~., labeller = label_value, scales = "free_y")

out %>% 
  select(data_key, varphi50, mu, mean_est50, size_id50, size_rows50, CR, jentropy, jsim50, attribute_CR, time_minutes) %>%
  xtable(include.rownames = FALSE)
