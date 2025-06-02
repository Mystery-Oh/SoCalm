import requests
from coord_converter import convert_to_grid
from datetime import datetime
import json
import csv

serviceKey = "" # 본인의 서비스 키 입력
url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"

now = datetime.now()

base_date = now.strftime("%Y%m%d")  # YYYYMMDD 형식
base_time = now.strftime("%H00")   # HH00 형식 (시간은 00분 기준)

final_data = {}
file_list = ['accident_cheongju/cheongjuAccident.csv','accident_cheongju/cheongjuAccident2.csv']


for filename in file_list:
    with open(filename, encoding='utf-8') as csvfile:
        accident_data = csv.DictReader(csvfile)
        #print(accident_data.fieldnames) 열이름 체크
        for item in accident_data:
            id = item.get('\ufeff사고다발지fid') or item.get('\ufeff다발지역 에프아이디(FID)')
            name = item['지점명']
            lat = float(item['위도'])
            lon = float(item['경도'])
            사고건수 = item['사고건수']
            if 사고건수 == '0':
                continue
            사고종류 = item.get('사고종류', None)
            사상자수 = item['사상자수']
            사망자수 = item['사망자수']
            중상자수 = item['중상자수']
            경상자수 = item['경상자수']
            polygon = item.get('다발지역폴리곤')
            try:
                polygon = json.loads(polygon) if polygon else None
            except json.JSONDecodeError:
                polygon = None  # 잘못된 형식이면 None 처리

            nx, ny = convert_to_grid(lat, lon)

            # url

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

            final_data[id] = {
                "지점명": name,
                "날씨": informations,
                "위도": lat,
                "경도": lon,
                "사고종류": 사고종류,
                "사고건수": 사고건수,
                "사상자수": 사상자수,
                "사망자수": 사망자수,
                "중상자수": 중상자수,
                "경상자수": 경상자수,
                "다발지역폴리곤": polygon
            }
            print(id)


print(final_data)
with open('algorithms/markingData.json', 'w', encoding='utf-8') as outfile:
    json.dump(final_data, outfile, ensure_ascii=False)
    outfile.write('\n')
print('생성 완료!')



