import pandas as pd

file_name = 'nba_players.csv'
df = pd.read_csv(file_name)

# Fix column headers
df = df.rename(columns={
    '3:00 PM': '3PM',
    '#ERROR!': 'PLUS_MINUS'
})

# Save to new cleaned file
df.to_csv('nba_stats_cleaned.csv', index=False)
print("File nba_stats_cleaned.csv created successfully!")