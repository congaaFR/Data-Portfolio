# Install library (if needed)
# !pip install riotwatcher

from riotwatcher import LolWatcher, ApiError
import pandas as pd
import requests
import urllib.parse
import time

# --- Settings ---
# Enter your keys and name here
api_key = input("Your API Key: ").strip()
region_account = 'europe'
region_game = 'euw1'
player_name = input("Your Game Name: ").strip()
player_tag = input("Your Tag: ").strip()

# How many games to get
target_games_count = 700

watcher = LolWatcher(api_key)

try:
    print(f"Looking for account: {player_name}#{player_tag}...")

    # Fix name for URL
    name_encoded = urllib.parse.quote(player_name)
    tag_encoded = urllib.parse.quote(player_tag)
    url_account = f"https://{region_account}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name_encoded}/{tag_encoded}"

    response = requests.get(url_account, headers={"X-Riot-Token": api_key})

    if response.status_code == 200:
        user_data = response.json()
        user_puuid = user_data['puuid']
        print("Account found.")

        # --- Step 1: Get Match IDs ---
        print("Getting match list...")
        all_match_ids = []
        start_index = 0

        while len(all_match_ids) < target_games_count:
            # Get 100 matches at a time
            new_matches = watcher.match.matchlist_by_puuid(region_game, user_puuid, start=start_index, count=100)

            if not new_matches:
                break

            all_match_ids.extend(new_matches)
            start_index += 100
            print(f" -> Found {len(all_match_ids)} matches")
            time.sleep(1) # Small pause

        print(f"Total: {len(all_match_ids)} matches found.")

        # --- Step 2: Get Details ---
        print("Getting details for each match...")

        match_data_list = []

        for i, match_id in enumerate(all_match_ids):
            try:
                # Safety pause
                time.sleep(1.2)

                match_detail = watcher.match.by_id(region_game, match_id)

                # Get player stats
                participants = match_detail['info']['participants']
                player_stats = next(p for p in participants if p['puuid'] == user_puuid)

                game_creation = match_detail['info']['gameCreation']
                game_date = pd.to_datetime(game_creation, unit='ms')

                # Save info
                match_info = {
                    'MatchID': match_id,
                    'Date': game_date,
                    'Champion': player_stats['championName'],
                    'Kills': player_stats['kills'],
                    'Deaths': player_stats['deaths'],
                    'Assists': player_stats['assists'],
                    'Win': player_stats['win'],
                    'Damage': player_stats['totalDamageDealtToChampions'],
                    'Gold': player_stats['goldEarned'],
                    'CS': player_stats['totalMinionsKilled'] + player_stats['neutralMinionsKilled'],
                    'Role': player_stats['teamPosition'],
                    'Mode': match_detail['info']['gameMode'],
                    'Duration_Min': round(match_detail['info']['gameDuration'] / 60, 2)
                }
                match_data_list.append(match_info)

                # Show progress
                if (i+1) % 50 == 0:
                    print(f"Progress: {i+1}/{len(all_match_ids)} matches done.")

            except ApiError as err:
                if err.response.status_code == 429:
                    print("Too many requests. Waiting 10 seconds...")
                    time.sleep(10)
                else:
                    print(f"Error on match {match_id}: {err}")
            except Exception as e:
                continue

        # --- Step 3: Save File ---
        df = pd.DataFrame(match_data_list)
        
        # Calculate KDA
        df['KDA'] = round((df['Kills'] + df['Assists']) / df['Deaths'].replace(0, 1), 2)

        print("Finished.")
        
        filename = 'lol_match_history.csv'
        df.to_csv(filename, index=False)
        print(f"File saved: {filename}")

    else:
        print(f"Error: API Key or Name is wrong (Code {response.status_code})")

except Exception as e:
    print(f"Critical Error: {e}")
