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

setwd("C:/Users/20200059/OneDrive - TU Eindhoven/Documents/Github/DescriptionModels/output/funa/")
out <- read_excel("date24012024/output.xlsx")
out <- read_excel("date30012024/output.xlsx")
out <- read_excel("date31012024/output.xlsx")

info <- read_excel("date31012024/output.xlsx", sheet = 2)

out <- out %>%
  arrange(factor(data_key, levels = c("long_with", "long_without", 
                                      "long_full_target_with", "long_full_target_without", 
                                      "long_adapt_with", "long_adapt_without", 
                                      "long_adapt_full_target_with", "long_adapt_full_target_without", 
                                      "wide", "wide_10", "wide_adapt", "wide_50", "wide_90", 
                                      "desc", "desc_adapt")))

out %>% 
  pivot_longer(
    cols = c(mean_est50, size_id50, CR, jentropy, jsim50, attribute_CR, time_minutes),
    names_to = 'measure', 
    values_to = 'value') %>%
  ggplot(aes(y = value, x = data_key)) +
  geom_bar(stat='identity', position = position_dodge()) + 
  facet_grid(measure~., labeller = label_value, scales = "free_y")

out %>% 
  select(data_key, model, varphi50, size_id50, size_rows50, mu, rej99, CR, jentropy, jsim50, attribute_CR, time_minutes) %>%
  arrange(factor(data_key, levels = c("long_with", "long_without", 
                                      "long_full_target_with", "long_full_target_without", 
                                      "long_adapt_with", "long_adapt_without", 
                                      "long_adapt_full_target_with", "long_adapt_full_target_without", 
                                      "wide", "wide_10", "wide_adapt", "wide_50", "wide_90", 
                                      "desc", "desc_adapt"))) %>%
  arrange(factor(model, levels = c("zsubrange_low", "subrange_fit"))) %>%
  xtable(include.rownames = FALSE)

out %>% 
  select(data_key, model, subrange_est50, subrange_se50) %>%
  arrange(factor(data_key, levels = c("long_with", "long_without", 
                                      "long_full_target_with", "long_full_target_without", 
                                      "long_adapt_with", "long_adapt_without", 
                                      "long_adapt_full_target_with", "long_adapt_full_target_without", 
                                      "wide", "wide_10", "wide_adapt", "wide_50", "wide_90", 
                                      "desc", "desc_adapt"))) %>%
  arrange(factor(model, levels = c("zsubrange_low", "subrange_fit"))) %>%
  xtable(include.rownames = FALSE)

info[,c(1,20)] %>%
  rename(data_key=`0`, model_params=`19`) %>%
  mutate(model_params = str_sub(model_params,-30,-1))

# visualize subgroups subitizing range
descs <- read_delim("date01022024/desc/['desc', 4, 20, 3, 5, 'subrange_fit', True, True, 0.5, True, 'without', 0.05, 3].txt")
setwd("C:/Users/20200059/Documents/Data/FUNA/DescriptionModels/") 
target <- read_parquet("target.pq")
descriptive <- read_parquet("descriptive_desc.pq")
setwd("C:/Users/20200059/OneDrive - TU Eindhoven/Documents/Github/DescriptionModels/output/funa/date01022024/")
out <- read_excel("output.xlsx")

out %>% 
  select(data_key, varphi50, size_id50, size_rows50, mu, rej90, CR, jentropy, jsim50, attribute_CR, time_minutes) %>%
  xtable(include.rownames = FALSE)

# manually select IDCodes using descriptions in descs
sgID1 <- descriptive %>%
  filter(NCtimeCmean <= 1.0) %>%
  filter(NCtimeCmean >= 0.2) %>%
  filter(SAtimeCmean <= 1.0) %>%
  filter(SAtimeCmean >= 0.71) %>%
  select(IDCode)
sgID2 <- descriptive %>%
  filter(NCtimeCmean <= 1.0) %>%
  filter(NCtimeCmean >= 0.16) %>%
  filter(SAtimeCmean <= 1.0) %>%
  filter(SAtimeCmean >= 0.71) %>%
  select(IDCode)
sgID3 <- descriptive %>%
  filter(NCtimeCmean <= 1.0) %>%
  filter(NCtimeCmean >= 0.16) %>%
  select(IDCode)
sgID4 <- descriptive %>%
  filter(NCtimeCmedian <= 1.0) %>%
  filter(NCtimeCmean >= 0.24) %>%
  filter(CAAnsCsum <= 0.25) %>%
  filter(CAAnsCsum >= 0.0) %>%
  select(IDCode)
sgID5 <- descriptive %>%
  filter(NCIES <= 0.73) %>%
  filter(NCIES >= 0.04) %>%
  select(IDCode)

target <- target %>%
  mutate(inSG1 = if_else(IDCode %in% sgID1$IDCode, 1, 0)) %>%
  mutate(inSG2 = if_else(IDCode %in% sgID2$IDCode, 1, 0)) %>%
  mutate(inSG3 = if_else(IDCode %in% sgID3$IDCode, 1, 0)) %>%
  mutate(inSG4 = if_else(IDCode %in% sgID4$IDCode, 1, 0)) %>%
  mutate(inSG5 = if_else(IDCode %in% sgID5$IDCode, 1, 0))

# manually take values from descs; ic = betas[0], b1 = betas[1], b2 = betas[3]  
regs <- data.frame(bp=c(3.34,2.87,3.09,3.17,2.9,3.18),
                   ic=c(1406.6,2130.03,1924.79,1857.68,1980.3,1861.03),
                   b1=c(88.07,79.02,127.98,121.54,81.66,118.54),
                   b2=c(462.68,665.82,575.36,551.71,627.49,558.07)) %>%
  mutate(y1 = ic+(bp*b1)) %>%
  mutate(y2 = y1+(9-bp)*b2)
regs

colors <- c("#999999", "#56B4E9", "#E69F00", "#a1d99b", "#c51b8a", "#de2d26")
i <- 5
selcol <- colors[i+1]
plot5 <- target %>% 
  slice_sample(n=1000) %>%
  ggplot(aes(x=DMStimL, y=DMTime)) +
  geom_point(aes(colour=as.factor(inSG5),shape=as.factor(inSG5)), size=0.4) + 
  scale_shape_manual(values=c(4, 15)) + 
  theme(legend.position="none") + 
  scale_x_continuous(breaks = seq(1,9,1)) + 
  scale_y_continuous(breaks = seq(0,10000,2000), limits=c(0,10000)) + 
  scale_color_manual(values=c("#999999", selcol)) + 
  geom_segment(aes(x = 1, y = regs[1,'ic'], xend = regs[1,'bp'], yend = regs[1,'y1']), colour="#999999", linewidth=0.4) + 
  geom_segment(aes(x = regs[1,'bp'], y = regs[1,'y1'], xend = 9, yend = regs[1,'y2']), colour="#999999", linewidth=0.4) + 
  geom_point(aes(x=regs[1,'bp'], y=regs[1,'y1']), colour="#999999", size=0.5) + 
  geom_point(aes(x=1, y=regs[1,'ic']), colour="#999999", size=0.5) + 
  geom_point(aes(x=9, y=regs[1,'y2']), colour="#999999", size=0.5) + 
  geom_segment(aes(x = 1, y = regs[i+1,'ic'], xend = regs[i+1,'bp'], yend = regs[i+1,'y1']), colour=selcol, linewidth=0.4) + 
  geom_segment(aes(x = regs[i+1,'bp'], y = regs[i+1,'y1'], xend = 9, yend = regs[i+1,'y2']), colour=selcol, linewidth=0.4) + 
  geom_point(aes(x=regs[i+1,'bp'], y=regs[i+1,'y1']), colour=selcol, size=0.5) + 
  geom_point(aes(x=1, y=regs[i+1,'ic']), colour=selcol, size=0.5) + 
  geom_point(aes(x=9, y=regs[i+1,'y2']), colour=selcol, size=0.5) + 
  ggtitle(paste0("DMTime=", regs[i+1,'ic'], "+", regs[i+1,'b1'], "(DMStimL-1)+", regs[i+1,'b2'], "(DMStimL-1-", regs[i+1,'bp'], ")")) + 
  theme(plot.title = element_text(color=selcol, size = 6, vjust=-2),  
        axis.text=element_text(size=5),
        axis.title=element_text(size=5))

plot0 <- target %>% 
  slice_sample(n=1000) %>%
  ggplot(aes(x=DMStimL, y=DMTime)) +
  geom_point(colour="#999999", size=0.4, shape=4) + 
  theme(legend.position="none") + 
  scale_x_continuous(breaks = seq(1,9,1)) + 
  scale_y_continuous(breaks = seq(0,10000,2000), limits=c(0,10000)) + 
  geom_segment(aes(x = 1, y = regs[1,'ic'], xend = regs[1,'bp'], yend = regs[1,'y1']), colour="#999999", linewidth=0.4) + 
  geom_segment(aes(x = regs[1,'bp'], y = regs[1,'y1'], xend = 9, yend = regs[1,'y2']), colour="#999999", linewidth=0.4) + 
  geom_point(aes(x=regs[1,'bp'], y=regs[1,'y1']), colour="#999999", size=0.5) + 
  geom_point(aes(x=1, y=regs[1,'ic']), colour="#999999", size=0.5) + 
  geom_point(aes(x=9, y=regs[1,'y2']), colour="#999999", size=0.5) + 
  ggtitle(paste0("DMTime=", regs[1,'ic'], "+", regs[1,'b1'], "(DMStimL-1)+", regs[1,'b2'], "(DMStimL-1-", regs[1,'bp'], ")")) + 
  theme(plot.title = element_text(color="#999999", size = 6, vjust=-2),  
        axis.text=element_text(size=5),
        axis.title=element_text(size=5))

pl <- grid.arrange(plot0, plot1, plot2, plot3, plot4, plot5, ncol=3)
ggsave("plot.pdf", pl, width = 24, height = 12, units = "cm")
