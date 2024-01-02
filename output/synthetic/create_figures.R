library(ggplot2)
library(readxl)
library(tidyverse)
library(purrr)

setwd("C:/Users/20200059/OneDrive - TU Eindhoven/Documents/Github/DescriptionModels/output/synthetic/")
out <- read_excel("zmean_high22122023/[[False], [False], [False], ['without'], None]_.xlsx")

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
