import requests
from datetime import datetime
import json

serviceKey = "A0HK/SOeu1VN3B3SYlqE+WE77Bqw9x7nZ2D96eM9PTZpRyKULaisgX8LMZLeTFxuFM0WpQCzlPc6OqOaB8OgPQ==" # 본인의 서비스 키 입력

now = datetime.now()

base_date = now.strftime("%Y%m%d")  # YYYYMMDD 형식
base_time = now.strftime("%H00")   # HH00 형식 (시간은 00분 기준)

#청주시 서원구 사창동의 좌표
nx = '68' # 예보 지점 x좌표
ny = '107' # 예보 지점 y좌표

input_d = datetime.strptime(base_date + base_time, "%Y%m%d%H%M" )
print(input_d)              #현재 시각 출력

# url
url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"
params = {
    "serviceKey": serviceKey,
    "numOfRows": "1000",
    "pageNo": "2",
    "dataType": "JSON",
    "base_date": base_date,
    "base_time": base_time,
    "totalCount": "10",
    "nx": nx,
    "ny": ny,
}

print(url)
response = requests.get(url, params=params)
data = response.json()

#print(json.dumps(data, indent=2, ensure_ascii=False))  #전체 출력값 확인

informations = dict()
wanted_categories = ['T1H', 'PTY', 'SKY', 'LGT', 'WSD', 'RN1']  # 필터링할 항목

# 원하는 항목만 필터링
for item in data['response']['body']['items']['item']:
    category = item['category']
    if category in wanted_categories:
        baseTime = item['baseTime']
        value = item['obsrValue']

        if baseTime not in informations:
            informations[baseTime] = {}
        informations[baseTime][category] = value

# ✅ 주요 날씨 항목 출력
category_labels = {
    'T1H': '기온(℃)',
    'RN1': '1시간 강수량(mm)',
    'SKY': '하늘 상태(1:맑음 3:구름많음 4:흐림)',
    'PTY': '강수형태(0:없음 1:비 2:비/눈 3:눈 4:소나기)',
    'REH': '습도(%)',
    'VEC': '풍향',
    'WSD': '풍속(m/s)',
    'LGT': '낙뢰(kA)'
}

print(f"\n✅ {base_date} {base_time} 기준 청주시 서원구 사창동 날씨:")
for baseTime, values in informations.items():
    print(f"\n🕒 예보 시각: {baseTime}")
    for cat, val in values.items():
        label = category_labels.get(cat, cat)
        print(f"  • {label}: {val}")

#json파일로 저장
with open("cheongju_weather.json", "w", encoding="utf-8") as f:
    json.dump(informations, f, indent=2, ensure_ascii=False)