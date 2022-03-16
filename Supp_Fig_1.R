# Supplementary_Fig_1
rm(list=ls())
#install.packages("patchwork")
library(patchwork)
library(tidyverse)
library(ggplot2)
library(cowplot)
library(data.table)
############## 00. plot_setting ######################
plot_setting <- theme_classic() + 
  theme(plot.title = element_text(size = 8,hjust = 0.5,face = 'bold'), 
        axis.text.x  = element_text(size=20, face = 'bold'), # size 20, bold 
        axis.title.x = element_text(size=20, face = 'bold'), 
        axis.title.y = element_text(size=20, face = 'bold'),
        axis.text.y = element_text(size = 20, face = 'bold'),
        panel.grid.major=element_line(colour=NA),
        axis.line = element_line(colour = "black",size = 1),
        axis.ticks = element_line(colour = 'black'),
        panel.background = element_rect(fill = "transparent",colour = NA),
        plot.background = element_rect(fill = "transparent",colour = NA),
        panel.grid.minor = element_blank())

############## 01. load data ######################
fst <- read.csv('/Users/evolutioneco/Project/1.guppy_fst/new_genotype/MF_fst.weir.fst', sep = '\t', header = T)
perm <- read.csv('/Users/evolutioneco/Project/1.guppy_fst/new_genotype/pop.value_sorted.csv', sep = '\t', header = T)
fisher <- read.csv('/Users/evolutioneco/Project/1.guppy_fst/new_genotype/fisher_mf_sorted.csv', sep = '\t', header = T)

################## 02. tidy data #########################
x <- c(1:23)
data<-data.frame(CHROM=factor(fst$CHROM,levels = paste("LG",x,sep="")), 
                MIDPOINT = as.numeric(fst$POS),
                Fst=fst$WEIR_AND_COCKERHAM_FST, Pvalue=perm$PVALUE, Pvalue2=fisher$PVALUE)
# check data again
as.factor(data$CHROM)
head(data)

############### 03. calculate chr position ################
#1) calculate chromosome length
chr_len <- data %>% 
  group_by(CHROM) %>% 
  summarise(chr_len=max(MIDPOINT))
# check chromosome length
chr_len

#2）calculate initial position of each chromosome
chr_pos <- chr_len  %>% 
  mutate(total = cumsum(chr_len) - chr_len) %>%
  select(-chr_len)

#3) accumuated SNP position
Snp_pos <- chr_pos %>%
  left_join(data, ., by="CHROM") %>%
  arrange(CHROM, MIDPOINT) %>%
  mutate(BPcum = MIDPOINT + total) 
head(Snp_pos)
#4) X axis position of each chromosome
X_axis <-  Snp_pos %>% group_by(CHROM) %>% summarize(center=(max(BPcum) + min(BPcum)) / 2 )


######################## (1) 1% Fst  ##########################  
base
new <- Snp_pos[which(Snp_pos$CHROM != 'LG12'),]
baseline<-quantile(new$Fst,.99,na.rm = T)


data1 <- Snp_pos %>% mutate(is_highlight = ifelse(Snp_pos$Fst >= baseline & Snp_pos$CHROM != "LG12", "yes","no"))

top_1<-ggplot(data=data1, aes(x=BPcum, y=Fst)) +
  geom_point(aes(color=CHROM), alpha=0.8, size=1.3) +
  scale_color_manual(values = rep(c("steelblue", "#989898"), 22)) +
  scale_x_continuous(label = c(1:23), breaks= X_axis$center ) + guides(color=FALSE)+
  scale_y_continuous(expand = c(0, 0) ) + plot_setting + theme(axis.title.x=element_blank())+
  ylab(expression(bold(paste(Intersexual," ", F[ST])))) + ggtitle("") + xlab("Chromosome") + ylim(-0.02,0.5) +
  geom_point(data = subset(data1, is_highlight=="yes"), aes(x=BPcum, y=Fst), size=1.3, color="orange") +
  geom_point(data = subset(data1, CHROM == "LG12"), aes(x=BPcum, y=Fst), size=1.3, color="lightgrey") +
  geom_hline(yintercept = baseline, color = 'red', size= 0.5)

################# (2) Permutation P-values #####################
data <- Snp_pos %>% mutate(is_highlight = ifelse(-log10(Snp_pos$Pvalue) > 3 & Snp_pos$CHROM != "LG12", "yes","no"))

permu_p<-ggplot(data=data, aes(x=BPcum, y=-log10(Pvalue))) +
  geom_point(aes(color=CHROM), alpha=0.8, size=1.3) +
  scale_color_manual(values = rep(c("steelblue", "#989898"), 22)) +
  scale_x_continuous(label = c(1:23), breaks= X_axis$center ) + guides(color=FALSE)+
  scale_y_continuous(expand = c(0, 0) ) + plot_setting + theme(axis.title.x=element_blank())+
  ylab(expression(bold(paste(-Log[10], (italic(P)))))) + ggtitle("") + xlab("Chromosome") + ylim(0,5) +
  geom_point(data = subset(data, is_highlight=="yes"), aes(x=BPcum, y=-log10(Pvalue)), size=1.3, color="orange") +
  geom_point(data = subset(data, CHROM == "LG12"), aes(x=BPcum, y=-log10(Pvalue)), size=1.3, color="lightgrey") +
  geom_hline(yintercept = 3, color = 'red', size= 0.5)

############# (3) Fisher's exact test P-values ###################
data2 <- Snp_pos %>% mutate(is_highlight = ifelse(-log10(Snp_pos$Pvalue2) > 3 & Snp_pos$CHROM != "LG12", "yes","no"))

fisher_p<-ggplot(data=data2, aes(x=BPcum, y=-log10(Pvalue2))) +
  geom_point(aes(color=CHROM), alpha=0.8, size=1.3) +
  scale_color_manual(values = rep(c("steelblue", "#989898"), 22)) +
  scale_x_continuous(label = c(1:23), breaks= X_axis$center ) + guides(color=FALSE)+
  scale_y_continuous(expand = c(0, 0) ) + plot_setting + theme(axis.title.x=element_blank()) +
  ylab(expression(bold(paste(-Log[10], (italic(P)))))) + ggtitle("") + xlab("Chromosome") + ylim(0,20) +
  geom_point(data = subset(data2, is_highlight=="yes"), aes(x=BPcum, y=-log10(Pvalue2)), size=1.3, color="orange") +
  geom_point(data = subset(data2, CHROM == "LG12"), aes(x=BPcum, y=-log10(Pvalue2)), size=1.3, color="lightgrey") +
  geom_hline(yintercept = 3, color = 'red', size= 0.5)


##############04. Bayescan ###########################
#bayscan_Fst <- ggplot(data=Snp_pos, aes(x=BPcum, y=Fst)) +
#  geom_point(aes(color=CHROM), alpha=0.8, size=1.3) +
#  scale_color_manual(values = rep(c("steelblue", "#989898"), 22)) +
#  scale_x_continuous(label = c(1:23), breaks= X_axis$center ) + guides(color=FALSE)+
#  scale_y_continuous(expand = c(0, 0) ) + plot_setting + 
#  ylab(expression(bold(paste(Intersexual," ", F[ST])))) + ggtitle("") + xlab("Chromosome") + ylim(-0.02,0.5) +
#  geom_point(data = subset(Snp_pos, CHROM == "LG12"), aes(x=BPcum, y=Fst), size=1.3, color="lightgrey") +
#  geom_point(data = subset(Snp_pos, bayescan=="yes"), aes(x=BPcum, y=Fst), size=1.3, color="orange") 

########## 04. combined outlier ######################
data3 <- Snp_pos %>% mutate(is_highlight = ifelse(-log10(Snp_pos$Pvalue) > 3 &-log10(Snp_pos$Pvalue2) > 3 & Snp_pos$CHROM != "LG12", "yes","no"))

combined <- ggplot(data=data3, aes(x=BPcum, y=Fst)) +
  geom_point(aes(color=CHROM), alpha=0.8, size=1.3) +
  scale_color_manual(values = rep(c("steelblue", "#989898"), 22)) +
  scale_x_continuous(label = c(1:23), breaks= X_axis$center ) + guides(color=FALSE)+
  scale_y_continuous(expand = c(0, 0) ) + plot_setting + 
  ylab(expression(bold(paste(Intersexual," ",F[ST])))) + ggtitle("") + xlab("Chromosome")  + ylim(-0.0188679,0.5) +
  geom_point(data = subset(data3, is_highlight=="yes"), aes(x=BPcum, y=Fst), size=1.5, color="orange") +
  geom_point(data = subset(data3, CHROM == "LG12"), aes(x=BPcum, y=Fst), size=1.3, color="lightgrey") 



################ integrate plots #####################
top_1 + permu_p + fisher_p + combined + plot_layout(nrow = 4) + plot_annotation(tag_levels = 'A') & theme(plot.tag = element_text(size = 25, face = 'bold'))
# save plot
setwd("~/")
ggsave("Supp_Fig_1_ABCD.png",dpi = 900, height = 52, width = 39, units = "cm", limitsize = FALSE)
ggsave("Supp_Fig_1_ABCD.pdf",dpi = 900, height = 52, width = 39, units = "cm", limitsize = FALSE)
