/* SPOTIFY 2024 DATA ANALYSIS
   Source: Cleaned CSV via Python Script
   Table: top_songs_2024
*/

-- 1. Top 10 Most Streamed Songs on Spotify
SELECT 
    track_name, 
    artist_name, 
    spotify_streams
FROM top_songs_2024
ORDER BY spotify_streams DESC
LIMIT 10;

-- 2. TikTok vs Spotify: Which songs are viral on TikTok but not Spotify?
-- We look for songs with High TikTok Posts but lower Spotify ranking
SELECT 
    track_name,
    tiktok_posts,
    spotify_streams
FROM top_songs_2024
ORDER BY tiktok_posts DESC
LIMIT 10;

-- 3. Artist Popularity: Total Views across platforms
SELECT 
    artist_name,
    COUNT(track_name) as Total_Tracks,
    SUM(spotify_streams) as Total_Spotify_Streams,
    SUM(youtube_views) as Total_Youtube_Views
FROM top_songs_2024
GROUP BY artist_name
HAVING Total_Tracks > 2 -- Only artists with more than 2 hits
ORDER BY Total_Spotify_Streams DESC;

-- 4. Who is the "King/Queen" of Spotify? (Total Streams per Artist)
SELECT 
    artist_name,
    SUM(spotify_streams) as Total_Spotify_Streams
FROM top_songs_2024
GROUP BY artist_name
ORDER BY Total_Spotify_Streams DESC
LIMIT 1;
