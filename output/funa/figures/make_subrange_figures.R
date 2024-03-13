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

source("helper_functions.R")

setwd("C:/Users/20200059/Documents/Data/FUNA/FUNA_EMM/") 
target <- read_parquet("target.pq")
descriptive <- read_parquet("descriptive_desc.pq")

setwd("C:/Users/20200059/OneDrive - TU Eindhoven/Documents/Github/FUNA_EMM/output/funa/figures/")
colors <- c("#56B4E9", "#de2d26", "#a1d99b", "#c51b8a", "#E69F00", "#a6cee3", "#ffffb3", "#7570b3", "#a6761d", "#1b9e77",
            "#56B4E9", "#de2d26", "#a1d99b", "#c51b8a", "#E69F00", "#a6cee3", "#ffffb3", "#7570b3", "#a6761d", "#1b9e77")

# q = 10
# bic
descs <- read_delim("../date05032024/desc/['desc', 4, 20, 3, 10, 'subrange_ssrb', False, True, 0.5, False, 'without', 0.05, 3].txt")
descs <- read_delim("../date07032024/desc/['desc', 4, 20, 3, 10, 'subrange_bic', False, True, 0.5, False, 'without', 0.05, 3].txt")
descs <- read_delim("../date08032024/desc/['desc', 4, 20, 3, 10, 'subrange_ssr', False, True, 0.5, False, 'without', 0.05, 3].txt")

out <- do_all(descs, target, regs, subgroups=c(1:10), colors)
Gplot <- out[[1]]
Gplot
selregs <- out[[2]]
selregs %>%
  mutate(target = paste0(ic, " + ", b1, "*x + ", b2, "*", "(x-", bp, ")")) %>%
  select(target) %>%
  xtable()

name <- paste('bic050305.pdf', sep = "", collapse = NULL)
ggsave(name, width = 16, height = 10, units = "cm")

descriptions <- make_descriptions(descs, subgroups=c(1:10)) 
descriptions %>%
  select(size, lit1, lit2, lit3) %>%
  xtable(digits=c(0,2,0,0,0))

# q = 20
# ssrb
descs <- read_delim("../date06032024/desc/['desc', 4, 20, 3, 20, 'subrange_ssrb', False, True, 0.5, False, 'without', 0.05, 3].txt")
regs <- create_regs(descs)
out <- create_figure(target, regs, subgroups=c(1:20), colors)
Gplot <- out[[1]]
Gplot
selregs <- out[[2]]
selregs %>%
  mutate(target = paste0(ic, " + ", b1, "*x + ", b2, "*", "(x-", bp, ")")) %>%
  select(target) %>%
  xtable()

name <- paste('ssrb305all.pdf', sep = "", collapse = NULL)
ggsave(name, width = 16, height = 10, units = "cm")

descriptions <- make_descriptions(descs, subgroups=c(1:20)) 
descriptions %>%
  select(size, lit1, lit2, lit3) %>%
  xtable(digits=c(0,2,0,0,0))

# bic
descs <- read_delim("../date10032024/desc/['desc', 4, 20, 3, 20, 'subrange_bic', False, True, 0.5, False, 'without', 0.05, 3].txt")
regs <- create_regs(descs)
out <- create_figure(target, regs, subgroups=c(1:20), colors)
Gplot <- out[[1]]
Gplot
selregs <- out[[2]]
selregs %>%
  mutate(target = paste0(ic, " + ", b1, "*x + ", b2, "*", "(x-", bp, ")")) %>%
  select(target) %>%
  xtable()

name <- paste('bic305all.pdf', sep = "", collapse = NULL)
ggsave(name, width = 16, height = 10, units = "cm")

descriptions <- make_descriptions(descs, subgroups=c(1:20)) 
descriptions %>%
  select(size, lit1, lit2, lit3) %>%
  xtable(digits=c(0,2,0,0,0))

