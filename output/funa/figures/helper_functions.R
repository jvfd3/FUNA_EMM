# helper functions for visualizing target models

create_bp <- function(x){
  y = unlist(strsplit(x," "))
  z = y[y!=""]
  return(as.numeric(z[2]))}

create_ic <- function(x){
  y = unlist(strsplit(x," "))
  z = gsub("[^0-9.-]", "", y)
  g = z[z!=""]
  return(as.numeric(g[1]))}

create_slopes <- function(x){
  y = unlist(strsplit(x," "))
  z = gsub("[^0-9.-]", "", y)
  g = z[z!=""]
  w1 = as.numeric(gsub("[^0-9.-]", "", g[1]))
  w2 = as.numeric(gsub("[^0-9.-]", "", g[2]))
  return(c(w1,w2))
}

create_regs <- function(descs){
  
  bp <- c(3.34)
  ic <- c(1407)
  b1 <- c(88)
  b2 <- c(463)
  
  nrsgs <- nrow(descs)
  for(i in 1:nrsgs){
    x <- descs$fitbreaks[i]
    bp[i+1] <- create_bp(x)
    x <- descs$intercepts[i]
    ic[i+1] <- create_ic(x)
    x <- descs$slopes[i]
    w <- create_slopes(x)
    b1[i+1] <- w[1]
    b2[i+1] <- w[2]
  }

  regs <- data.frame(bp=bp,
                     ic=ic,
                     b1=b1,
                     b2=b2) %>%
    mutate(ic1 = ic+b1) %>%
    mutate(y1 = ic+(bp*b1)) %>%
    mutate(y2 = y1+(9-bp)*b2) %>%
    mutate(bp = round(bp,1)) %>%
    mutate(ic = round(ic,0)) %>%
    mutate(ic1 = round(ic1,0)) %>%
    mutate(b1 = round(b1,0)) %>%
    mutate(b2 = round(b2,0))
  
  return(regs)}

create_figure <- function(target, regs, subgroups, colours){ 
  
  n <- nrow(target)
  selregs <- regs[subgroups+1,] %>%
    rownames_to_column() %>%
    rename('sg' = 'rowname') %>%
    mutate(sg = as.numeric(sg)-1) %>%
    mutate(xs = 1) %>%
    mutate(xe = 9)
  selcolors <- colors[subgroups+1]
  
  Gplot <- target %>% 
    mutate(sg = sample(subgroups,size=nrow(target),replace=TRUE)) %>%
    left_join(selregs) %>%
    slice_sample(n=5000) %>%
    ggplot(aes(x=DMStimL, y=DMTime)) +
    geom_point(colour="#999999", size=0.4) + 
    geom_segment(aes(x=xs, y=ic1, xend=bp, yend=y1, colour=as.factor(sg)), linewidth=0.4) +
    geom_segment(aes(x=bp, y=y1, xend=xe, yend=y2, colour=as.factor(sg)), linewidth=0.4) +
    geom_point(aes(x=bp, y=y1, colour=as.factor(sg)), size=0.5) + 
    geom_point(aes(x=xs, y=ic1, colour=as.factor(sg)), size=0.5) + 
    geom_point(aes(x=xe, y=y2, colour=as.factor(sg)), size=0.5) + 
    scale_x_continuous(breaks = seq(1,9,1)) + 
    scale_y_continuous(breaks = seq(0,10000,2000), limits=c(0,10000)) +
    geom_segment(aes(x=1, y=regs[1,'ic1'], xend = regs[1,'bp'], yend = regs[1,'y1']), colour="#999999", linewidth=0.4) + 
    geom_segment(aes(x=regs[1,'bp'], y=regs[1,'y1'], xend=9, yend=regs[1,'y2']), colour="#999999", linewidth=0.4) + 
    geom_point(aes(x=regs[1,'bp'], y=regs[1,'y1']), colour="#999999", size=0.5) + 
    geom_point(aes(x=1, y=regs[1,'ic1']), colour="#999999", size=0.5) + 
    geom_point(aes(x=9, y=regs[1,'y2']), colour="#999999", size=0.5) + 
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
    labs(x = "Set size", y = "Response time (ms)", 
         title = paste0("Subitizing patterns")) 

  return(list(Gplot, selregs))
}

make_descriptions <- function(descs, subgroups){
  
  df <- data.frame()
  for(i in 1:length(subgroups)){
    sg <- subgroups[i]
    desc <- descs[sg,] %>%
      select_if(~ !any(is.na(.))) %>%
      select(-c(literal_order,varphi,wvarphi,size_id,size_rows,subrange_est,subrange_se,slopes,intercepts,fitbreaks,betas,ssres,sstot,precision,nrparams,chorder,SSresGlobal,SSresLocal,nrrows,bic))
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



