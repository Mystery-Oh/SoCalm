import pandas as pd

# CSV 파일 불러오기. 공공데이터, 관공서는 cp949로 인코딩 경우가 많음
df = pd.read_csv('accident/지자체별_사고다발통계.csv', encoding='cp949')

# '시도시군구명' 열에서, '충청북도 청주시'가 포함된 행 필터링
filtered_df = df[df['시도시군구명'].str.contains(r'^충청북도 청주시', na=False)]

# 결과 저장
filtered_df.to_csv('accident_cheongju/cheongjuAccident2.csv', index=False, encoding='utf-8-sig')  # CSV 저장
filtered_df.to_json('accident_cheongju/cheongjuAccident2.json', orient='records', force_ascii=False)  # JSON 저장