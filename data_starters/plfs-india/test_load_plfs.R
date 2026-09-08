# Tests for load_plfs.R, run against the synthetic fixtures rather than real
# PLFS data. Mirrors test_load_plfs.py, so both languages are held to the same
# standard.
#
#   python make_fixture.py --outdir fixtures
#   Rscript test_load_plfs.R

source("load_plfs.R")

failures <- character(0)
check <- function(name, condition, detail = "") {
  if (isTRUE(condition)) {
    cat(sprintf("  ok    %s\n", name))
  } else {
    cat(sprintf("  FAIL  %s%s\n", name, if (nzchar(detail)) paste0(": ", detail) else ""))
    failures <<- c(failures, name)
  }
}
errors <- function(expr) inherits(try(expr, silent = TRUE), "try-error")

LAYOUT <- "fixtures/layout.csv"; HH <- "fixtures/CHHV1.txt"; PER <- "fixtures/CPerV1.txt"

cat("layout\n")
layout <- read_layout(LAYOUT)
check("layout read", nrow(layout) > 0, sprintf("%d fields", nrow(layout)))
check("end position derived", layout$end[1] == layout$start[1] + layout$length[1] - 1L)
hh_layout <- layout[layout$block == "household", ]
check("household block ends where the record ends", max(hh_layout$end) == 37,
      as.character(max(hh_layout$end)))

bad <- layout; bad$start[bad$name == "State"] <- 2L
bad$end <- bad$start + bad$length - 1L
check("overlapping fields are rejected", errors(validate_layout(bad)))
zero <- layout; zero$start[zero$name == "State"] <- 0L
check("a 0-indexed layout is rejected", errors(validate_layout(zero)))

cat("fixed-width reading\n")
hh <- read_fixed_width(HH, layout, block = "household", quiet = TRUE)
check("all household records read", nrow(hh) == 240, as.character(nrow(hh)))
check("quarter is in range 1 to 4", all(hh$Quarter >= 1 & hh$Quarter <= 4))
check("sector is 1 or 2", all(hh$Sector %in% c(1, 2)))
check("household size is plausible", all(hh$Household_Size >= 1 & hh$Household_Size <= 8))
check("FSU serial numbers are five digits",
      all(hh$FSU_Serial_No >= 10000 & hh$FSU_Serial_No <= 99999))

cat("implied decimals\n")
check("MLTS divided by its two implied decimal places", mean(hh$MLTS) < 10000,
      sprintf("mean %.2f", mean(hh$MLTS)))
raw <- read_fixed_width(HH, layout, block = "household", apply_decimals = FALSE, quiet = TRUE)
check("the raw field is exactly 100 times the scaled one",
      isTRUE(all.equal(raw$MLTS / 100, hh$MLTS)))
check("integer fields are left alone", all(raw$Household_Size == hh$Household_Size))

cat("the weight rule\n")
combined <- apply_weight(hh, "combined", quiet = TRUE)
subsample <- apply_weight(hh, "subsample", quiet = TRUE)
differ <- combined$NSS != combined$NSC
check("some second stage strata have NSS different from NSC",
      any(differ) && any(!differ), sprintf("%d of %d", sum(differ), length(differ)))
check("MLTS/200 where NSS differs from NSC",
      isTRUE(all.equal(combined$weight[differ], combined$MLTS[differ] / 200)))
check("MLTS/100 where NSS equals NSC",
      isTRUE(all.equal(combined$weight[!differ], combined$MLTS[!differ] / 100)))
check("a sub-sample estimate always uses MLTS/100",
      isTRUE(all.equal(subsample$weight, subsample$MLTS / 100)))
naive <- sum(hh$MLTS / 100 * hh$Household_Size)
correct <- sum(combined$weight * combined$Household_Size)
check("the naive divide-by-100 inflates the population total", naive > correct * 1.2,
      sprintf("%.0f against %.0f", naive, correct))
check("a combined weight without NSC is refused",
      errors(apply_weight(hh[, setdiff(names(hh), "NSC")], "combined", quiet = TRUE)))

cat("keys\n")
hh_keyed <- build_key(combined, layout)
widths <- stats::setNames(layout$length, layout$name)
expected <- sum(sapply(PLFS_KEY_FIELDS, function(f) widths[[f]]))
check("every key is the same length",
      identical(unique(nchar(hh_keyed$hhid)), as.integer(expected)),
      paste(unique(nchar(hh_keyed$hhid)), collapse = ","))
check("keys are unique in the household file", !any(duplicated(hh_keyed$hhid)))
unpadded <- paste0(as.integer(combined$FSU_Serial_No), as.integer(combined$Sample_Household_No))
check("the padded key has at least as many distinct values as the unpadded one",
      length(unique(hh_keyed$hhid)) >= length(unique(unpadded)))

cat("merging person to household\n")
per <- build_key(read_fixed_width(PER, layout, block = "person", quiet = TRUE), layout)
merged <- merge_person_household(per, hh_keyed, quiet = TRUE)
check("the merge does not change the person row count", nrow(merged) == nrow(per),
      sprintf("%d against %d", nrow(merged), nrow(per)))
check("every person matched a household", !any(is.na(merged$Household_Size)))

# The strongest check available without real data: household size was written
# into one file and the members into another, so they agree only if the byte
# positions, the key padding and the merge are all correct.
counted <- table(merged$hhid)
declared <- stats::setNames(hh_keyed$Household_Size, hh_keyed$hhid)
check("declared household size equals the number of person records",
      all(as.integer(counted) == as.integer(declared[names(counted)])),
      sprintf("%d disagree", sum(as.integer(counted) != as.integer(declared[names(counted)]))))
check("a duplicated household key is refused",
      errors(merge_person_household(per, rbind(hh_keyed, head(hh_keyed, 3)), quiet = TRUE)))

cat("record length\n")
check("record length matches the layout",
      check_record_length(HH, hh_layout, quiet = TRUE) == 37)

cat("\n")
if (length(failures)) {
  cat(sprintf("FAIL: %d check(s) failed: %s\n", length(failures),
              paste(failures, collapse = ", ")))
  quit(status = 1)
}
cat("PASS\n")
