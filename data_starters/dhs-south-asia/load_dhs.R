# ---------------------------------------------------------------------------
# Load a DHS recode file without exhausting memory, attach the survey design,
# and stop rather than return a wrong number.
#
# Covers every DHS survey in South Asia (see surveys.csv). One loader serves
# India, Bangladesh, Nepal, Pakistan, Maldives, Afghanistan and Sri Lanka,
# because the recode structure is the same in all of them.
#
#   source("load_dhs.R")
#   ir <- read_recode("IAIR7EFL.DTA", c("v012", "v106", "v190"))
#   des <- dhs_design(ir)
#   survey::svymean(~v012, des)
#
# No data ships with this script. Download the files yourself from
# dhsprogram.com once your data request is approved; see README.md.
# ---------------------------------------------------------------------------

# haven reads Stata and SPSS. survey is only needed for dhs_design().
suppressPackageStartupMessages({
  library(haven)
})

# Weight, PSU and strata differ by recode type. Getting this wrong does not
# error; it silently produces standard errors for the wrong design.
DHS_DESIGN <- list(
  IR = c(weight = "v005",  psu = "v021",  strata = "v022",  strata_alt = "v023"),
  KR = c(weight = "v005",  psu = "v021",  strata = "v022",  strata_alt = "v023"),
  BR = c(weight = "v005",  psu = "v021",  strata = "v022",  strata_alt = "v023"),
  CR = c(weight = "v005",  psu = "v021",  strata = "v022",  strata_alt = "v023"),
  MR = c(weight = "mv005", psu = "mv021", strata = "mv022", strata_alt = "mv023"),
  HR = c(weight = "hv005", psu = "hv021", strata = "hv022", strata_alt = "hv023"),
  PR = c(weight = "hv005", psu = "hv021", strata = "hv022", strata_alt = "hv023")
)

DHS_RECODE_NAMES <- c(
  IR = "Individual Recode (women 15-49)", MR = "Men's Recode",
  KR = "Children's Recode (births in the last 5 years, living or dead)",
  BR = "Births Recode (full birth history)", HR = "Household Recode",
  PR = "Household Member Recode", CR = "Couples Recode"
)

# WHO 2006 plausibility bounds. DHS stores these z-scores multiplied by 100 and
# uses values at or above 9990 for flags and missing.
DHS_ANTHRO_BOUNDS <- list(haz = c(-6, 6), waz = c(-6, 5),
                          whz = c(-5, 5), bmiz = c(-5, 5))
DHS_ANTHRO_COLS <- list(haz = c("hw70", "hc70"), waz = c("hw71", "hc71"),
                        whz = c("hw72", "hc72"), bmiz = c("hw73", "hc73"))

# Columns that must not be rescaled from variables.csv, because something else
# owns them. Weights belong to attach_design, which needs the raw value to tell
# a genuine DHS weight from one already divided. Anthropometry belongs to
# clean_anthropometry, which must spot the 9990-and-above flags *before*
# anything divides them down into the plausible range.
DHS_OWNED_ELSEWHERE <- unique(c(
  vapply(DHS_DESIGN, function(d) unname(d["weight"]), character(1)),
  unlist(DHS_ANTHRO_COLS, use.names = FALSE)
))


#' Read country, recode type and phase out of a DHS filename.
#'
#' DHS names files {CC}{RR}{phase}{release}{format}, so IAIR7EFL.DTA is India,
#' Individual Recode, phase 7, release E, flat. Renaming the file breaks this,
#' which is why every function here lets you pass `recode` explicitly.
parse_filename <- function(path) {
  stem <- basename(path)
  m <- regmatches(stem, regexec(
    # The two characters after the recode are the phase number and then a
    # version character that is incremented when DHS reissues the file. That
    # version can be a digit: NFHS-4's individual recode is IAIR74FL.DTA.
    "^([A-Za-z]{2})(IR|MR|KR|BR|HR|PR|CR|GE|HW)([0-9A-Za-z])([0-9A-Za-z])(FL|DT|SV|SD)",
    stem, ignore.case = TRUE))[[1]]
  if (length(m) == 0L) {
    stop(sprintf(paste0("Cannot read a DHS filename out of '%s'. Expected something ",
                        "like IAIR7EFL.DTA. If you renamed the file, pass recode= ",
                        "explicitly."), stem), call. = FALSE)
  }
  list(country = toupper(m[2]), recode = toupper(m[3]), phase = toupper(m[4]),
       release = toupper(m[5]), fmt = toupper(m[6]), path = path)
}


#' Divisors for the variables DHS stores as integers, read from variables.csv so
#' the documented scale and the applied scale cannot drift apart.
scale_factors <- function(recode, csv_path = NULL) {
  if (is.null(csv_path)) csv_path <- file.path(dhs_script_dir(), "variables.csv")
  if (!file.exists(csv_path)) {
    stop(sprintf("Cannot find variables.csv at '%s'. Pass csv_path= explicitly.",
                 csv_path), call. = FALSE)
  }
  tbl <- utils::read.csv(csv_path, stringsAsFactors = FALSE)
  col <- if (recode == "MR") "mr_var" else if (recode %in% c("HR", "PR")) "hr_pr_var" else "ir_kr_br_var"
  keep <- nzchar(trimws(tbl[[col]])) & grepl("^divide by", tolower(trimws(tbl$scale)))
  if (!any(keep)) return(setNames(numeric(0), character(0)))
  vars <- trimws(tbl[[col]][keep])
  divs <- as.numeric(sub("^divide by\\s*", "", tolower(trimws(tbl$scale[keep]))))
  setNames(divs, vars)
}

dhs_script_dir <- function() {
  # Under Rscript.
  args <- commandArgs(trailingOnly = FALSE)
  file_arg <- grep("^--file=", args, value = TRUE)
  if (length(file_arg)) return(dirname(normalizePath(sub("^--file=", "", file_arg[1]))))
  # Under source(), where the path hides in the calling frame.
  for (i in seq_len(sys.nframe())) {
    ofile <- tryCatch(sys.frame(i)$ofile, error = function(e) NULL)
    if (!is.null(ofile)) return(dirname(normalizePath(ofile)))
  }
  getwd()
}


#' Column names without reading any rows.
available_columns <- function(path) {
  reader <- if (grepl("\\.dta$", path, ignore.case = TRUE)) haven::read_dta else haven::read_sav
  names(reader(path, n_max = 0))
}


#' Read selected variables from a DHS recode file.
#'
#' `variables` is the analysis variables you want. The design variables for the
#' recode are added automatically, so you never have to remember that the men's
#' recode weights on mv005 rather than v005.
#'
#' Variables absent from this round are reported rather than silently dropped.
#' That report is the cross-round harmonisation problem made visible: v190 is
#' missing from pre-2000 rounds, and sdist exists only for India from NFHS-4 on.
read_recode <- function(path, variables = NULL, recode = NULL,
                        add_design = TRUE, apply_scales = TRUE, quiet = FALSE) {
  if (is.null(recode)) recode <- parse_filename(path)$recode
  recode <- toupper(recode)
  if (!recode %in% names(DHS_DESIGN)) {
    stop(sprintf("No design defined for recode '%s'. Known: %s",
                 recode, paste(names(DHS_DESIGN), collapse = ", ")), call. = FALSE)
  }
  d <- DHS_DESIGN[[recode]]
  reader <- if (grepl("\\.dta$", path, ignore.case = TRUE)) haven::read_dta else haven::read_sav

  if (!is.null(variables)) {
    wanted <- unique(c(variables, unname(d[c("weight", "psu", "strata", "strata_alt")])))
    present <- available_columns(path)
    missing <- setdiff(wanted, present)
    usecols <- intersect(wanted, present)
    if (length(missing) && !quiet) {
      message("  not in this file: ", paste(missing, collapse = ", "))
    }
    if (!length(usecols)) {
      stop("None of the requested variables exist in this file.", call. = FALSE)
    }
    df <- reader(path, col_select = tidyselect::all_of(usecols))
  } else {
    if (!quiet) message("  reading every column (slow and memory hungry on large surveys)")
    df <- reader(path)
  }

  # Drop value labels so arithmetic works, but leave string keys (caseid, hhid)
  # alone rather than coercing them to NA.
  df <- as.data.frame(
    lapply(df, function(x) if (is.character(x)) x else as.numeric(haven::zap_labels(x))),
    stringsAsFactors = FALSE, check.names = FALSE)
  if (apply_scales) df <- rescale(df, recode, quiet = quiet)
  if (add_design) df <- attach_design(df, recode, quiet = quiet)
  df
}


rescale <- function(df, recode, quiet = FALSE) {
  facs <- scale_factors(recode)
  for (v in names(facs)) {
    if (v %in% names(df) && !v %in% DHS_OWNED_ELSEWHERE) {
      df[[v]] <- df[[v]] / facs[[v]]
      if (!quiet) message(sprintf("  scaled %s by 1/%g", v, facs[[v]]))
    }
  }
  df
}


#' Add weight, psu and strata columns, and complain when the design is broken.
attach_design <- function(df, recode, quiet = FALSE) {
  d <- DHS_DESIGN[[toupper(recode)]]
  wcol <- unname(d["weight"])
  if (!wcol %in% names(df)) {
    stop(sprintf(paste0("%s is missing, so nothing weighted can be computed from ",
                        "this file. Include it in your variable list."), wcol), call. = FALSE)
  }
  raw <- suppressWarnings(as.numeric(df[[wcol]]))
  if (all(is.na(raw))) stop(sprintf("%s is entirely missing.", wcol), call. = FALSE)
  mean_raw <- mean(raw, na.rm = TRUE)
  if (mean_raw < 1000) {
    stop(sprintf(paste0("%s averages %s, far below the ~1,000,000 a raw DHS weight ",
                        "should average. This file looks pre-scaled or is not a DHS ",
                        "recode. Dividing again would shrink every weighted total by ",
                        "a million."), wcol, format(mean_raw, big.mark = ",")), call. = FALSE)
  }
  df$weight <- raw / 1e6

  if (unname(d["psu"]) %in% names(df)) df$psu <- df[[unname(d["psu"])]]
  strata_col <- intersect(unname(d[c("strata", "strata_alt")]), names(df))
  if (length(strata_col)) {
    df$strata <- df[[strata_col[1]]]
    if (!quiet && strata_col[1] == unname(d["strata_alt"])) {
      message(sprintf("  design strata taken from %s (%s absent, normal in older rounds)",
                      strata_col[1], unname(d["strata"])))
    }
  } else if (!quiet) {
    message("  no strata variable found; variance estimates will be wrong ",
            "unless the design really is unstratified")
  }
  df
}


#' Turn DHS anthropometry into usable z-scores.
#'
#' Three things go wrong here and none of them raise an error on their own: the
#' values are stored times 100, flags and missing sit at 9990 and above, and the
#' columns are hw70-hw73 in the children's recode but hc70-hc73 in the household
#' member recode.
clean_anthropometry <- function(df, recode = "KR", quiet = FALSE) {
  idx <- if (toupper(recode) == "PR") 2L else 1L
  for (nm in names(DHS_ANTHRO_COLS)) {
    col <- DHS_ANTHRO_COLS[[nm]][idx]
    if (!col %in% names(df)) next
    raw <- suppressWarnings(as.numeric(df[[col]]))
    flagged <- sum(raw >= 9990, na.rm = TRUE)
    z <- ifelse(is.na(raw) | raw >= 9990, NA_real_, raw / 100)
    b <- DHS_ANTHRO_BOUNDS[[nm]]
    out_of_range <- sum(z < b[1] | z > b[2], na.rm = TRUE)
    z[!is.na(z) & (z < b[1] | z > b[2])] <- NA_real_
    df[[nm]] <- z
    if (!quiet) {
      message(sprintf("  %s from %s: %d flagged or missing, %d outside WHO bounds [%g, %g]",
                      nm, col, flagged, out_of_range, b[1], b[2]))
    }
  }
  df
}


#' Century month code to year and month. CMC 1441 is January 2020.
cmc_to_year_month <- function(cmc) {
  cmc <- as.numeric(cmc)
  year <- 1900 + ((cmc - 1) %/% 12)
  list(year = year, month = cmc - 12 * (year - 1900))
}

year_month_to_cmc <- function(year, month) (year - 1900) * 12 + month


#' A survey design object with the DHS design already set.
#'
#' nest = TRUE because DHS cluster numbers restart within strata.
dhs_design <- function(df) {
  if (!requireNamespace("survey", quietly = TRUE)) {
    stop("dhs_design() needs the survey package: install.packages('survey')", call. = FALSE)
  }
  has_strata <- "strata" %in% names(df) && any(!is.na(df$strata))
  survey::svydesign(
    ids = ~psu,
    strata = if (has_strata) ~strata else NULL,
    weights = ~weight,
    data = df,
    nest = TRUE
  )
}


summarise_recode <- function(df) {
  cat(sprintf("  rows: %s\n", format(nrow(df), big.mark = ",")))
  cat(sprintf("  columns: %d\n", ncol(df)))
  if ("weight" %in% names(df)) {
    cat(sprintf("  sum of weights: %s (should be close to the unweighted row count)\n",
                format(round(sum(df$weight, na.rm = TRUE)), big.mark = ",")))
  }
  if ("psu" %in% names(df)) {
    cat(sprintf("  clusters: %s\n", format(length(unique(df$psu)), big.mark = ",")))
  }
  if ("strata" %in% names(df)) {
    cat(sprintf("  strata: %s\n", format(length(unique(df$strata)), big.mark = ",")))
  }
  invisible(df)
}
