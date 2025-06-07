import json

input_path = "danger.json"
output_path = "danger_fixed.json"

merged_data = {}

with open(input_path, "r", encoding="utf-8") as infile:
    for line in infile:
        if not line.strip():
            continue
        obj = json.loads(line)
        merged_data.update(obj)

with open(output_path, "w", encoding="utf-8") as outfile:
    json.dump(merged_data, outfile, ensure_ascii=False, indent=2)

print(f"✅ 변환 완료: {output_path}")
