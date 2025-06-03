import sqlite3
import pandas as pd

# '데이터이름.csv'
df = pd.read_csv('datas.csv', encoding='utf-8')

# '데이터베이스이름.db'
conn = sqlite3.connect('accidents.db')

# '열이름'
df.to_sql('accidents', conn, if_exists='replace', index=False)
c = conn.cursor()
c.execute("SELECT * FROM accidents")

# 결과 출력
rows = c.fetchall()  # 모든 행을 가져옵니다.
for row in rows:
    print(row)

conn.close