# R Integration for Jekyll Journal

This document explains how to use R for data analysis and visualization within the Jekyll journal publishing system.

## Overview

The R integration provides:

- **Data analysis capabilities** for journal articles
- **R Markdown templates** for reproducible research articles
- **Automated analytics** for journal metrics and citations
- **Interactive visualizations** embedded in web articles
- **Seamless Jekyll integration** for web publishing

## Quick Start

### 1. Install R and Setup Environment

```r
# Run the setup script
source("setup_r_environment.R")
```

This will:
- Install all required R packages
- Create necessary directories
- Set up project configuration
- Create helper scripts

### 2. Create Data-Driven Articles

Use the R Markdown template:

```r
# Copy the template
file.copy("templates/article_template.Rmd", "my_article.Rmd")

# Edit your article in my_article.Rmd
# Then render it
rmarkdown::render("my_article.Rmd")
```

### 3. Run Journal Analytics

```r
# Source analysis functions
source("scripts/data_analysis.R")

# Run complete analysis
results <- run_journal_analysis()
```

## File Structure

```
├── scripts/
│   └── data_analysis.R          # Main R analysis functions
├── templates/
│   └── article_template.Rmd     # R Markdown article template
├── data/                        # Raw data files
├── _data/analysis/              # Generated analysis outputs
├── figures/                     # Generated visualizations
├── reports/                     # Rendered reports
├── setup_r_environment.R       # Environment setup script
├── run_analysis.R              # Quick analysis runner
├── .Rprofile                   # R project settings
└── R_PACKAGES.md               # Package documentation
```

## R Markdown to Jekyll Workflow

### Step 1: Write R Markdown Article

Create your article using the template in `templates/article_template.Rmd`:

```yaml
---
title: "Your Article Title"
author: 
  - name: "Your Name"
    affiliation: "Your Institution"
jekyll_front_matter:
  layout: page
  category: "research"
  type: "issue01"
  DOI: "10.xxxx/xxx"
---
```

### Step 2: Include Jekyll Front Matter

The template automatically includes Jekyll-compatible YAML front matter:

- `layout`: Jekyll layout to use
- `category`: Article section
- `type`: Issue identifier
- `DOI`: Digital Object Identifier
- `bio`: Author references
- `media`: Associated media files

### Step 3: Render to Markdown

```r
rmarkdown::render("your_article.Rmd", 
                  output_format = "md_document",
                  output_options = list(preserve_yaml = TRUE))
```

### Step 4: Move to Jekyll Collection

```bash
# Move rendered markdown to Jekyll collection
mv your_article.md _issue01/section1/

# Copy generated figures to media server
cp your_article_files/figure-markdown_strict/* /path/to/media/server/
```

## Analysis Functions

### Citation Analysis

```r
# Load analysis functions
source("scripts/data_analysis.R")

# Generate citation statistics
citation_stats <- generate_citation_stats(your_data)

# Create publication timeline
timeline_plot <- create_publication_timeline(your_data)

# Analyze author networks
author_networks <- analyze_author_networks(your_data)
```

### Journal Metrics

```r
# Run complete analytics suite
results <- run_journal_analysis(output_dir = "_data/analysis/")

# Access results
citation_data <- results$citation_stats
author_data <- results$author_networks
```

### Custom Analysis

Create your own analysis functions:

```r
# Custom function template
my_analysis <- function(data) {
  # Your analysis code here
  result <- data %>%
    group_by(category) %>%
    summarise(metric = mean(value))
  
  return(result)
}
```

## Interactive Visualizations

### Plotly Integration

```r
library(plotly)

# Create interactive plot
p <- ggplot(data, aes(x = year, y = citations)) +
  geom_point() +
  theme_minimal()

# Convert to interactive
ggplotly(p)
```

### Data Tables

```r
library(DT)

# Create interactive table
datatable(your_data, 
          options = list(pageLength = 10, scrollX = TRUE),
          filter = 'top')
```

## Publishing Workflow

### For Journal Editors

1. **Set up R environment**: Run `setup_r_environment.R`
2. **Collect submission data**: Store in `data/` directory
3. **Run analytics**: Use `run_analysis.R` for regular metrics
4. **Generate reports**: Create R Markdown reports for editorial review

### For Authors

1. **Use R Markdown template**: Copy `templates/article_template.Rmd`
2. **Include your analysis**: Add data analysis and visualizations
3. **Render to markdown**: Use `rmarkdown::render()`
4. **Submit for review**: Include both `.Rmd` and generated files

### For Reviewers

1. **Reproducible review**: Execute the R code to verify results
2. **Check methodology**: Review analysis code in R chunks
3. **Validate outputs**: Ensure plots and tables are accurate

## Advanced Features

### Citation Network Analysis

```r
library(igraph)

# Create citation network
citation_network <- create_citation_network(citation_data)

# Visualize network
plot(citation_network, 
     vertex.size = 5,
     edge.arrow.size = 0.5,
     layout = layout_with_fr)
```

### Text Analysis

```r
library(tidytext)

# Analyze article text
article_text %>%
  unnest_tokens(word, text) %>%
  anti_join(stop_words) %>%
  count(word, sort = TRUE)
```

### Academic APIs

```r
library(scholar)
library(rcrossref)

# Get author metrics from Google Scholar
author_profile <- get_profile("scholar_id")

# Get article metadata from Crossref
article_metadata <- cr_works(dois = "10.xxxx/xxxx")
```

## Configuration

### Jekyll Configuration

Add to `_config.yml`:

```yaml
# Enable R-generated content
include: 
  - "_data/analysis"
  - "figures"

# Collections for R Markdown articles
collections:
  research:
    output: true
    permalink: /:collection/:name/
```

### R Project Settings

The `.Rprofile` file includes:

```r
# Default options
options(
  repos = c(CRAN = "https://cloud.r-project.org/"),
  stringsAsFactors = FALSE,
  scipen = 999
)

# Default ggplot2 theme
ggplot2::theme_set(ggplot2::theme_minimal())
```

## Best Practices

### Code Organization

- **Modular functions**: Create reusable functions in `scripts/`
- **Clear documentation**: Comment your R code thoroughly
- **Version control**: Track both `.Rmd` and `.md` files
- **Reproducible analysis**: Use `set.seed()` for random operations

### Performance

- **Cache results**: Use `cache=TRUE` in R Markdown chunks
- **Optimize plots**: Use appropriate figure sizes and DPI
- **Efficient data loading**: Use `readr` for fast CSV reading
- **Memory management**: Remove large objects when done

### Publishing

- **Test locally**: Render and preview before submission
- **Check dependencies**: Ensure all packages are documented
- **Validate outputs**: Check that plots and tables render correctly
- **Follow journal style**: Use consistent formatting and citations

## Troubleshooting

### Common Issues

**Package installation fails**:
```r
# Try installing from source
install.packages("package_name", type = "source")
```

**R Markdown won't render**:
```r
# Check for missing packages
rmarkdown::pandoc_version()  # Ensure Pandoc is installed
```

**Jekyll integration problems**:
- Check YAML front matter syntax
- Verify file paths in `_config.yml`
- Ensure proper file permissions

### Getting Help

1. Check R package documentation: `?function_name`
2. Review R Markdown guide: `vignette("rmarkdown")`
3. Jekyll documentation: https://jekyllrb.com/docs/
4. R community: https://community.rstudio.com/

## Examples

See the `templates/` directory for complete examples of:

- Data analysis articles
- Interactive visualizations
- Statistical reporting
- Citation analysis

## Contributing

To add new R functionality:

1. Create functions in `scripts/`
2. Add to package requirements in `setup_r_environment.R`
3. Update documentation in this README
4. Test with sample data

---

*This R integration enables modern, reproducible, data-driven academic publishing within the Jekyll journal framework.*