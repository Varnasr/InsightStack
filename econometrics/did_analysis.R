# Difference-in-Differences Analysis in R
# Uses sample program evaluation data
#
# Requirements: tidyverse, fixest (for robust standard errors)

library(tidyverse)

# Load data
data_path <- file.path(dirname(sys.frame(1)$ofile), "sample_program_data.csv")
df <- read_csv(data_path, show_col_types = FALSE)

# Basic DiD estimation
cat("=== Basic DiD ===\n")
did_model <- lm(outcome ~ treatment + post + treatment:post, data = df)
summary(did_model)

att <- coef(did_model)["treatment:post"]
cat(sprintf("\nATT (interaction coefficient): %.2f\n", att))

# DiD with covariates
cat("\n=== DiD with Covariates ===\n")
did_cov <- lm(outcome ~ treatment + post + treatment:post + age + female + education_years,
               data = df)
summary(did_cov)

# Group means for visual check
cat("\n=== Group Means ===\n")
df %>%
  group_by(treatment, post) %>%
  summarise(
    mean_outcome = mean(outcome),
    sd_outcome = sd(outcome),
    n = n(),
    .groups = "drop"
  ) %>%
  print()

# Event study plot (simple version with 2 periods)
means <- df %>%
  group_by(treatment, post) %>%
  summarise(outcome = mean(outcome), .groups = "drop")

ggplot(means, aes(x = factor(post, labels = c("Pre", "Post")),
                   y = outcome,
                   color = factor(treatment, labels = c("Control", "Treatment")),
                   group = treatment)) +
  geom_point(size = 3) +
  geom_line(linewidth = 1) +
  labs(x = "Period", y = "Outcome", color = "Group",
       title = "Difference-in-Differences") +
  theme_minimal()

ggsave("did_plot.png", width = 7, height = 4, dpi = 150)
cat("Saved: did_plot.png\n")
