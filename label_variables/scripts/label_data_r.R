library(haven)
library(dplyr)

# Load your data and dictionary
data <- read_dta("your_data_file.dta")
dict <- read.csv("../input/data_dictionary.csv")

# Apply labels
for (i in 1:nrow(dict)) {
  varname <- dict$variable[i]
  label <- dict$label[i]
  attr(data[[varname]], "label") <- label
}

write_dta(data, "your_data_file_labelled.dta")