library(ggplot2)
library(readxl)
library(tidyverse)
library(purrr)
library(ggpubr)
library(xtable)

setwd("C:/Users/20200059/OneDrive - TU Eindhoven/Documents/Github/DescriptionModels/output/synthetic/")
out <- read_excel("date24012024/output.xlsx")
out <- read_excel("date25012024/output.xlsx")
out <- read_excel("date26012024/output.xlsx")

out

# explore results
out %>%
  pivot_longer(
    cols = c(varphi50, mean_est50, se_est50, slope_est50, se_slope50, size_id50, CR, jentropy, jsim50, attribute_CR),
    names_to = 'measure', 
    values_to = 'value') %>%
  ggplot(aes(y = value, x = data_key)) +
  geom_bar(stat='identity', position = position_dodge()) + 
  facet_grid(measure ~ model, labeller = label_value, scales = "free_y") + 
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))

out %>% 
  filter(SGType == 'E') %>% 
  filter(model == 'zmean_high') %>%
  select(data_key, mean_est50, size_id50, size_rows50, CR, jentropy, jsim50, attribute_CR, time_minutes) %>%
  xtable(include.rownames = FALSE)

out %>%
  filter(model == 'zmean_high') %>%
  select(data_key, SGType, mean_est50, size_id50, CR, jentropy, jsim50, attribute_CR, time_minutes) %>%
  pivot_wider(names_from = 'SGType', values_from = c(mean_est50, size_id50, CR, jentropy, jsim50, attribute_CR, time_minutes)) %>%
  mutate(mean_est_dif = mean_est50_D - mean_est50_E,
         size_id50_dif = size_id50_D - size_id50_E,
         CR_dif = CR_D - CR_E, 
         jentropy_dif = jentropy_D - jentropy_E,
         jsim50_dif = jsim50_D - jsim50_E, 
         attribute_CR_dif = attribute_CR_D - attribute_CR_E, 
         time_minutes_dif = time_minutes_D - time_minutes_E
         ) %>%
  select(data_key, mean_est_dif, size_id50_dif, CR_dif, jentropy_dif, jsim50_dif, attribute_CR_dif, time_minutes_dif) %>%
  xtable(include.rownames = FALSE)

##

figure <- ggarrange(mean_est50, se_est50, size_id50, jsim50, CR, overall_coverage, desc_len50, attribute_CR,
                    labels = c("", "", "", ""),
                    ncol = 2, nrow = 4)
figure

name <- paste('date03012024/figure.pdf', sep = "", collapse = NULL)
ggsave(name, width = 20, height = 16, units = "cm")

# input data

link_to_data <- "../../data_input/synthetic/data/[10, 10, 3, 'default', 1.0]/data.xlsx"
datain <- map(set_names(excel_sheets(link_to_data)), 
                 read_excel, path=link_to_data)
lapply(names(datain), function(x) 
  assign(x, datain[[x]], envir=.GlobalEnv))

target <- as.data.frame(target)
str(target)

plot(target$TargetC)
names(target)

ggplot(target, aes(group = TimeInd, y = TargetC)) + geom_boxplot()

target %>% group_by(TimeInd) %>% summarise(avg = mean(TargetC))

desc_target <- as.data.frame(desc_target)
nrow(desc_target[desc_target$seq == 'ccc',])       
33/1000
