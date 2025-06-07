import sqlite3

# SQLite 데이터베이스에 연결
conn = sqlite3.connect('cheongju_accidents2.db')
c = conn.cursor()

# 데이터 조회
c.execute("SELECT * FROM accidents_cheongju")  # 테이블 이름

# 결과 출력
rows = c.fetchall()  # 모든 행을 가져옵니다.
for row in rows:
    print(row)  # 각 행을 출력합니다.

# 연결 종료
conn.close()