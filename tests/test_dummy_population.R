# Basic test for sample population projection CSV
data <- read.csv("../sample_data/population_projection_dummy.csv")

# Check expected columns
stopifnot(all(c("district", "year", "projected_population") %in% names(data)))

# Check for no missing values
stopifnot(!any(is.na(data)))

cat("All tests passed.\n")
