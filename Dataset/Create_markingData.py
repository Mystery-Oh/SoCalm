import requests
from coord_converter import convert_to_grid
from datetime import datetime
import json
import csv

serviceKey = "A0HK/SOeu1VN3B3SYlqE+WE77Bqw9x7nZ2D96eM9PTZpRyKULaisgX8LMZLeTFxuFM0WpQCzlPc6OqOaB8OgPQ==" # 본인의 서비스 키 입력

now = datetime.now()

base_date = now.strftime("%Y%m%d")  # YYYYMMDD 형식
base_time = now.strftime("%H00")   # HH00 형식 (시간은 00분 기준)

file_list = ['accident_cheongju/cheongjuAccident.csv', 'accident_cheongju/cheongjuAccident2.csv']

with open('markingData.jsonl', 'a', encoding='utf-8') as outfile:
    for filename in file_list:
        with open(filename, 'r', encoding='utf-8') as csvfile:
            accident_data = csv.DictReader(csvfile)
            for item in accident_data:
                id = item.get('사고다발지id') or item.get('다발지역 아이디(ID)')
                name = item['지점명']
                lat = float(item['위도'])
                lon = float(item['경도'])
                nx, ny = convert_to_grid(lat, lon)

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

                response = requests.get(url, params=params)
                api_data = response.json()

                # print(json.dumps(data, indent=2, ensure_ascii=False))  #전체 출력값 확인

                informations = {}
                wanted_categories = ['T1H', 'PTY', 'SKY', 'LGT', 'WSD', 'RN1']  # 필터링할 항목

                # 원하는 항목만 필터링
                for item in api_data['response']['body']['items']['item']:
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

                final_data = {}
                final_data[id] = {
                    "지점명": name,
                    "날씨": informations,
                    "위도": lat,
                    "경도": lon
                }
                print(final_data)
                json.dump(final_data, outfile, ensure_ascii=False)
                outfile.write('\n')

print('생성 완료!')



