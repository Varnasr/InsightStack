# Validate a data frame against a data dictionary: duplicates, required, ranges,
# allowed values. R companion to data_validation/validate.py, which is the
# reference and does more. Base R, no packages.
#
#   source("data_validation/companions/validate.R")
#   issues <- validate_against_dictionary(df, "data_validation/sample_data/data_dictionary.csv", id = "id")

validate_against_dictionary <- function(df, dictionary_path, id,
                                        sentinels = c(-999, -998, -99, -88, -9)) {
  dict <- read.csv(dictionary_path, stringsAsFactors = FALSE, colClasses = "character")
  dict[is.na(dict)] <- ""
  if (!id %in% names(df)) stop("no id column ", id, call. = FALSE)

  issue <- function(check, ids, variable, value, message) {
    data.frame(check = check, id = as.character(ids), variable = variable,
               value = as.character(value), message = message, stringsAsFactors = FALSE)
  }
  is_blank <- function(x) {
    if (is.numeric(x)) return(is.na(x) | x %in% sentinels)
    t <- trimws(as.character(x))
    is.na(x) | t %in% c("", ".", "NA", "N/A", "n/a") | suppressWarnings(as.numeric(t)) %in% sentinels
  }
  out <- list()

  ids <- df[[id]]
  bl <- is_blank(ids)
  if (any(bl)) out[[length(out) + 1]] <- issue("id_blank", paste("row", which(bl)), id, NA, "identifier is blank")
  dup <- duplicated(ids[!bl]) | duplicated(ids[!bl], fromLast = TRUE)
  if (any(dup)) {
    tab <- table(ids[!bl][dup])
    out[[length(out) + 1]] <- issue("id_duplicate", names(tab), id, as.integer(tab), "identifier appears more than once")
  }

  for (i in seq_len(nrow(dict))) {
    v <- trimws(dict$variable[i]); if (!nzchar(v)) next
    if (!v %in% names(df)) {
      out[[length(out) + 1]] <- issue("column_missing", "(file)", v, NA, "in the dictionary, absent from the file"); next
    }
    x <- df[[v]]; blank <- is_blank(x)
    if ("required" %in% names(dict) && tolower(dict$required[i]) %in% c("yes", "y", "true", "1") && any(blank)) {
      out[[length(out) + 1]] <- issue("required_blank", ids[blank], v, NA, paste(v, "is required but blank"))
    }
    lo <- if ("min" %in% names(dict)) dict$min[i] else ""; hi <- if ("max" %in% names(dict)) dict$max[i] else ""
    if (nzchar(lo) || nzchar(hi)) {
      num <- suppressWarnings(as.numeric(as.character(x))); num[blank] <- NA
      bad <- !is.na(num) & ((nzchar(lo) & num < as.numeric(lo)) | (nzchar(hi) & num > as.numeric(hi)))
      if (any(bad)) out[[length(out) + 1]] <- issue("out_of_range", ids[bad], v, num[bad],
                                                    sprintf("%s outside [%s, %s]", v, ifelse(nzchar(lo), lo, "-inf"), ifelse(nzchar(hi), hi, "inf")))
    }
    if ("allowed" %in% names(dict) && nzchar(dict$allowed[i])) {
      opts <- trimws(strsplit(dict$allowed[i], "|", fixed = TRUE)[[1]])
      vals <- trimws(as.character(x)); bad <- !blank & !vals %in% opts
      if (any(bad)) out[[length(out) + 1]] <- issue("not_allowed", ids[bad], v, vals[bad], paste(v, "not one of", paste(opts, collapse = ", ")))
    }
  }
  if (!length(out)) return(data.frame(check = character(), id = character(), variable = character(),
                                      value = character(), message = character(), stringsAsFactors = FALSE))
  do.call(rbind, out)
}
