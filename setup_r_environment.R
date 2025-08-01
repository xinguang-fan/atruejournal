# R Environment Setup for Jekyll Journal
# This script installs all required R packages and sets up the environment

cat("Setting up R environment for Jekyll Journal...\n")

# Check R version
cat("R Version:", R.version.string, "\n")

# Required packages
required_packages <- c(
  # Core data manipulation and analysis
  "dplyr",
  "tidyr", 
  "readr",
  "tibble",
  "stringr",
  "lubridate",
  
  # Visualization
  "ggplot2",
  "plotly",
  "viridis",
  "RColorBrewer",
  "gridExtra",
  
  # R Markdown and publishing
  "rmarkdown",
  "knitr",
  "bookdown",
  "blogdown",
  
  # Interactive elements
  "DT",
  "htmlwidgets",
  "crosstalk",
  
  # Statistical analysis
  "broom",
  "modelr",
  "infer",
  "corrplot",
  
  # Network analysis (for citation networks)
  "igraph",
  "networkD3",
  "visNetwork",
  
  # Text analysis (for journal content analysis)
  "tidytext",
  "wordcloud",
  "tm",
  "topicmodels",
  
  # Academic publishing tools
  "scholar",  # For Google Scholar data
  "rcrossref", # For Crossref API
  "roadoi",   # For open access data
  
  # Data import/export
  "readxl",
  "writexl",
  "jsonlite",
  "yaml",
  
  # Development tools
  "devtools",
  "usethis"
)

# Function to install missing packages
install_if_missing <- function(package_list) {
  installed_packages <- rownames(installed.packages())
  missing_packages <- setdiff(package_list, installed_packages)
  
  if (length(missing_packages) > 0) {
    cat("Installing missing packages:", paste(missing_packages, collapse = ", "), "\n")
    install.packages(missing_packages, dependencies = TRUE)
  } else {
    cat("All required packages are already installed.\n")
  }
}

# Install packages
install_if_missing(required_packages)

# Load core packages to verify installation
cat("\nVerifying package installation...\n")
core_packages <- c("dplyr", "ggplot2", "rmarkdown", "knitr")

for (pkg in core_packages) {
  tryCatch({
    library(pkg, character.only = TRUE)
    cat("✓", pkg, "loaded successfully\n")
  }, error = function(e) {
    cat("✗", pkg, "failed to load:", e$message, "\n")
  })
}

# Create project directory structure
cat("\nCreating directory structure...\n")

directories <- c(
  "scripts",
  "templates",
  "data",
  "_data/analysis",
  "figures",
  "reports"
)

for (dir in directories) {
  if (!dir.exists(dir)) {
    dir.create(dir, recursive = TRUE)
    cat("Created directory:", dir, "\n")
  } else {
    cat("Directory already exists:", dir, "\n")
  }
}

# Create .Rprofile for project-specific settings
rprofile_content <- '# Jekyll Journal R Project Settings
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
cat("Jekyll Journal R Environment Loaded\\n")
cat("Available scripts in scripts/ directory\\n")
cat("Use source(\\"scripts/data_analysis.R\\") to load analysis functions\\n")
'

writeLines(rprofile_content, ".Rprofile")
cat("Created .Rprofile with project settings\n")

# Create a sample analysis script runner
runner_script <- '#!/usr/bin/env Rscript
# Quick runner for journal analytics

# Source the main analysis script
source("scripts/data_analysis.R")

# Run analysis with default settings
results <- run_journal_analysis()

cat("Analysis complete!\\n")
cat("Check _data/analysis/ for results\\n")
'

writeLines(runner_script, "run_analysis.R")
cat("Created run_analysis.R script\n")

# Create package documentation
package_doc <- paste0("# R Packages for Jekyll Journal\n\n",
                     "This document lists all R packages used in the Jekyll Journal project.\n\n",
                     "## Installation\n\n",
                     "Run the setup script:\n",
                     "```r\n",
                     "source('setup_r_environment.R')\n",
                     "```\n\n",
                     "## Package List\n\n")

for (pkg in sort(required_packages)) {
  package_doc <- paste0(package_doc, "- **", pkg, "**: ")
  
  # Add brief description for key packages
  descriptions <- list(
    "dplyr" = "Data manipulation",
    "ggplot2" = "Data visualization",
    "rmarkdown" = "Dynamic documents",
    "knitr" = "Literate programming",
    "DT" = "Interactive tables",
    "plotly" = "Interactive plots",
    "scholar" = "Google Scholar data",
    "rcrossref" = "Crossref API access",
    "tidytext" = "Text analysis",
    "igraph" = "Network analysis"
  )
  
  if (pkg %in% names(descriptions)) {
    package_doc <- paste0(package_doc, descriptions[[pkg]])
  } else {
    package_doc <- paste0(package_doc, "Supporting package")
  }
  
  package_doc <- paste0(package_doc, "\n")
}

writeLines(package_doc, "R_PACKAGES.md")
cat("Created R_PACKAGES.md documentation\n")

cat("\n=== R Environment Setup Complete ===\n")
cat("Next steps:\n")
cat("1. Source the analysis script: source('scripts/data_analysis.R')\n")
cat("2. Run analysis: run_journal_analysis()\n")
cat("3. Use R Markdown templates in templates/ directory\n")
cat("4. Check _data/analysis/ for generated outputs\n")