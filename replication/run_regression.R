# The same model in R, writing the same key results, so the two can be compared.
#
#   Rscript replication/run_regression.R
#
# Coefficients and R-squared must match the Python run to six places; standard
# errors are not compared, because this uses lm()'s conventional errors and the
# Python uses HC1, and installing `sandwich` is not worth it for a check that
# the point estimates agree.

args <- commandArgs(trailingOnly = TRUE)
root <- if (file.exists("replication/data/simulated_study_data.csv")) "replication" else "."
data <- read.csv(file.path(root, "data", "simulated_study_data.csv"))
stopifnot(!any(duplicated(data$id)))

model <- lm(outcome ~ treatment + age + income, data = data)
s <- summary(model)

dir.create(file.path(root, "output"), showWarnings = FALSE)
sink(file.path(root, "output", "model_summary_r.txt")); print(s); sink()

key <- list(
  n = nobs(model),
  r_squared = round(unname(s$r.squared), 6),
  treatment_estimate = round(unname(coef(model)["treatment"]), 6),
  outcome_mean_control = round(mean(data$outcome[data$treatment == 0]), 6),
  outcome_mean_treated = round(mean(data$outcome[data$treatment == 1]), 6)
)
json <- paste0("{\n", paste(sprintf('  "%s": %s', names(key),
               vapply(key, function(v) format(v, digits = 15), "")), collapse = ",\n"), "\n}\n")
writeLines(json, file.path(root, "output", "key_results_r.json"))
cat("R: treatment estimate", key$treatment_estimate, " R2", key$r_squared, "\n")
