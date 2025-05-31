import requests
import json
from coord_converter import convert_to_grid
from datetime import datetime



serviceKey = "U5VK8CgJFZwu73FsJKKLz6B2qfAUZcIRmsJf+IV4CCAkqdaWQETKV5igoCm40QZ6Od89IGv3p8+iQNcxCqxwWA==" # 본인의 서비스 키 입력

now = datetime.now()

base_date = now.strftime("%Y%m%d")  # YYYYMMDD 형식
base_time = now.strftime("%H00")   # HH00 형식 (시간은 00분 기준)

url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"

with open('markingData.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    for id, item in data.items():
        lat = float(item['위도'])
        lon = float(item['경도'])
        nx, ny = convert_to_grid(lat, lon)

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
        for items in api_data['response']['body']['items']['item']:
            category = items['category']
            if category in wanted_categories:
                baseTime = items['baseTime']
                value = items['obsrValue']

                if baseTime not in informations:
                    informations[baseTime] = {}
                informations[baseTime][category] = value

        # 주요 날씨 항목 출력
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
        item["날씨"] = informations

with open('weatherupdate.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# 4. 다시 저장
