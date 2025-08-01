# Basic R Environment Setup for Jekyll Journal
# Installs only essential packages for immediate use

cat("Setting up basic R environment for Jekyll Journal...\n")

# Essential packages only
essential_packages <- c(
  "ggplot2",
  "dplyr", 
  "readr",
  "knitr",
  "rmarkdown"
)

# Install essential packages
cat("Installing essential packages:", paste(essential_packages, collapse = ", "), "\n")
install.packages(essential_packages, dependencies = TRUE, repos = "https://cloud.r-project.org/")

# Test loading
cat("\nTesting package installation...\n")
for (pkg in essential_packages) {
  tryCatch({
    library(pkg, character.only = TRUE)
    cat("✓", pkg, "loaded successfully\n")
  }, error = function(e) {
    cat("✗", pkg, "failed to load:", e$message, "\n")
  })
}

cat("\nBasic R environment setup complete!\n")
cat("You can now use R for basic data analysis and R Markdown.\n")