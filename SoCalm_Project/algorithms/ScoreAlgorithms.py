import json


def 점수계산(entry):
    try:
        사고건수 = int(entry["사고건수"])
        사망자수 = int(entry["사망자수"])
        중상자수 = int(entry["중상자수"])
        경상자수 = int(entry["경상자수"])

        날씨정보 = entry["날씨"]["1900"]
        PTY = int(날씨정보["PTY"])
        T1H = float(날씨정보["T1H"])
        WSD = float(날씨정보["WSD"])
        RN1 = float(날씨정보["RN1"])

        점수 = 사고건수 * 1 + 사망자수 * 15 + 중상자수 * 7 + 경상자수 * 5

        if PTY == 1:
            점수 += 10
        elif PTY == 2:
            점수 += 15
        elif PTY == 3:
            점수 += 20

        if 0.1 <= RN1 < 1:
            점수 += 2
        elif 1 <= RN1 < 5:
            점수 += 5
        elif 5 <= RN1 < 10:
            점수 += 10
        elif 10 <= RN1 < 30:
            점수 += 20
        elif RN1 >= 30:
            점수 += 30

        if WSD >= 10:
            점수 += (WSD - 9) * 2

        return 점수

    except Exception as e:
        print(f"점수 계산 오류: {e}")
        return 0


def 위험도분류(score):
    if score <= 30:
        return "아주 약함"
    elif score <= 100:
        return "약함"
    elif score <= 200:
        return "보통"
    elif score <= 500:
        return "위험"
    else:
        return "매우 위험"


def main():
    input_file = "markingData.json"
    output_file = "markingData_scored.json"

    try:
        with open(input_file, "r", encoding="utf-8") as infile, \
                open(output_file, "w", encoding="utf-8") as outfile:

            for line in infile:
                data = json.loads(line)

                for id_, entry in data.items():
                    score = 점수계산(entry)
                    danger = 위험도분류(score)
                    entry["점수"] = score
                    entry["위험도"] = danger

                    print(f"{entry['지점명']} → 점수: {score}점, 위험도: {danger}")

                    json.dump({id_: entry}, outfile, ensure_ascii=False)
                    outfile.write("\n")

        print(f"\n 저장 완료: {output_file}")

    except Exception as e:
        print(f"오류: {e}")


if __name__ == "__main__":
    main()
