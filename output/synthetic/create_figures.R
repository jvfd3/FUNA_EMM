library(ggplot2)
library(readxl)
library(tidyverse)
library(purrr)
library(ggpubr)

setwd("C:/Users/20200059/OneDrive - TU Eindhoven/Documents/Github/DescriptionModels/output/synthetic/")
out <- read_excel("date02012024/output.xlsx")

# explore results
mean_est50 <- ggplot(out, aes(y = mean_est50, x = SGType, fill = data)) + 
  geom_bar(stat = "identity", position = position_dodge(), colour="black")
se_est50 <- ggplot(out, aes(y = se_est50, x = SGType, fill = data)) + 
  geom_bar(stat = "identity", position = position_dodge(), colour="black")
size_id50 <- ggplot(out, aes(y = size_id50, x = SGType, fill = data)) + 
  geom_bar(stat = "identity", position = position_dodge(), colour="black")
jsim50 <- ggplot(out, aes(y = jsim50, x = SGType, fill = data)) + 
  geom_bar(stat = "identity", position = position_dodge(), colour="black")
CR <- ggplot(out, aes(y = CR, x = SGType, fill = data)) + 
  geom_bar(stat = "identity", position = position_dodge(), colour="black")
overall_coverage <- ggplot(out, aes(y = overall_coverage, x = SGType, fill = data)) + 
  geom_bar(stat = "identity", position = position_dodge(), colour="black")
desc_len50 <- ggplot(out, aes(y = desc_len50, x = SGType, fill = data)) + 
  geom_bar(stat = "identity", position = position_dodge(), colour="black")
attribute_CR <- ggplot(out, aes(y = attribute_CR, x = SGType, fill = data)) + 
  geom_bar(stat = "identity", position = position_dodge(), colour="black")

figure <- ggarrange(mean_est50, se_est50, size_id50, jsim50, CR, overall_coverage, desc_len50, attribute_CR,
                    labels = c("", "", "", ""),
                    ncol = 2, nrow = 4)
figure

name <- paste('../figures/Figures_manuscript_finalized/orders_exceptional_starting_behaviour.eps', sep = "", collapse = NULL)
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
