import pandas as pd
from sqlalchemy import create_engine

# --- CONFIGURATION ---
# Ask for database password securely
db_password = input("Enter MySQL Password: ").strip()

def clean_and_export():
    print("Starting data cleaning process...")

    # 1. Load Data with tolerant encoding
    # 'latin-1' helps read files with special characters without crashing
    file_path = 'spotify_2024.csv' 
    
    try:
        df = pd.read_csv(file_path, encoding='latin-1')
        print(f"File loaded: {len(df)} rows.")
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    # 2. Text Cleaning Function
    print("Cleaning text columns...")

    def clean_text(text):
        if isinstance(text, str):
            # Remove specific garbage characters found in the raw file
            text = text.replace('ý', '')
            text = text.replace('ï»¿', '') # Excel artifact
            # Fix encoding errors
            text = text.replace('Ã', 'A').replace('©', 'e') 
            return text.strip()
        return text

    # Apply cleaning to all text columns (Artist, Track Name, etc.)
    text_columns = df.select_dtypes(include=['object']).columns
    for col in text_columns:
        df[col] = df[col].apply(clean_text)

    # 3. Numeric Cleaning (Remove commas)
    # Convert "1,000,000" (string) to 1000000 (number)
    num_columns = ['spotify_streams', 'youtube_views', 'tiktok_posts', 'tiktok_likes']
    for col in num_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '').str.replace(' ', '')
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 4. Export to MySQL Database
    try:
        # Connection string with UTF-8 support
        connection_str = f"mysql+mysqlconnector://root:{db_password}@localhost:3306/spotify_project?charset=utf8mb4"
        engine = create_engine(connection_str)
        
        print("Sending data to MySQL...")
        df.to_sql('top_songs_2024', con=engine, if_exists='replace', index=False)
        print("SUCCESS! Data is clean and stored in the database.")
        
    except Exception as e:
        print(f"MySQL Error: {e}")

if __name__ == "__main__":
    clean_and_export()
