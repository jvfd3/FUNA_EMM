# helper functions for visualizing target models

create_slopes <- function(x){
  y = unlist(strsplit(x," "))
  z = gsub("[^0-9.-]", "", y)
  g = z[z!=""]
  
  w = c()
  for(j in 1:(length(g)-1)){
    w[j] = as.numeric(gsub("[^0-9.-]", "", g[j+1]))
  }
  
  return(w)
}

create_ic <- function(x){
  return(as.numeric(x))
}

create_regs <- function(descs){
  
  nrsgs <- nrow(descs)
  
  ic <- c(-5.785255839882121,rep(0,nrsgs))
  slope1 <- c(1.56553148,rep(0,nrsgs))
  slope2 <- c(-0.0520093,rep(0,nrsgs))
  slope3 <- c(0,rep(0,nrsgs))
  
  for(i in 1:nrsgs){
    x <- descs$intercepts[i]
    ic[i+1] <- create_ic(x)
    
    x <- descs$slopes[i]
    w <- create_slopes(x)
    
    slope1[i+1] <- w[1]
    if(length(w)>1){
      slope2[i+1] <- w[2]
      if(length(w)>2){
        slope3[i+1] <- w[3]
      }
    }
  }
  
  regs <- data.frame(ic=ic,
                     slope1=slope1,
                     slope2=slope2, 
                     slope3=slope3) %>%
    mutate(ic = round(ic,2)) %>%
    mutate(slope1 = round(slope1,2)) %>%
    mutate(slope2 = round(slope2,2)) %>%
    mutate(slope3 = round(slope3,2))

  return(regs)}

create_figure <- function(target, regs, subgroups, colours){ 
  
  n <- nrow(target)
  selregs <- regs[subgroups+1,] %>%
    rownames_to_column() %>%
    rename('sg' = 'rowname') %>%
    mutate(sg = as.numeric(sg)-1)
  selcolors <- colors[subgroups+1]

  dat <- target %>% 
    mutate(sg = sample(subgroups,size=nrow(target),replace=TRUE)) %>%
    left_join(selregs) %>%
    mutate(line = ic + slope1 * kidagetv + slope2 * (kidagetv**2) + slope3 * (kidagetv**3))

  Gplot <- dat %>%
    ggplot(aes(x=kidagetv, y=read)) +
    geom_point(colour="#999999", size=0.4) + 
    geom_line(aes(x = kidagetv, y = line, colour=as.factor(sg)), linewidth=0.4) + 
    scale_color_manual(name="sg", values=selcolors) + 
    theme(legend.position="top",
          legend.justification="right",
          plot.title = element_text(vjust=-8,size=14), 
          legend.box.margin = margin(0,0,0,0, "line"),
          text=element_text(size=14),
          axis.text.x=element_text(size=12),
          axis.text.y=element_text(size=10),
          legend.text=element_text(size=10),
          axis.title=element_text(size=12)) + 
    guides(fill = guide_legend(direction = "horizontal")) +
    labs(x = "Age", y = "Reading skills", 
         title = paste0("")) 

  return(list(Gplot, selregs))
}

make_descriptions <- function(descs, subgroups){
  
  df <- data.frame()
  for(i in 1:length(subgroups)){
    sg <- subgroups[i]
    desc <- descs[sg,] %>%
      select_if(~ !any(is.na(.))) %>%
      select(-any_of(c("literal_order","varphi","wvarphi","size_id","size_rows",
                       "subrange_est","subrange_se","slopes","intercepts",
                       "fitbreaks","betas","ssres","sstot","precision",
                       "nrparams","chorder","SSresGlobal","SSresLocal",
                       "nrrows","bic")))
    nlit <- ncol(desc)
    colnames <- colnames(desc)
    for(j in 1:length(colnames)){
      litj <- paste0(colnames[j], ":", desc[1,j])
      df[i,j] <- litj
    }
  }
  names(df) <- c('lit1', 'lit2', 'lit3')
  df['sg'] <- subgroups
  df['size'] <- descs['size_id']
  
  return(df)
}



