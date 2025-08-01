# Academic Journal Data Analysis Toolkit
# R script for data processing and visualization for journal submissions

# Load required libraries
library(ggplot2)
library(dplyr)
library(readr)
library(knitr)
library(rmarkdown)
library(tidyr)
library(plotly)

# Function to generate citation statistics
generate_citation_stats <- function(data) {
  citation_summary <- data %>%
    summarise(
      total_articles = n(),
      avg_citations = mean(citations, na.rm = TRUE),
      median_citations = median(citations, na.rm = TRUE),
      max_citations = max(citations, na.rm = TRUE)
    )
  
  return(citation_summary)
}

# Function to create publication timeline visualization
create_publication_timeline <- function(data) {
  timeline_plot <- ggplot(data, aes(x = publication_date, y = citations)) +
    geom_point(alpha = 0.7, size = 3) +
    geom_smooth(method = "loess", se = FALSE, color = "#1f77b4") +
    labs(
      title = "Publication Timeline and Citation Impact",
      x = "Publication Date",
      y = "Citations",
      caption = "Academic Journal Analytics"
    ) +
    theme_minimal() +
    theme(
      plot.title = element_text(size = 16, face = "bold"),
      axis.text = element_text(size = 12),
      axis.title = element_text(size = 14)
    )
  
  return(timeline_plot)
}

# Function to analyze author collaboration networks
analyze_author_networks <- function(data) {
  author_stats <- data %>%
    group_by(author) %>%
    summarise(
      publications = n(),
      total_citations = sum(citations, na.rm = TRUE),
      avg_citations_per_paper = mean(citations, na.rm = TRUE)
    ) %>%
    arrange(desc(total_citations))
  
  return(author_stats)
}

# Function to generate subject area distribution
create_subject_distribution <- function(data) {
  subject_plot <- data %>%
    count(subject_area) %>%
    ggplot(aes(x = reorder(subject_area, n), y = n)) +
    geom_col(fill = "#2ca02c", alpha = 0.8) +
    coord_flip() +
    labs(
      title = "Distribution of Articles by Subject Area",
      x = "Subject Area",
      y = "Number of Articles"
    ) +
    theme_minimal()
  
  return(subject_plot)
}

# Function to export data for Jekyll integration
export_for_jekyll <- function(data, filename) {
  # Convert data to YAML format for Jekyll
  yaml_content <- paste0("---\n",
                        "title: \"Data Analysis Results\"\n",
                        "layout: page\n",
                        "generated_date: \"", Sys.Date(), "\"\n",
                        "---\n\n")
  
  # Add data summary
  summary_text <- paste0("## Data Summary\n\n",
                        "Total articles analyzed: ", nrow(data), "\n",
                        "Date range: ", min(data$publication_date, na.rm = TRUE), 
                        " to ", max(data$publication_date, na.rm = TRUE), "\n\n")
  
  # Write to file
  writeLines(paste0(yaml_content, summary_text), filename)
  
  cat("Data exported to:", filename, "\n")
}

# Sample data generation function for testing
generate_sample_data <- function(n = 100) {
  set.seed(42)
  
  sample_data <- data.frame(
    article_id = 1:n,
    title = paste("Article", 1:n),
    author = sample(c("Smith, J.", "Johnson, M.", "Williams, K.", "Brown, L.", "Davis, R."), n, replace = TRUE),
    publication_date = sample(seq(as.Date("2020-01-01"), as.Date("2023-12-31"), by = "day"), n),
    citations = rpois(n, lambda = 15),
    subject_area = sample(c("Literature", "Digital Humanities", "Media Studies", "Cultural Studies", "Technology"), n, replace = TRUE),
    doi = paste0("10.1234/journal.", 1:n)
  )
  
  return(sample_data)
}

# Main analysis function
run_journal_analysis <- function(output_dir = "_data/analysis/") {
  # Create output directory if it doesn't exist
  if (!dir.exists(output_dir)) {
    dir.create(output_dir, recursive = TRUE)
  }
  
  # Generate sample data (replace with actual data loading)
  data <- generate_sample_data()
  
  # Run analyses
  cat("Running journal analytics...\n")
  
  # Citation statistics
  citation_stats <- generate_citation_stats(data)
  write_csv(citation_stats, paste0(output_dir, "citation_stats.csv"))
  
  # Author network analysis
  author_networks <- analyze_author_networks(data)
  write_csv(author_networks, paste0(output_dir, "author_stats.csv"))
  
  # Create visualizations
  timeline_plot <- create_publication_timeline(data)
  ggsave(paste0(output_dir, "publication_timeline.png"), timeline_plot, width = 10, height = 6, dpi = 300)
  
  subject_plot <- create_subject_distribution(data)
  ggsave(paste0(output_dir, "subject_distribution.png"), subject_plot, width = 8, height = 6, dpi = 300)
  
  # Export for Jekyll
  export_for_jekyll(data, paste0(output_dir, "analysis_summary.md"))
  
  cat("Analysis complete! Results saved to:", output_dir, "\n")
  
  return(list(
    data = data,
    citation_stats = citation_stats,
    author_networks = author_networks
  ))
}

# Run analysis if script is executed directly
if (!interactive()) {
  run_journal_analysis()
}