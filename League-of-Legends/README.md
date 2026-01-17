# League of Legends Data Pipeline & Analysis

## Project Overview
This project analyzes my personal League of Legends match history to identify factors influencing my performance. 
I built an end-to-end data pipeline to extract my match data, process it, and store it for SQL analysis.

## Tech Stack
* Python: API Extraction (Riot Games API), Data Cleaning (Pandas).
* SQL: Data Storage & Querying (Key Performance Indicators).
* Analysis: Personal Win Rate calculation, Gold Efficiency, Early vs. Late game impact.

## Key Insights (Based on my Match History)
* Optimal Playing Time: My Win Rate is 15% higher during morning sessions compared to late-night games, highlighting the impact of focus.
* First Blood Impact: When I am involved in First Blood, my win probability increases to 60%.
* Snowballing Efficiency: When I secure a 2,000 gold lead at 15 minutes, I convert it into a victory 80% of the time.

## How to Run
1.  Clone the repo.
2.  Install dependencies: `pip install requests pandas`.
3.  Add your Riot API Key in `config.py`.
4.  Run `main.py` to fetch data.
