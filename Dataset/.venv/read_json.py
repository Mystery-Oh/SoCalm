import json

#읽을 json파일명
with open('accident_cheongju/cheongjuAccident2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 첫 번째 항목 전체 출력
print(json.dumps(data[0], indent=2, ensure_ascii=False))