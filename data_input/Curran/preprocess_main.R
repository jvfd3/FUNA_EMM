library(foreign)
library(dplyr)
library(tidyr)
library(stringr)
library(mice)
library(writexl)
library(arrow)

path_to_this_folder = NaN # scrubbed for double=blind reviewing
setwd("path_to_this_folder/FUNA_EMM/data_input/Curran/")
#data <- read.spss('CurranData.sav', to.data.frame = TRUE)
data <- read.spss('CurranLong.sav', to.data.frame = TRUE)
head(data)

# read as target
# long format
data_long <- data %>%
  mutate(kidgen = recode(kidgen, "girl" = 1, "boy" = 0)) %>%
  mutate(id = paste0('id',id)) %>%
  select(-c(anti,kidage6,kidagec,occasion2,kidagesq)) %>%
  mutate(intage = momage*kidagetv) %>%
  mutate(intemo = homeemo*kidagetv) %>%
  mutate(intcog = homecog*kidagetv) %>%
  cc()

head(data_long)
target <- data_long[,c("id","occasion","read","kidagetv")]

# change to wide format
data_wide <- data_long %>%
  select(-c(read,kidagetv)) %>%
  pivot_wider(values_from = c(intage,intemo,intcog), names_from = occasion)

# change to desc format
data_desc <- data_long %>%
  select(-kidage) %>%
  group_by(id) %>%
  mutate(sum_age = sum(intage)) %>%
  mutate(slope_age = rev(intage)[1] - intage[1]) %>%
  mutate(min_age = min(intage)) %>%
  mutate(max_age = max(intage)) %>%
  mutate(sum_emo = sum(intemo)) %>%
  mutate(slope_emo = rev(intemo)[1] - intemo[1]) %>%  
  mutate(min_emo = min(intemo)) %>%
  mutate(max_emo = max(intemo)) %>%
  mutate(sum_cog = sum(intcog)) %>%
  mutate(slope_cog = rev(intcog)[1] - intcog[1]) %>%  
  mutate(min_cog = min(intcog)) %>%
  mutate(max_cog = max(intcog)) %>%
  ungroup() %>%
  select(c(id, kidgen, momage, homecog, homeemo, sum_age, slope_age, min_age, max_age, sum_emo, slope_emo, max_emo, min_emo, sum_cog, slope_cog, min_cog, max_cog)) %>% # needed to bring back to wide format
  distinct_all() %>%
  mutate(across(c(sum_age, slope_age, min_age, max_age, sum_emo, slope_emo, max_emo, min_emo, sum_cog, slope_cog, min_cog, max_cog), scales::rescale))

head(data_desc)

data_wide %>% write_parquet("data/wide.pq")
data_long %>% select(-read,-intage,-intemo,-kidage) %>% write_parquet("data/long.pq")
data_desc %>% write_parquet("data/desc.pq")
write_parquet(target, "data/target.pq")
