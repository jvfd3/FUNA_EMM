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
library(ggpattern)

setwd("C:/Users/20200059/OneDrive - TU Eindhoven/Documents/Github/FUNA_EMM/output/Curran/")

out09 <- read_excel("date09032024/output.xlsx") %>%
  select(model,d,gamma,varphi50,size_id50,jentropy,jsim50,time_minutes) 





