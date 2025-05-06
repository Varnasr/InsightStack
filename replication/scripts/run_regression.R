data <- read.csv('../data/simulated_study_data.csv')

model <- lm(outcome ~ treatment + age + income, data=data)
summary_out <- summary(model)

sink("../output/results_r.txt")
print(summary_out)
sink()