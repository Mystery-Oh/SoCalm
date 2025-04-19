import pandas as pd

# CSV 파일 불러오기
df = pd.read_csv('accident/충청북도_사고다발지역 데이터_20211130.csv', encoding='utf-8')

# '시군구명' 열에서,  '청주'와 '구'가 포함된 행 필터링
filtered_df = df[df['시구군명'].str.contains('청주.*구', na=False)]

# 결과 저장
filtered_df.to_csv('accident_cheongju/cheongjuAccident.csv', index=False, encoding='utf-8-sig')  # CSV 저장
filtered_df.to_json('accident_cheongju/cheongjuAccident.json', orient='records', force_ascii=False)  # JSON 저장