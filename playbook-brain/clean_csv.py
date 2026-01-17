import pandas as pd

file_name = 'nba_players.csv'
df = pd.read_csv(file_name)

# תיקון הכותרות
df = df.rename(columns={
    '3:00 PM': '3PM',
    '#ERROR!': 'PLUS_MINUS'
})

# שמירה לקובץ חדש ונקי
df.to_csv('nba_stats_cleaned.csv', index=False)
print("הקובץ nba_stats_cleaned.csv נוצר בהצלחה!")