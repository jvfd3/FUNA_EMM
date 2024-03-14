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

out10 <- read_excel("date10032024/output.xlsx") %>%
  select(model,d,gamma,varphi50,size_id50,jentropy,jsim50,time_minutes,mu,rej90,rej95,rej99)

out10sum <- out10 %>%
  group_by(model) %>% 
  mutate(avg_varphi = mean(varphi50),
         var_varphi = var(varphi50)) %>%
  ungroup() %>%
  mutate(varphi = (varphi50 - avg_varphi)/sqrt(var_varphi)) %>%
  mutate(d = as.character(d)) %>%
  mutate(gamma = as.character(gamma)) %>%
  mutate(model = ordered(factor(model), levels = c('reg_ssr','reg_ssrb','reg_bic'))) 

plot <-  out10sum %>%
  filter(model %in% c('reg_ssr', 'reg_ssrb', 'reg_bic')) %>%
  ggplot(aes(y=varphi,x=d,fill=gamma)) + 
  geom_bar(stat='identity', position = position_dodge()) + 
  facet_grid(. ~ model, scales = "free_y") + 
  scale_pattern_manual(values = c('3' = "stripe", '5' = "none")) +
  labs(x = "Number of search levels d", y = "Standardized quality value", 
       pattern = "",
       title = "") + 
  guides(pattern = guide_legend(override.aes = list(fill = "white")),
         fill = guide_legend(override.aes = list(pattern = "none"),
                             direction = 'horizontal')) + 
  theme(legend.position="top",
        legend.justification="right",
        plot.title = element_text(vjust=-4), 
        legend.box.margin = margin(-1,0,0,0, "line"),
        #axis.title.y = element_text(),
        panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank(),
        panel.grid.major.y = element_blank(),
        panel.grid.minor.y = element_blank(), 
        strip.background.y = element_blank(), 
        strip.text.y = element_blank()) + 
  scale_fill_manual(values=c("#bae4b3", "#31a354", "#006d2c"))

plot

name <- paste0('figures/dgamma.eps', sep = "", collapse = NULL)
ggsave(name, width = 16, height = 10, units = "cm")

out10 %>%
  arrange(factor(model, levels=c('reg_ssr','reg_ssrb','reg_bic')), d, gamma) %>%
  select(model, d, gamma, size_id50, rej99, jentropy, jsim50, time_minutes) %>%
  xtable(include.rownames = FALSE, digits=c(0,0,0,1,2,0,2,2,2))



