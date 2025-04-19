import pandas as pd

# CSV 파일 불러오기. 공공데이터, 관공서는 cp949로 인코딩 경우가 많음
df = pd.read_csv('accident/링크기반사고정보.csv', encoding='cp949')

# '시군구코드' 열에서, 청주시코드 43111~43114만 필터링
filtered_df = df[(df['시군구코드']>=43111) & (df['시군구코드']<=43114)]

# 결과 저장
filtered_df.to_csv('accident_cheongju/cheongjuAccident3.csv', index=False, encoding='utf-8-sig')  # CSV 저장
filtered_df.to_json('accident_cheongju/cheongjuAccident3.json', orient='records', force_ascii=False)  # JSON 저장