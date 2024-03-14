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

setwd("C:/Users/20200059/OneDrive - TU Eindhoven/Documents/Github/FUNA_EMM/data_input/Curran/data/")
target <- read_parquet("target.pq")
target
descriptive <- read_parquet("desc.pq")

setwd("C:/Users/20200059/OneDrive - TU Eindhoven/Documents/Github/FUNA_EMM/output/Curran/figures/")
source("helper_functions.R")

colors <- c("#878787", "#de2d26", "#a1d99b", "#c51b8a", "#01665e", "#ffed6f", "#ffffb3", "#543005", "#a6761d", "#1b9e77",
            "#a6cee3", "#1f78b4", "#33a02c", "#fb9a99", "#e31a1c", "#fdbf6f", "#ff7f00", "#cab2d6", "#6a3d9a", "#b15928")
# q = 10
descs <- read_delim("../date10032024/desc/['desc', 4, 20, 3, 10, 'reg_bic', False, 0.05, True, 0.5, False, 'without', 0.05, 3].txt")

regs <- create_regs(descs)
regs

out <- create_figure(target, regs, subgroups=c(1:10), colors)

Gplot <- out[[1]]
Gplot

selregs <- out[[2]]
selregs %>%
  mutate(at_age_6 = ic + 6*slope1) %>%
  #mutate(target = paste0(ic, " + ", slope1, "* age + ", slope2, " * age^2 + ", slope3, " * age^3")) %>%
  select(at_age_6, slope1, slope2, slope3) %>%
  xtable()

name <- paste('bic053.pdf', sep = "", collapse = NULL)
ggsave(name, width = 16, height = 10, units = "cm")

descriptions <- make_descriptions(descs, subgroups=c(1:10)) 
descriptions %>%
  select(size, lit1, lit2, lit3) %>%
  xtable(digits=c(0,2,0,0,0))
