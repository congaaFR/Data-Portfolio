# Spotify ETL Data Pipeline

## Project Overview
A robust ETL (Extract, Transform, Load) pipeline designed to handle messy real-world music data. 
The goal was to clean a raw dataset containing encoding errors, special characters, and inconsistencies before analysis.

## Tech Stack
* Python (Pandas): Data cleaning, String manipulation, Date formatting.
* ETL Process:
    * Extract: Load raw CSV data.
    * Transform: Fix text encoding (UTF-8), handle missing values, standardize artist names.
    * Load: Export clean data to MySQL / Clean CSV.

## Key Insights
* Top Artist: Taylor Swift dominates total streams, outperforming viral TikTok trends.
* Genre Trends: "Pop" remains the most consistent genre for daily streams compared to "Hip-Hop" (high variance).
* Seasonality: A spike in acoustic tracks is observed during winter months.

## File Structure
* `etl_pipeline.py`: Main script for cleaning data.
* `raw_data.csv`: Original messy dataset.
* `clean_data.csv`: Final processed output.
