# Propensity Score Matching in R
# Uses MatchIt for flexible matching methods
#
# Requirements: tidyverse, MatchIt

library(tidyverse)

# If MatchIt is not available, provide instructions
if (!requireNamespace("MatchIt", quietly = TRUE)) {
  cat("Install MatchIt: install.packages('MatchIt')\n")
  cat("Running without matching...\n\n")
} else {
  library(MatchIt)
}

# Load baseline data
data_path <- file.path(dirname(sys.frame(1)$ofile), "sample_program_data.csv")
df <- read_csv(data_path, show_col_types = FALSE) %>%
  filter(post == 0)

cat("=== Data Summary ===\n")
cat(sprintf("Treatment: %d, Control: %d\n",
            sum(df$treatment == 1), sum(df$treatment == 0)))

# Estimate propensity scores
cat("\n=== Propensity Score Model ===\n")
ps_model <- glm(treatment ~ age + female + education_years + income_baseline,
                 family = binomial, data = df)
summary(ps_model)

df$pscore <- predict(ps_model, type = "response")

cat(sprintf("\nTreatment mean pscore: %.3f\n", mean(df$pscore[df$treatment == 1])))
cat(sprintf("Control mean pscore: %.3f\n", mean(df$pscore[df$treatment == 0])))

# Matching with MatchIt (if available)
if (requireNamespace("MatchIt", quietly = TRUE)) {
  cat("\n=== Nearest Neighbor Matching ===\n")
  m_out <- matchit(treatment ~ age + female + education_years + income_baseline,
                    data = df, method = "nearest", caliper = 0.2)
  summary(m_out)

  # Balance check
  cat("\n=== Balance Summary ===\n")
  matched_data <- match.data(m_out)
  cat(sprintf("Matched observations: %d\n", nrow(matched_data)))

  # ATT on matched sample
  att_model <- lm(baseline_outcome ~ treatment, data = matched_data)
  cat(sprintf("\nATT: %.3f (SE: %.3f)\n",
              coef(att_model)["treatment"],
              summary(att_model)$coefficients["treatment", "Std. Error"]))
}
