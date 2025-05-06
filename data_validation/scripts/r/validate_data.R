
df <- read.csv('../sample_data/sample_data.csv')

# Missing values
cat("Missing values:\n")
print(colSums(is.na(df)))

# Duplicates
cat("\nDuplicate IDs:\n")
print(df[duplicated(df$id), ])

# Invalid gender
cat("\nInvalid gender values:\n")
print(subset(df, !(gender %in% c('M', 'F'))))
