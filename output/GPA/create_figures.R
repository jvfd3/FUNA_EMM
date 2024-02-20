library(ggplot2)
library(readxl)
library(tidyverse)
library(purrr)
library(ggpubr)
library(xtable)
library(devtools)
install_github("coolbutuseless/ggpattern")
library(ggpattern)

setwd("C:/Users/20200059/OneDrive - TU Eindhoven/Documents/Github/DescriptionModels/output/gpa/")
out <- read_excel("admitted/date06022024/output.xlsx")

out

# explore results for admitted
out %>% 
  select(data_key, varphi50, suppclass50, size_id50, size_rows50, CR, jentropy, jsim50, attribute_CR, time_minutes, rej99) %>%
  xtable(include.rownames = FALSE)

out

out %>%
  pivot_longer(
    cols = c(rej90,suppclass50,CR,jentropy,jsim50,attribute_CR),
    names_to = "measure",
    values_to = "value") %>%
  mutate(measure = ordered(factor(measure), 
                           levels = c('rej90','suppclass50','CR','jentropy','jsim50','attribute_CR'))) %>%
  mutate(wcs = as.character(wcs)) %>%
  mutate(dbs = as.character(dbs)) %>%
  mutate(dp = as.character(dp)) %>%
  select(c(measure,value,data_key,wcs,dbs,dp)) %>%
  ggplot(aes(y=value,x=dp,fill=dbs,pattern=wcs)) + 
  #geom_bar(stat='identity', position = position_dodge(), color="black") + 
  geom_bar_pattern(stat='identity', position = position_dodge(),
                   color="black",
                   pattern_fill = "black",
                   pattern_angle = 45,
                   pattern_density = 0.1,
                   pattern_spacing = 0.025,
                   pattern_key_scale_factor = 0.6) + 
  facet_grid(measure ~ data_key., scales = "free_y") + 
  scale_fill_manual(values=c("#2ca25f", "#3182bd")) + 
  scale_pattern_manual(values = c('TRUE' = "stripe", 'FALSE' = "none")) +
  scale_alpha_discrete(range = c(0.2,0.8)) + 
  labs(x = "format", y = "value", pattern = "wcs") + 
  guides(pattern = guide_legend(override.aes = list(fill = "white")),
         fill = guide_legend(override.aes = list(pattern = "none")))

name <- paste('wcsdbsdp.eps', sep = "", collapse = NULL)
ggsave(name, width = 20, height = 24, units = "cm")

# explore results for gpa
out <- read_excel("gpa/date07022024/output.xlsx")

?facet_grid
