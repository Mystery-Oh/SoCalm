import pandas as pd



# CSV 파일 불러오기. 공공데이터, 관공서는 cp949로 인코딩 경우가 많음
df = pd.read_csv('accident/19_23_truck.csv', encoding='cp949')

# '시군구코드' 열에서, 충북 청주ooN 이 포함된 행 필터링
filtered_df = df[df['시도시군구명'].str.match(r'^충북\s청주', na=False)]

# 결과 저장
filtered_df.to_csv('accident_cheongju/truck.csv', index=False, encoding='utf-8-sig')  # CSV 저장
filtered_df.to_json('accident_cheongju/truck.json', orient='records', force_ascii=False)  # JSON 저장