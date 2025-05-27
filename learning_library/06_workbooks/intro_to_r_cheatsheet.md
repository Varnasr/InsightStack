# intro_to_r_cheatsheet.md

A practical starter guide based on *An Introduction to R* by Mark Gardener.

---

## ✅ Load R and Get Help
```r
# Start R and use help
help.start()
?mean
```

## 📊 Create a Simple Dataset
```r
heights <- c(150, 160, 170, 165, 180)
weights <- c(55, 60, 72, 68, 80)
```

## 📉 Plot It
```r
plot(heights, weights, main="Height vs Weight", xlab="Height (cm)", ylab="Weight (kg)")
```

## 📚 Run a Linear Model
```r
lm_result <- lm(weights ~ heights)
summary(lm_result)
```
