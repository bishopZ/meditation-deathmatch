
setwd('~/Projects/eeg/meditation-deathmatch/python-server/')
filename <- 'md_20140729-000237.csv'

library(plyr)
library(reshape2)
library(ggplot2)

results <- read.csv(filename)
p1 <- results[,1:10]
p2 <- results[,11:20]

colnames <- c('attention', 'meditation', 'delta', 'theta', 'lowAlpha', 
             'highAlpha', 'lowBeta', 'highBeta', 'lowGamma', 'highGamma')
names(p1) <- colnames
names(p2) <- colnames

p1['time'] <- 1:nrow(p1)
p2['time'] <- 1:nrow(p2)

meltdf <- melt(p1, 'time')
ggplot(meltdf, aes(x=time,y=value,colour=variable,group=variable)) + geom_line()

meters <- rbind(meltdf[ which(meltdf$variable=='attention'),], 
                 meltdf[ which(meltdf$variable=='meditation'),])
ggplot(meters, aes(x=time,y=value,colour=variable,group=variable)) + geom_line()




