import os

# 변환할 파일 경로
original_file = 'accident_cheongju/cheongjuAccident4.csv'
converted_file = 'accident_cheongju/cheongjuAccident4.csv'

# 원래 인코딩이 cp949라고 가정 (Windows에서 흔함)
with open(original_file, 'r', encoding='cp949') as infile, \
     open(converted_file, 'w', encoding='utf-8', newline='') as outfile:
    data = infile.read()
    outfile.write(data)

print(f"{converted_file} 파일이 UTF-8로 저장되었습니다.")