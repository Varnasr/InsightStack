# ---------------------------------------------------------------------------
# Read PLFS unit-level data: fixed-width text, driven by the round's own layout.
#
# PLFS arrives from MoSPI's microdata portal as plain text with no delimiters,
# no header and no column names, plus a separate layout spreadsheet giving each
# field's block, name, byte position and length. Nothing in the text file tells
# you where a column starts. Everything here is therefore driven by the layout
# you downloaded with your data: positions change between rounds, and a script
# that hardcodes them quietly reads the wrong bytes a year later.
#
#   source("load_plfs.R")
#   layout <- read_layout("Data_LayoutPLFS_2022.csv")
#   hh <- read_fixed_width("CHHV1.txt", layout, block = "household")
#   hh <- apply_weight(hh, kind = "combined")
#
# No data ships with this script. Register at microdata.gov.in and download the
# round you want; see README.md.
#
# Requires: readr
# ---------------------------------------------------------------------------

suppressPackageStartupMessages(library(readr))

# Field names in the MoSPI README for PLFS January-December 2022. Names are
# stable across recent rounds; byte positions are not, which is why they are
# read from the layout rather than written here.
PLFS_WEIGHT_FIELD <- "MLTS"
PLFS_SUBSAMPLE_FSU_FIELD <- "NSS"
PLFS_COMBINED_FSU_FIELD <- "NSC"

PLFS_KEY_FIELDS <- c("Quarter", "FSU_Serial_No", "Hamlet_Group_Sub_Block_No",
                     "Second_Stage_Stratum_No", "Sample_Household_No")


#' Read a layout into the canonical form and check that it is usable
#'
#' Column names are matched loosely, because the header wording varies between
#' rounds ("Byte Position", "Start", "Position (From)" have all appeared).
#'
#' Positions in MoSPI layouts are 1-indexed and inclusive. R happens to agree,
#' which removes one trap the Python version has to handle explicitly, but the
#' inclusive end still has to be computed as start + length - 1.
read_layout <- function(path) {
  raw <- utils::read.csv(path, stringsAsFactors = FALSE, check.names = FALSE)
  key <- tolower(gsub("_", " ", trimws(names(raw))))
  canon <- names(raw)
  canon[key %in% c("block", "block no", "block number", "schedule block")] <- "block"
  canon[key %in% c("name", "field name", "column name", "variable", "variable name")] <- "name"
  canon[key %in% c("start", "byte position", "position from", "from", "start position")] <- "start"
  canon[key %in% c("length", "size", "bytes", "field length")] <- "length"
  canon[key %in% c("decimals", "decimal", "no of decimals", "decimal places")] <- "decimals"
  canon[key %in% c("label", "description", "field description")] <- "label"
  names(raw) <- canon

  missing <- setdiff(c("name", "start", "length"), names(raw))
  if (length(missing)) {
    stop("The layout is missing ", paste(missing, collapse = ", "),
         ". Rename the columns of your MoSPI layout export to match.", call. = FALSE)
  }
  if (!"block" %in% names(raw)) raw$block <- ""
  if (!"decimals" %in% names(raw)) raw$decimals <- 0
  if (!"label" %in% names(raw)) raw$label <- ""

  layout <- data.frame(
    block = as.character(raw$block),
    name = trimws(as.character(raw$name)),
    start = suppressWarnings(as.numeric(raw$start)),
    length = suppressWarnings(as.numeric(raw$length)),
    decimals = suppressWarnings(as.numeric(raw$decimals)),
    label = as.character(raw$label),
    stringsAsFactors = FALSE
  )
  layout$decimals[is.na(layout$decimals)] <- 0
  layout <- layout[!is.na(layout$start) & !is.na(layout$length), , drop = FALSE]
  layout$start <- as.integer(layout$start)
  layout$length <- as.integer(layout$length)
  layout$decimals <- as.integer(layout$decimals)
  layout$end <- layout$start + layout$length - 1L

  validate_layout(layout)
  rownames(layout) <- NULL
  layout
}


#' Refuse a layout that cannot describe a real file, and report the odd bits
#'
#' Overlapping fields are fatal: two columns cannot occupy one byte, and the
#' usual cause is a transcription slip that shifts everything after it. Gaps are
#' not fatal, because MoSPI layouts do legitimately leave filler bytes.
validate_layout <- function(layout) {
  if (any(layout$start < 1)) {
    stop("Positions must be 1-indexed; these start below 1: ",
         paste(layout$name[layout$start < 1], collapse = ", "), call. = FALSE)
  }
  if (any(layout$length < 1)) {
    stop("These fields have a length below 1: ",
         paste(layout$name[layout$length < 1], collapse = ", "), call. = FALSE)
  }
  problems <- character(0)
  for (blk in unique(layout$block)) {
    chunk <- layout[layout$block == blk, , drop = FALSE]
    chunk <- chunk[order(chunk$start), , drop = FALSE]
    prev_end <- 0L
    prev_name <- NULL
    for (i in seq_len(nrow(chunk))) {
      if (chunk$start[i] <= prev_end) {
        stop("In block '", blk, "', ", chunk$name[i], " starts at byte ",
             chunk$start[i], " but ", prev_name, " already runs to byte ", prev_end,
             ". Overlapping fields usually mean a shifted row in the layout, and ",
             "every field after it will read the wrong bytes.", call. = FALSE)
      }
      if (!is.null(prev_name) && chunk$start[i] > prev_end + 1L) {
        problems <- c(problems, sprintf("block %s: bytes %d-%d unused between %s and %s",
                                        blk, prev_end + 1L, chunk$start[i] - 1L,
                                        prev_name, chunk$name[i]))
      }
      prev_end <- chunk$end[i]
      prev_name <- chunk$name[i]
    }
  }
  invisible(problems)
}


#' Read a PLFS text file using the layout
#'
#' `block` selects one block of the schedule and `columns` selects field names.
#' Reading only what you need matters: the person file for a single year runs to
#' several hundred thousand records.
read_fixed_width <- function(path, layout, block = NULL, columns = NULL,
                             apply_decimals = TRUE, quiet = FALSE) {
  spec <- layout
  if (!is.null(block)) {
    spec <- spec[as.character(spec$block) == as.character(block), , drop = FALSE]
    if (!nrow(spec)) {
      stop("No block '", block, "' in the layout. Available: ",
           paste(sort(unique(layout$block)), collapse = ", "), call. = FALSE)
    }
  }
  if (!is.null(columns)) {
    absent <- setdiff(columns, spec$name)
    if (length(absent) && !quiet) {
      message("  not in this layout: ", paste(absent, collapse = ", "))
    }
    spec <- spec[spec$name %in% columns, , drop = FALSE]
    if (!nrow(spec)) stop("None of the requested fields exist in this layout.", call. = FALSE)
  }
  spec <- spec[order(spec$start), , drop = FALSE]

  df <- as.data.frame(readr::read_fwf(
    path,
    readr::fwf_positions(spec$start, spec$end, col_names = spec$name),
    col_types = readr::cols(.default = readr::col_character()),
    progress = FALSE
  ), stringsAsFactors = FALSE)

  check_record_length(path, spec, quiet = quiet)
  for (nm in spec$name) df[[nm]] <- suppressWarnings(as.numeric(trimws(df[[nm]])))
  if (apply_decimals) df <- apply_implied_decimals(df, spec, quiet = quiet)
  if (!quiet) message(sprintf("  %s records, %d fields",
                              format(nrow(df), big.mark = ","), ncol(df)))
  df
}


#' Divide each field by ten to the power of its declared decimal places
#'
#' PLFS stores decimals implicitly: MLTS is ten bytes holding a number with two
#' implied decimal places, so 0000123456 means 1234.56. The scale comes from the
#' layout rather than from anything in this script, so it stays right when a
#' round changes it.
apply_implied_decimals <- function(df, spec, quiet = FALSE) {
  for (i in seq_len(nrow(spec))) {
    nm <- spec$name[i]
    d <- spec$decimals[i]
    if (!is.na(d) && d > 0 && nm %in% names(df)) {
      df[[nm]] <- df[[nm]] / (10 ^ d)
      if (!quiet) message(sprintf("  %s: %d implied decimal place(s)", nm, d))
    }
  }
  df
}


#' Compare the file's line length against the last byte the layout describes
check_record_length <- function(path, layout, quiet = FALSE) {
  con <- file(path, "r")
  on.exit(close(con))
  first <- readLines(con, n = 1L, warn = FALSE)
  actual <- nchar(sub("\r$", "", first))
  declared <- max(layout$end)
  if (actual != declared && !quiet) {
    message(sprintf(paste0("  record length is %d but the layout describes %d bytes. ",
                           "Check that the layout and the data are from the same round."),
                    actual, declared))
  }
  actual
}


#' Add the final weight, following MoSPI's rule rather than dividing by 100
#'
#' From the README shipped with the data:
#'
#'   For generating sub-sample wise estimate for the Calendar Year, weight may
#'   be applied as follows:
#'        Final Weight = MLTS/100
#'   For generating combined estimate for the Calendar Year (taking both the
#'   subsamples together), weights may be applied as follows:
#'        Final weight = MLTS/100   if NSS=NSC
#'                     = MLTS/200   otherwise.
#'
#' NSS is the number of first stage units surveyed in the sub-sample within a
#' second stage stratum; NSC is the same count for both sub-samples combined.
#' Where they differ, both sub-samples are present and each carries half the
#' weight. Dividing everything by 100 therefore doubles the estimated population
#' exactly where the sub-samples differ, and does so silently: rates barely move,
#' so a participation rate looks fine while every employment total is wrong.
apply_weight <- function(df, kind = c("combined", "subsample"),
                         weight_field = PLFS_WEIGHT_FIELD, quiet = FALSE) {
  kind <- match.arg(kind)
  if (!weight_field %in% names(df)) {
    stop(weight_field, " is not in the data, so no weighted estimate is possible. ",
         "Include it in the fields you read.", call. = FALSE)
  }
  mlts <- as.numeric(df[[weight_field]])

  if (kind == "subsample") {
    df$weight <- mlts / 100
    if (!quiet) message("  sub-sample weight: MLTS/100")
    return(df)
  }
  for (field in c(PLFS_SUBSAMPLE_FSU_FIELD, PLFS_COMBINED_FSU_FIELD)) {
    if (!field %in% names(df)) {
      stop("A combined estimate needs ", PLFS_SUBSAMPLE_FSU_FIELD, " and ",
           PLFS_COMBINED_FSU_FIELD, " to decide between MLTS/100 and MLTS/200, and ",
           field, " is missing. Read it in, or use kind = 'subsample' if that is ",
           "really what you want.", call. = FALSE)
    }
  }
  nss <- as.numeric(df[[PLFS_SUBSAMPLE_FSU_FIELD]])
  nsc <- as.numeric(df[[PLFS_COMBINED_FSU_FIELD]])
  halved <- nss != nsc
  df$weight <- ifelse(halved, mlts / 200, mlts / 100)
  if (!quiet) {
    message(sprintf(paste0("  combined weight: MLTS/100 for %s records, MLTS/200 for ",
                           "%s where NSS differs from NSC"),
                    format(sum(!halved, na.rm = TRUE), big.mark = ","),
                    format(sum(halved, na.rm = TRUE), big.mark = ",")))
  }
  df
}


#' Build the household key by zero-padding each part to its layout length
#'
#' MoSPI's common primary key is Quarter, FSU serial number, hamlet group or
#' sub-block, second stage stratum and sample household number. Concatenating
#' them without padding to the declared field width collapses distinct
#' households onto one key: FSU 1234 with household 5 and FSU 12345 with
#' household nothing both read as "12345". The merge then succeeds and is wrong.
build_key <- function(df, layout, fields = PLFS_KEY_FIELDS, name = "hhid") {
  missing <- setdiff(fields, names(df))
  if (length(missing)) {
    stop("Key fields absent from the data: ", paste(missing, collapse = ", "),
         call. = FALSE)
  }
  widths <- stats::setNames(layout$length, layout$name)
  parts <- lapply(fields, function(f) {
    w <- widths[[f]]
    if (is.null(w) || is.na(w) || w < 1) {
      stop("No length for key field '", f, "' in the layout.", call. = FALSE)
    }
    formatC(as.integer(df[[f]]), width = w, flag = "0", format = "d")
  })
  df[[name]] <- do.call(paste0, parts)
  df
}


#' Attach household fields to person records, refusing a merge that inflates
#'
#' A many-to-many merge on a key that is not unique in the household file
#' multiplies rows and inflates every weighted total. This checks first.
merge_person_household <- function(person, household, on = "hhid", quiet = FALSE) {
  dupes <- sum(duplicated(household[[on]]))
  if (dupes > 0) {
    stop(format(dupes, big.mark = ","), " duplicated ", on, " values in the household ",
         "file, so the merge would multiply person records. Check the key fields and ",
         "the visit or quarter selection before merging.", call. = FALSE)
  }
  before <- nrow(person)
  shared <- setdiff(intersect(names(person), names(household)), on)
  merged <- merge(person, household[, setdiff(names(household), shared), drop = FALSE],
                  by = on, all.x = TRUE, sort = FALSE)
  if (nrow(merged) != before) {
    stop("The merge changed the row count from ", before, " to ", nrow(merged),
         ".", call. = FALSE)
  }
  merged
}
