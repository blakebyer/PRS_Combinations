library(xlsx)

## Load data
excel_path <- "UniversityofKentucky/MillerLab/PRSKB/Means_Sorted.xlsx"

# Create vectors
dx <- read.xlsx(excel_path, sheetName = "Sheet1", colIndex = 2)
ar <- read.xlsx(excel_path, sheetName = "Sheet1", colIndex = 29, startRow = 2)
geo <- read.xlsx(excel_path, sheetName = "Sheet1", colIndex = 30, startRow = 2)
har <- read.xlsx(excel_path, sheetName = "Sheet1", colIndex = 31, startRow =2)

# Create DataFrame
df <- data.frame(dx, ar, geo, har)
colnames(df) <- c('DX','AR','GEO','HAR') 

# Megagraphs
plot(density(df$AR), main = "Arithmetic Mean", xlab = "PRS", col = 'black', lwd = 2)

plot(density(df$GEO), main = "Geometric Mean", xlab = "PRS", col = 'black', lwd = 2)

plot(density(df$HAR), main = "Harmonic Mean", xlab = "PRS", col = 'black', lwd = 2)

## Chi-squared

# Count of case conditions in entire population. CN is cognitively normal, CI is cognitively impaired.
cn_count <- length(which(dx == "CN"))
ci_count <- length(which(dx == "MCI")) + length(which(dx == "Dementia"))

chi_sq_calc <- function(meantype, percentile) {
  #Expected case counts
  expected_cn <- (cn_count / 808) * ((1 - percentile) * 808)
  expected_ci <- (ci_count / 808) * ((1 - percentile) * 808)
  
  #Rows with PRS above or equal to percentile
  sorted_rows <- quantile(df[[meantype]], percentile)
  cases <- which(df[[meantype]] >= sorted_rows)
  
  #Observed cases 
  observed_cn <- sum(dx[cases,] == "CN")
  observed_ci <- sum(dx[cases,] %in% c("MCI", "Dementia"))
  
  #Convert to vectors
  expected <- c(expected_cn, expected_ci)
  observed <- c(observed_cn, observed_ci)
  
  #Make contingency table
  contingency_tbl <- data.frame(Expected = expected, Observed = observed)
  print(contingency_tbl)
  
  #Calculate chi-squared and print to screen
  result <- chisq.test(contingency_tbl)
  print(result)
}

## Example Usage
chi_sq_calc("GEO", 0.8)
chi_sq_calc("GEO",0.9)
