# Jekyll Journal R Project Settings
options(
  repos = c(CRAN = "https://cloud.r-project.org/"),
  stringsAsFactors = FALSE,
  scipen = 999,  # Avoid scientific notation
  digits = 3
)

# Set default ggplot2 theme
if (requireNamespace("ggplot2", quietly = TRUE)) {
  ggplot2::theme_set(ggplot2::theme_minimal())
}

# Welcome message
cat("Jekyll Journal R Environment Loaded\n")
cat("Available scripts in scripts/ directory\n")
cat("Use source(\"scripts/data_analysis.R\") to load analysis functions\n")

