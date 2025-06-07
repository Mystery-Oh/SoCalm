# SoCalm- [Project summary](#SoCalm)
  - [Purpose](#purpose)
  - [Schedule](#schedule)
  - [Requirements](#requirements)
  - [How to install](#how-to-install)
  - [How to use](#how-to-use)
  - [Contacts](#contacts)
  - [License](#license)

---

### Project summary  

보행자를 위한 안전도 평가 지도 프로그램을 만들자!  

#### Purpose  

자율주행 차량의 경로 최적화의 일부분으로 사용 될 수 있다.  
자율주행에서의 핵심은 보행자 안전이기 때문.  
보행자 교통사고 사망자는 차량사고 사망자에 비해 압도적으로 많다.  
그래서 보행자 교통사고의 예방을 위해 이 프로젝트를 선택했다.  

### Schedule  

1주차 ~ 6주차 : 주제 정하기 및 개발 계획 및 개발 역할 분담  
7주차 : html을 통해 웹페이지 구현 (전반적인 프론트앤드 개발) + 티맵 api연동  
8주차 : 데이터베이스 구축  
9주차 ~ 11주차 : 교통사고 및 날씨 데이터 수집  
12주차 : flask를 활용해서 로컬 서버 구현  
13주차 : 데이터베이스 구축 및 웹페이지에 들어가는 기능 구현 (위험지역 맵핑 등) , 데이터를 웹페이지에 구현시킬 수 있는 알고리즘 개발  
14주차 : 전반적인 프론트엔드 및 백엔드 유지 보수 + '제보하기' 데이터 베이스에 저장  

---

#### Requirements  

* requirements.txt 참고.  

---

#### How to install  

Clone & Install  

```sh
git clone git@github.com:Mystery-Oh/SoCalm.git
cd SoCalm
pip3 install -r requirements.txt
```

---

### How to use  
![로그인](https://github.com/user-attachments/assets/eaf136fe-eed5-4980-941c-24cf1afdd995)  
웹페이지 접속 후 로그인  
아이디가 없다면 아이디가 없으신가요 클릭 후 회원가입  
![회원가입](https://github.com/user-attachments/assets/1ef9ed19-c17f-4a27-9d8a-4a1bfcdfb687)  
정보 입력 후 회원가입  
![위험도]("https://github.com/user-attachments/assets/5fcb4be5-475b-4361-a492-8a67d0f78b07")  
지도에서 위험정보 확인 가능  
지도에서 위치 클릭 시 위험지역 제보 가능  
![제보](https://github.com/user-attachments/assets/6add0f31-a693-4a6d-b6e1-ee7c6038c152)  
위험지역 클릭 뒤 내용 입력 후 제보하기  
![제보완료](https://github.com/user-attachments/assets/3a44fdd8-4bdc-45b5-8647-88f27cc0f5fd)  
제보 완료  

.env 파일에 Tmap api키, 기상청 api키, MySQL연결 필요  
run.py 실행

---

### Contacts  

오희승 dghmltmd2760@gmail.com  
이정주 leezungzoo@gmail.com  
장현규 hyeongyu0117@naver.com  

---

### License  

`SoCalm`은 `modified MIT` 라이선스 하에 공개되어 있습니다. 모델 및 코드를 사용할 경우 라이선스 내용을 준수해주세요. 라이선스 전문은 `LICENSE` 파일에서 확인하실 수 있습니다.  
