/* PLAYER PERFORMANCE ANALYSIS - LEAGUE OF LEGENDS
 Data Source: Riot API (via Python Script)
 Format: CSV file imported into 'match_history' table
*/

-- 1. Average Performance by Champion (KDA & Damage)
SELECT 
    Champion,
    COUNT(*) as Games_Played,
    ROUND(AVG(Kills), 1) as Avg_Kills,
    ROUND(AVG(Deaths), 1) as Avg_Deaths,
    ROUND(AVG(Assists), 1) as Avg_Assists,
    ROUND(AVG(Damage), 0) as Avg_Damage,
    ROUND((SUM(CASE WHEN Win = 'True' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) as Win_Rate_Pct
FROM match_history
GROUP BY Champion
HAVING COUNT(*) > 5 -- Only keep champions played more than 5 times
ORDER BY Win_Rate_Pct DESC;

-- 2. Impact of Game Duration on Result
SELECT 
    CASE 
        WHEN Duration_Min < 25 THEN 'Early Game (<25m)'
        WHEN Duration_Min BETWEEN 25 AND 35 THEN 'Mid Game (25-35m)'
        ELSE 'Late Game (>35m)'
    END as Game_Length,
    COUNT(*) as Total_Games,
    ROUND((SUM(CASE WHEN Win = 'True' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) as Win_Rate
FROM match_history
GROUP BY 
    CASE 
        WHEN Duration_Min < 25 THEN 'Early Game (<25m)'
        WHEN Duration_Min BETWEEN 25 AND 35 THEN 'Mid Game (25-35m)'
        ELSE 'Late Game (>35m)'
    END
ORDER BY Total_Games DESC;

-- 3. Gold Earned vs Victory Analysis
SELECT 
    Win,
    ROUND(AVG(Gold), 0) as Avg_Gold_Earned,
    ROUND(AVG(CS), 0) as Avg_Minions_Killed
FROM match_history
GROUP BY Win;

-- 4. "Fatigue" Analysis: Do I play better at the start of the day?
-- We rank games (1st, 2nd, 3rd...) played on the same day to see the Win Rate trend.
SELECT 
    Game_Number_In_Day,
    COUNT(*) as Total_Times_Reached,
    ROUND((SUM(CASE WHEN Win = 'True' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) as Win_Rate_Pct
FROM (
    SELECT 
        Win,
        -- This function ranks games by time for each date (1, 2, 3...)
        ROW_NUMBER() OVER (PARTITION BY DATE(Date) ORDER BY Date ASC) as Game_Number_In_Day
    FROM match_history
) as Daily_Ranking
WHERE Game_Number_In_Day <= 10 
GROUP BY Game_Number_In_Day
ORDER BY Game_Number_In_Day;
