#!/usr/bin/env Rscript
# Quick runner for journal analytics

# Source the main analysis script
source("scripts/data_analysis.R")

# Run analysis with default settings
results <- run_journal_analysis()

cat("Analysis complete!\n")
cat("Check _data/analysis/ for results\n")

