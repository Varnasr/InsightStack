# Apply variable and value labels from a data dictionary CSV, and write a
# labelled .dta or .sav. R companion to label_variables/labels.py. Needs haven.
#
#   source("label_variables/companions/label.R")
#   df <- label_from_dictionary(df, "label_variables/input/data_dictionary.csv")
#   haven::write_dta(df, "out.dta")

label_from_dictionary <- function(df, dictionary_path, strict = FALSE) {
  dict <- read.csv(dictionary_path, stringsAsFactors = FALSE, colClasses = "character")
  dict[is.na(dict)] <- ""
  dict$variable <- trimws(dict$variable)
  dict <- dict[nzchar(dict$variable), ]

  missing_col <- setdiff(dict$variable, names(df))
  unlabelled  <- setdiff(names(df), dict$variable)
  if (strict && (length(missing_col) || length(unlabelled))) {
    stop("dictionary entries with no column: ", paste(missing_col, collapse = ", "),
         "; columns with no entry: ", paste(unlabelled, collapse = ", "), call. = FALSE)
  }

  for (i in seq_len(nrow(dict))) {
    v <- dict$variable[i]
    if (!v %in% names(df)) next
    attr(df[[v]], "label") <- dict$label[i]
    spec <- if ("values" %in% names(dict)) trimws(dict$values[i]) else ""
    if (nzchar(spec) && is.numeric(df[[v]])) {
      pairs <- strsplit(strsplit(spec, "|", fixed = TRUE)[[1]], "=", fixed = TRUE)
      codes <- as.numeric(vapply(pairs, `[`, "", 1))
      labs  <- vapply(pairs, function(p) paste(p[-1], collapse = "="), "")
      df[[v]] <- haven::labelled(df[[v]], stats::setNames(codes, labs),
                                 label = dict$label[i])
    }
  }
  if (length(unlabelled)) message("unlabelled: ", paste(unlabelled, collapse = ", "))
  if (length(missing_col)) message("no such column: ", paste(missing_col, collapse = ", "))
  df
}
