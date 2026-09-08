# Tests for load_dhs.R, run against the synthetic fixtures rather than real DHS
# data. Mirrors test_load_dhs.py check for check, so the two languages are held
# to the same standard.
#
#   python make_fixture.py --outdir fixtures
#   Rscript test_load_dhs.R

source("load_dhs.R")

failures <- character(0)

check <- function(name, condition, detail = "") {
  ok <- isTRUE(condition)
  if (ok) {
    cat(sprintf("  ok    %s\n", name))
  } else {
    cat(sprintf("  FAIL  %s%s\n", name, if (nzchar(detail)) paste0(": ", detail) else ""))
    failures <<- c(failures, name)
  }
}

cat("filename parsing\n")
f <- parse_filename("fixtures/XXIR7AFL.DTA")
check("recode read from filename", f$recode == "IR", f$recode)
check("phase read from filename", f$phase == "7", f$phase)
check("a renamed file is rejected",
      inherits(try(parse_filename("women_final.dta"), silent = TRUE), "try-error"))
check("NFHS-4 style IAIR74FL parses", parse_filename("IAIR74FL.DTA")$recode == "IR")
check("NFHS-5 style IAIR7EFL parses", parse_filename("IAIR7EFL.DTA")$recode == "IR")
check("Bangladesh BDKR81FL parses", parse_filename("BDKR81FL.DTA")$recode == "KR")
check("country code read correctly", parse_filename("NPIR82FL.DTA")$country == "NP")

cat("weights\n")
ir <- read_recode("fixtures/XXIR7AFL.DTA", c("v012", "v106", "v190"), quiet = TRUE)
check("weight column added", "weight" %in% names(ir))
check("weight divided by a million", abs(mean(ir$weight) - 1) < 0.1,
      sprintf("mean %.4f", mean(ir$weight)))
check("sum of weights near the row count",
      abs(sum(ir$weight) - nrow(ir)) / nrow(ir) < 0.05,
      sprintf("%.0f vs %d", sum(ir$weight), nrow(ir)))

# Feeding back an already-scaled file must be refused, not divided again.
pre <- haven::read_dta("fixtures/XXIR7AFL.DTA")
pre$v005 <- pre$v005 / 1e6
tmp <- file.path("fixtures", "_prescaled.dta")
haven::write_dta(pre, tmp)
check("pre-scaled weights are refused",
      inherits(try(read_recode(tmp, c("v012"), recode = "IR", quiet = TRUE),
                   silent = TRUE), "try-error"))
unlink(tmp)

cat("design\n")
check("psu attached", "psu" %in% names(ir))
check("strata attached", "strata" %in% names(ir))
mr <- read_recode("fixtures/XXMR7AFL.DTA", c("mv012"), quiet = TRUE)
check("men's recode weights on mv005", abs(mean(mr$weight) - 1) < 0.1,
      sprintf("mean %.4f", mean(mr$weight)))
hr <- read_recode("fixtures/XXHR7AFL.DTA", c("hv270"), quiet = TRUE)
check("household recode weights on hv005", abs(mean(hr$weight) - 1) < 0.1,
      sprintf("mean %.4f", mean(hr$weight)))

cat("scale factors from variables.csv\n")
ir2 <- read_recode("fixtures/XXIR7AFL.DTA", c("v437", "v438", "v191"), quiet = TRUE)
check("woman's weight in kg not decikg", mean(ir2$v437) > 30 && mean(ir2$v437) < 90,
      sprintf("mean %.1f", mean(ir2$v437)))
check("woman's height in cm", mean(ir2$v438) > 140 && mean(ir2$v438) < 165,
      sprintf("mean %.1f", mean(ir2$v438)))
check("wealth score divided by 100,000", abs(mean(ir2$v191)) < 5,
      sprintf("mean %.3f", mean(ir2$v191)))
check("v005 not double-scaled by the scale table", abs(mean(ir2$weight) - 1) < 0.1)

cat("anthropometry\n")
kr_raw <- read_recode("fixtures/XXKR7AFL.DTA",
                      c("hw70", "hw71", "hw72", "hw73", "b5"), quiet = TRUE)
kr <- clean_anthropometry(kr_raw, "KR", quiet = TRUE)
check("haz created", "haz" %in% names(kr))
check("flags at 9990 and above dropped", max(kr$haz, na.rm = TRUE) < 6.001,
      sprintf("max %.2f", max(kr$haz, na.rm = TRUE)))
check("haz within WHO bounds", all(kr$haz >= -6 & kr$haz <= 6, na.rm = TRUE))
check("haz is a plausible z-score",
      mean(kr$haz, na.rm = TRUE) > -3 && mean(kr$haz, na.rm = TRUE) < 0,
      sprintf("mean %.3f", mean(kr$haz, na.rm = TRUE)))
check("some rows dropped as flagged", sum(is.na(kr$haz)) > 0,
      sprintf("%d missing", sum(is.na(kr$haz))))
pr_attempt <- clean_anthropometry(kr_raw, "PR", quiet = TRUE)
check("PR prefix does not pick up hw70", !("haz" %in% names(pr_attempt)))

cat("century month codes\n")
ym <- cmc_to_year_month(1441)
check("CMC 1441 is January 2020", ym$year == 2020 && ym$month == 1,
      sprintf("%d-%d", ym$year, ym$month))
ym <- cmc_to_year_month(1452)
check("CMC 1452 is December 2020", ym$year == 2020 && ym$month == 12,
      sprintf("%d-%d", ym$year, ym$month))
check("round trip", year_month_to_cmc(2020, 1) == 1441)

cat("missing variables are reported, not hidden\n")
got <- read_recode("fixtures/XXIR7AFL.DTA", c("v012", "sdist", "v456"), quiet = TRUE)
check("absent variables simply do not appear", !("sdist" %in% names(got)))
check("present variables still load", "v012" %in% names(got))

cat("survey design object\n")
des <- dhs_design(ir)
check("svydesign built", inherits(des, "survey.design"))
m <- survey::svymean(~v012, des)
check("a weighted mean comes back finite", is.finite(coef(m)[[1]]),
      sprintf("%.3f", coef(m)[[1]]))
check("its standard error is positive", survey::SE(m)[[1]] > 0)

cat("\n")
if (length(failures)) {
  cat(sprintf("FAIL: %d check(s) failed: %s\n", length(failures),
              paste(failures, collapse = ", ")))
  quit(status = 1)
}
cat("PASS\n")
