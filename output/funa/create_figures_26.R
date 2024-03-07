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
#install_github("coolbutuseless/ggpattern")
library(ggpattern)

setwd("C:/Users/20200059/OneDrive - TU Eindhoven/Documents/Github/DescriptionModels/output/funa/")

# with varying order, #subrange_fit has only order 1
out26 <- read_excel("date26022024/output.xlsx")
out27 <- read_excel("date27022024/output.xlsx")
out28 <- read_excel("date28022024/output.xlsx")
out29 <- read_excel("date29022024/output.xlsx")

info <- read_excel("date26022024/output.xlsx", sheet = 2)
info$`18`

out28

out28sum <- out28 %>% 
  rbind(out29) %>%
  mutate(n = c(rep(0.05,24),rep(0.10,24))) %>%
  group_by(model, n) %>% 
  summarise(avg_varphi = mean(varphi50),
            var_varphi = var(varphi50)) %>%
  ungroup() %>%
  left_join(out27) %>%
  select(c(model, n, avg_varphi, var_varphi, mu))
  
out28long <- out28 %>% 
  rbind(out29) %>%
  mutate(n = c(rep(0.05,24),rep(0.10,24))) %>%
  left_join(out28sum) %>%
  mutate(varphi = (varphi50 - avg_varphi)/sqrt(var_varphi)) %>%
  mutate(mu_varphi = (mu - avg_varphi)/sqrt(var_varphi)) %>%
  pivot_longer(
    cols = c(varphi,subrange_est50),
    names_to = "measure",
    values_to = "value") %>%
  mutate(measure = ordered(factor(measure), 
                           levels = c('varphi','subrange_est50'))) %>%
  mutate(d = as.character(d)) %>%
  mutate(gamma = as.character(gamma)) %>%
  mutate(n = as.character(n)) %>%
  select(c(measure,value,model,n,d,gamma,mu_varphi))

out28long  

colors <- c("#999999", "#56B4E9", "#E69F00", "#a1d99b", "#c51b8a", "#de2d26")
plot <-  out28long %>%
  filter(measure == 'varphi') %>%
  ggplot(aes(y=value,x=d,fill=gamma)) + 
  geom_bar(stat='identity', position = position_dodge()) + 
  #geom_bar_pattern(stat='identity', position = position_dodge(),
  #                 color="black",
  #                 pattern_fill = "black",
  #                 pattern_angle = 45,
  #                 pattern_density = 0.1,
  #                 pattern_spacing = 0.025,
  #                 pattern_key_scale_factor = 0.6) + 
  #geom_hline(aes(yintercept=mu_varphi)) + 
  facet_grid(n ~ model, scales = "free_y") + 
  scale_fill_manual(values=c("#bae4b3", "#31a354", "#006d2c")) + 
  scale_pattern_manual(values = c('3' = "stripe", '5' = "none")) +
  #scale_alpha_discrete(range = c(0.2,0.8)) + 
  labs(x = "Description length d", y = "Standardized quality value", pattern = "") + 
  guides(pattern = guide_legend(override.aes = list(fill = "white")),
         fill = guide_legend(override.aes = list(pattern = "none")))
  
plot

name <- paste('date28022024/dgamma.eps', sep = "", collapse = NULL)
ggsave(name, width = 20, height = 16, units = "cm")

###
# with order 1 for all 4 quality measures
# we do not have results for n = 0.1
out02 <- read_excel("date02032024/output.xlsx")
out27 <- read_excel("date27022024/output.xlsx") %>%
  filter(model == 'subrange_fit') %>%
  rbind(out02)
out03 <- read_excel("date03032024/output.xlsx")
out28 <- read_excel("date28022024/output.xlsx") %>%
  filter(model == 'subrange_fit') %>%
  rbind(out03) 
out28sum <- out28 %>%
  group_by(model) %>% 
  summarise(avg_varphi = mean(varphi50),
            var_varphi = var(varphi50)) %>%
  ungroup() %>%
  left_join(out27) %>%
  select(c(model, avg_varphi, var_varphi, mu))

out28long <- out28 %>% 
  left_join(out28sum) %>%
  mutate(varphi = (varphi50 - avg_varphi)/sqrt(var_varphi)) %>%
  mutate(mu_varphi = (mu - avg_varphi)/sqrt(var_varphi)) %>%
  pivot_longer(
    cols = c(varphi,subrange_est50),
    names_to = "measure",
    values_to = "value") %>%
  mutate(measure = ordered(factor(measure), 
                           levels = c('varphi','subrange_est50'))) %>%
  mutate(d = as.character(d)) %>%
  mutate(gamma = as.character(gamma)) %>%
  select(c(measure,value,model,d,gamma,mu_varphi))

plot <-  out28long %>%
  filter(measure == 'varphi') %>%
  ggplot(aes(y=value,x=d,fill=gamma)) + 
  geom_bar(stat='identity', position = position_dodge()) + 
  #geom_bar_pattern(stat='identity', position = position_dodge(),
  #                 color="black",
  #                 pattern_fill = "black",
  #                 pattern_angle = 45,
  #                 pattern_density = 0.1,
  #                 pattern_spacing = 0.025,
  #                 pattern_key_scale_factor = 0.6) + 
  #geom_hline(aes(yintercept=mu_varphi)) + 
  facet_grid(measure ~ model, scales = "free_y") + 
  scale_pattern_manual(values = c('3' = "stripe", '5' = "none")) +
  #scale_alpha_discrete(range = c(0.2,0.8)) + 
  labs(x = "Description length d", y = "Standardized quality value", 
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

name <- paste('date03032024/dgamma.eps', sep = "", collapse = NULL)
ggsave(name, width = 16, height = 10, units = "cm")

###

out02 <- read_excel("date02032024/output.xlsx")
read_excel("date27022024/output.xlsx") %>%
  filter(model == 'subrange_fit') %>%
  rbind(out02) %>%
  select(model, varphi50, size_id50, mu, rej95) %>%
  xtable(include.rownames = FALSE)

out05 <- read_excel("date05032024/output.xlsx")  
out28 %>%
  left_join(out05[,c('model','d','gamma','mu','rej90','rej95','rej99')],by=c('model','d','gamma')) %>%
  select(model, d, gamma, size_id50, rej95, CR, jentropy, jsim50, attribute_CR, time_minutes) %>%
  arrange(factor(model, levels=c('subrange_ssr','subrange_fit','subrange_ssrb','subrange_ll')), d, gamma) %>%
  xtable(include.rownames = FALSE)

###

setwd("C:/Users/20200059/OneDrive - TU Eindhoven/Documents/Github/DescriptionModels/output/funa/")
descsssrb <- read_delim("date02032024/desc/['desc', 4, 20, 3, 5, 'subrange_ssrb', False, True, 0.1, False, 'without', 0.05, 3].txt")

setwd("C:/Users/20200059/Documents/Data/FUNA/DescriptionModels/") 
target <- read_parquet("target.pq")
descriptive <- read_parquet("descriptive_desc.pq")

sgID1 <- descriptive %>%
  filter(CAPreOrdmax <= 0.19) %>%
  filter(NCRTinterceptNumDis >= 0.41) %>%
  filter(NCRTinterceptNumDis <= 0.57) %>%
  filter(NCRTslopeNumDis >= 0.37) %>%
  filter(NCRTslopeNumDis <= 0.56) %>%
  select(IDCode)
sgID2 <- descriptive %>%
  filter(CAPreOrdmax <= 0.19) %>%
  filter(SAAnsCsum >= 0.1) %>%
  filter(SAAnsCsum <= 0.24) %>%
  filter(SStimeCmedian >= 0.29) %>%
  filter(SStimeCmedian <= 0.35) %>%
  select(IDCode)
sgID3 <- descriptive %>%
  filter(CAPreOrdmax >= 0.02) %>%
  filter(CAPreOrdmax <= 0.15) %>%
  filter(NCtimeCmedian >= 0.19) %>%
  filter(NCtimeCmedian <= 0.52) %>%
  select(IDCode)
sgID4 <- descriptive %>%
  filter(NCRTinterceptNumDis >= 0.4) %>%
  filter(NCRTinterceptNumDis <= 0.57) %>%
  filter(NCIES >= 0.03) %>%
  filter(NCIES <= 0.38) %>%
  filter(NCtimeCmedian >= 0.20) %>%
  filter(NCtimeCmedian <= 0.44) %>%
  select(IDCode)
sgID5 <- descriptive %>%
  filter(NCIES >= 0.04) %>%
  filter(NCIES <= 0.38) %>%
  select(IDCode)

target <- target %>%
  mutate(inSG1 = if_else(IDCode %in% sgID1$IDCode, 1, 0)) %>%
  mutate(inSG2 = if_else(IDCode %in% sgID2$IDCode, 1, 0)) %>%
  mutate(inSG3 = if_else(IDCode %in% sgID3$IDCode, 1, 0)) %>%
  mutate(inSG4 = if_else(IDCode %in% sgID4$IDCode, 1, 0)) %>%
  mutate(inSG5 = if_else(IDCode %in% sgID5$IDCode, 1, 0))

descsssrb$intercepts
descsssrb$fitbreaks
descsssrb$slopes

regs <- data.frame(bp=c(3.34,3.32,2.21,2.54,3.41,3.23),
                   ic=c(1406.6,2267.76,2468.36,1786.98,2260.9,1762.72),
                   b1=c(88.07,26.32,-241.35,34.88,15.72,93.61),
                   b2=c(462.68,927.79,759.28,703.73,835.69,685.29)) %>%
  mutate(y1 = ic+(bp*b1)) %>%
  mutate(y2 = y1+(9-bp)*b2)
regs

colors <- c("#999999", "#56B4E9", "#de2d26", "#a1d99b", "#c51b8a", "#E69F00")
i <- 5
selcol <- colors[i+1]
plot <- target %>% 
  slice_sample(n=1000) %>%
  ggplot(aes(x=DMStimL, y=DMTime)) +
  geom_point(aes(colour=as.factor(inSG5),shape=as.factor(inSG5)), size=0.4) + 
  scale_shape_manual(values=c(4, 15)) + 
  theme(legend.position="none") + 
  scale_x_continuous(breaks = seq(1,9,1)) + 
  scale_y_continuous(breaks = seq(0,10000,2000), limits=c(0,10000)) + 
  scale_color_manual(values=c(selcol, "#999999")) + 
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
plot

plot <- target %>% 
  slice_sample(n=5000) %>%
  ggplot(aes(x=DMStimL, y=DMTime)) +
  geom_point(colour="#999999", size=0.4) + 
  scale_x_continuous(breaks = seq(1,9,1)) + 
  scale_y_continuous(breaks = seq(0,10000,2000), limits=c(0,10000)) +
  geom_segment(aes(x = 1, y = regs[1,'ic'], xend = regs[1,'bp'], yend = regs[1,'y1']), colour="#999999", linewidth=0.4) + 
  geom_segment(aes(x = regs[1,'bp'], y = regs[1,'y1'], xend = 9, yend = regs[1,'y2']), colour="#999999", linewidth=0.4) + 
  geom_point(aes(x=regs[1,'bp'], y=regs[1,'y1']), colour="#999999", size=0.8) + 
  geom_point(aes(x=1, y=regs[1,'ic']), colour="#999999", size=0.8) + 
  geom_point(aes(x=9, y=regs[1,'y2']), colour="#999999", size=0.8) + 
  geom_segment(aes(x = 1, y = regs[5+1,'ic'], xend = regs[5+1,'bp'], yend = regs[5+1,'y1'], colour='5'), linewidth=0.4, linetype=2) + 
  geom_segment(aes(x = regs[i+1,'bp'], y = regs[5+1,'y1'], xend = 9, yend = regs[5+1,'y2'], colour='5'), linewidth=0.4, linetype=2) + 
  geom_point(aes(x=regs[5+1,'bp'], y=regs[5+1,'y1']), colour=colors[5+1], size=0.8) + 
  geom_point(aes(x=1, y=regs[5+1,'ic']), colour=colors[5+1], size=0.8) + 
  geom_point(aes(x=9, y=regs[5+1,'y2']), colour=colors[5+1], size=0.8) + 
  geom_segment(aes(x = 1, y = regs[4+1,'ic'], xend = regs[4+1,'bp'], yend = regs[4+1,'y1'], colour='4'), linewidth=0.4, linetype=2) + 
  geom_segment(aes(x = regs[4+1,'bp'], y = regs[4+1,'y1'], xend = 9, yend = regs[4+1,'y2'], colour='4'), linewidth=0.4, linetype=2) + 
  geom_point(aes(x=regs[4+1,'bp'], y=regs[4+1,'y1']), colour=colors[4+1], size=0.8) + 
  geom_point(aes(x=1, y=regs[4+1,'ic']), colour=colors[4+1], size=0.8) + 
  geom_point(aes(x=9, y=regs[4+1,'y2']), colour=colors[4+1], size=0.8) + 
  geom_segment(aes(x = 1, y = regs[3+1,'ic'], xend = regs[3+1,'bp'], yend = regs[3+1,'y1'], colour='3'), linewidth=0.4, linetype=2) + 
  geom_segment(aes(x = regs[3+1,'bp'], y = regs[3+1,'y1'], xend = 9, yend = regs[3+1,'y2'], colour='3'), linewidth=0.4, linetype=2) + 
  geom_point(aes(x=regs[3+1,'bp'], y=regs[3+1,'y1']), colour=colors[3+1], size=0.8) + 
  geom_point(aes(x=1, y=regs[3+1,'ic']), colour=colors[3+1], size=0.8) + 
  geom_point(aes(x=9, y=regs[3+1,'y2']), colour=colors[3+1], size=0.8) + 
  geom_segment(aes(x = 1, y = regs[2+1,'ic'], xend = regs[2+1,'bp'], yend = regs[2+1,'y1'], colour='2'), linewidth=0.4, linetype=2) + 
  geom_segment(aes(x = regs[2+1,'bp'], y = regs[2+1,'y1'], xend = 9, yend = regs[2+1,'y2'], colour='2'), linewidth=0.4, linetype=2) + 
  geom_point(aes(x=regs[2+1,'bp'], y=regs[2+1,'y1']), colour=colors[2+1], size=0.8) + 
  geom_point(aes(x=1, y=regs[2+1,'ic']), colour=colors[2+1], size=0.8) + 
  geom_point(aes(x=9, y=regs[2+1,'y2']), colour=colors[2+1], size=0.8) + 
  geom_segment(aes(x = 1, y = regs[1+1,'ic'], xend = regs[1+1,'bp'], yend = regs[1+1,'y1'], colour='1'), linewidth=0.4, linetype=2) + 
  geom_segment(aes(x = regs[1+1,'bp'], y = regs[1+1,'y1'], xend = 9, yend = regs[1+1,'y2'], colour='1'), linewidth=0.4, linetype=2) + 
  geom_point(aes(x=regs[1+1,'bp'], y=regs[1+1,'y1']), colour=colors[1+1], size=0.8) + 
  geom_point(aes(x=1, y=regs[1+1,'ic']), colour=colors[1+1], size=0.8) + 
  geom_point(aes(x=9, y=regs[1+1,'y2']), colour=colors[1+1], size=0.8) + 
  labs(x = "Symbolic number", y = "Response time (ms)", 
       title = "Subitizing range for 5 subgroups") + 
  scale_color_manual(name='',
                     breaks=c('1', '2', '3', '4', '5'),
                     values=c('1'=colors[1+1], '2'=colors[2+1], '3'=colors[3+1], '4'=colors[4+1], '5'=colors[5+1])) + 
  theme(legend.position="top",
        legend.justification="right",
        plot.title = element_text(vjust=-8,size=14), 
        legend.box.margin = margin(0,0,0,0, "line"),
        text=element_text(size=20),
        axis.text.x=element_text(size=12),
        axis.text.y=element_text(size=10),
        legend.text=element_text(size=10),
        axis.title=element_text(size=12)) + 
  guides(fill = guide_legend(direction = "horizontal"))

plot

name <- paste('date02032024/subgroups_ssrb.eps', sep = "", collapse = NULL)
ggsave(name, width = 16, height = 10, units = "cm")

###

setwd("C:/Users/20200059/OneDrive - TU Eindhoven/Documents/Github/DescriptionModels/output/funa/")
descsssrb <- read_delim("date05032024/desc/['desc', 4, 20, 3, 10, 'subrange_ssrb', False, True, 0.5, False, 'without', 0.05, 3].txt")
descsfit <- read_delim("date05032024/desc/['desc', 4, 20, 3, 10, 'subrange_fit', False, True, 0.5, False, 'without', 0.05, 3].txt")

setwd("C:/Users/20200059/Documents/Data/FUNA/DescriptionModels/") 
target <- read_parquet("target.pq")
descriptive <- read_parquet("descriptive_desc.pq")

# ssrb
sgID1 <- descriptive %>%
  filter(NCRTinterceptNumRatio <= 0.58) %>%
  filter(NCRTinterceptNumRatio >= 0.41) %>%
  filter(NCtimeCmean   <= 0.36) %>%
  filter(NCtimeCmean   >= 0.2) %>%
  filter(CAAnsCsum   >= 0.05) %>%
  filter(NCRTslopeNumDis <= 0.3) %>%
  select(IDCode)
sgID2 <- descriptive %>%
  filter(NCRTinterceptNumRatio <= 0.58) %>%
  filter(NCRTinterceptNumRatio >= 0.38) %>%
  filter(NCIES <= 0.38) %>%
  filter(NCIES >= 0.04) %>%
  filter(CAPreOrdmax >= 0.02) %>%
  filter(CAPreOrdmax <= 0.15) %>%
  select(IDCode)
sgID3 <- descriptive %>%
  filter(NCRTinterceptNumRatio <= 0.58) %>%
  filter(NCRTinterceptNumRatio >= 0.41) %>%
  select(IDCode)

target <- target %>%
  mutate(inSG1 = if_else(IDCode %in% sgID1$IDCode, 1, 0)) %>%
  mutate(inSG2 = if_else(IDCode %in% sgID2$IDCode, 1, 0)) %>%
  mutate(inSG3 = if_else(IDCode %in% sgID3$IDCode, 1, 0)) %>%
  mutate(inSG4 = if_else(IDCode %in% sgID4$IDCode, 1, 0)) %>%
  mutate(inSG5 = if_else(IDCode %in% sgID5$IDCode, 1, 0))

descsssrb$intercepts
descsssrb$fitbreaks
descsssrb$slopes

regs <- data.frame(bp=c(3.34,3.32,2.21,2.54,3.41,3.23),
                   ic=c(1406.6,2267.76,2468.36,1786.98,2260.9,1762.72),
                   b1=c(88.07,26.32,-241.35,34.88,15.72,93.61),
                   b2=c(462.68,927.79,759.28,703.73,835.69,685.29)) %>%
  mutate(y1 = ic+(bp*b1)) %>%
  mutate(y2 = y1+(9-bp)*b2)
regs
