library(ggplot2)
library(readxl)
library(tidyverse)
library(purrr)
library(ggpubr)
library(xtable)
library(stringr)
library(arrow)
library(gridExtra)
library(grid)
library(devtools)
library(ggpattern)

setwd("C:/Users/20200059/Documents/Data/FUNA/FUNA_EMM/") 
target <- read_parquet("target.pq")
desc <- read_parquet("descriptive_desc.pq")
desc_unscaled <- read_parquet("descriptive_desc_unscaled.pq")

cols <- names(desc_unscaled)
sums <- desc_unscaled %>%
  select(-c(IDCode,sex,grade,language)) %>%
  summarise_all(list(quantile))
sums
