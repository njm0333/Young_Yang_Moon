# Young_Yang_Moon

<img width="1762" height="893" alt="image" src="https://github.com/user-attachments/assets/c0c1bdc5-82ef-4cc9-a877-148d270f519c" />


## Young Yang Moon - 영양문 모바일
영양문 모바일은 주식 거래 플랫폼인 영웅문 S#을 오마주한 프로그램으로, 사용자의 신체 조건과 영양소 섭취 목표를 고려하여 MTS 인터페이스 기반의 목표 달성을 지원하는 것을 목표로 합니다. 비전 인식과 OCR 기능을 활용하여 개인의 일일 영양 자산을 실시간으로 기록, 누적, 분석하는 웰니스 플랫폼입니다.


## Introduction

최근 현대 사회에서 건강 관리와 다이어트는 단순한 체중 감량을 넘어, 개인이 관리해야 할 중요한 **‘신체 자산(Bodily Capital)’** 으로 인식되고 있습니다.

하지만 많은 사람들은 운동과 식단 관리의 중요성을 알고 있음에도 불구하고, 귀찮음이나 낮은 지속성 등의 이유로 꾸준한 관리를 어려워합니다. 특히 음식명을 직접 검색하고, 섭취량을 계산하여 기록해야 하는 번거로운 과정은 많은 사용자가 중도에 관리를 포기하게 만드는 구조적 한계로 작용하고 있습니다.

그러던 중, 저는 주식 시장에서는 호가창을 바라보며 초 단위로 몰입하는 개인 투자자들의 열정을 보며 한 가지 질문을 떠올렸습니다.

**“내가 먹는 음식을 주식 종목처럼 매수하고, 내 몸의 영양 상태를 가상 계좌 장부처럼 실시간으로 추적한다면 어떨까?”**

이 질문에서 시작된 것이 바로 **영양문 모바일** 프로젝트입니다.

**프로젝트를 관통하는 핵심 철학은 내가 먹은 음식이 나의 신체자산의 가치를 떨어뜨릴수도, 올릴수도 있다는 사실입니다.**

본 프로젝트는 투자 시스템의 사고방식을 식단 관리에 접목하였습니다. 사용자는 자신의 신체를 하나의 **Me.corp** 로 정의하고 이를 운영하게 됩니다.

음식을 섭취하는 행위는 단순한 소비가 아닌 **‘자산 매수’** 로 해석되며, 사용자의 선택과 매수 행위는 곧 Me.corp의 가치에 직접적인 영향을 미치게 됩니다.

영양문 모바일은 건강 관리를 단순한 기록이 아닌, 사용자가 직접 운영하는 **신체 자산 관리 경험**으로 바꾸는 것을 목표로 합니다.

이 프로젝트가 여러분의 건강한 신체 자산 관리 여정에 실질적인 도움이 되기를 바랍니다.



## 개발한 사람
- njm0333(노정민) : 전체 개발 총괄

## 목차
- [설치](#설치)
- [프로그램 소개](#프로그램-소개)
- [전체 기능 및 구현 설명 _ for dev](#전체-기능-및-구현-설명-_-for-dev)
- [Reference](#reference)



## 설치

본 프로젝트는 conda 환경을 통해 의존성을 관리합니다. [conda 다운로드](https://www.anaconda.com/download)

### **1. 설치 및 환경 구축**

Windows 시작 메뉴에서 전용 터미널(**Anaconda Prompt** 또는 **Miniconda Prompt**)을 열고 원하는 저장소로 이동합니다. 바탕화면 등 한글 이름의 폴더는 피하고 영문 경로(예: `C:\Workspace`)를 이용해 주세요.

아래의 명령어에서 기본 경로를 바꿔서 실행해주세요.


```
cd C:\
mkdir Y_Y_Moon
cd Y_Y_Moon
git clone https://github.com/njm0333/Young_Yang_Moon.git
cd Young_Yang_Moon
conda env create -f environment.yaml
conda activate yolov3
```

- 가상환경 구축 및 패키지 다운로드에 다소 시간이 소요될 수 있습니다 (약 5~8분).


### **2. AI 가중치 파일 수동 다운로드**

가상환경 세팅이 완료되면 가중치 파일을 직접 다운로드하여 프로젝트 폴더 내 지정된 경로에 넣어주세요.

- [best_403food_e200b150v2.pt 다운로드](https://drive.google.com/file/d/1iwbbaJjO-zrD2FTxpRU-vVZOjIEGDvu0/view?usp=sharing)

  `Young_Yang_Moon/Yolo/` 폴더 안으로 이동

- [new_opencv_ckpt_b84_e200.pth 다운로드](https://drive.google.com/file/d/1M7tH-za2Y9kbN08J5GD7yYgnwNGecNLJ/view?usp=drive_link)

  `Young_Yang_Moon/Resnet/weights/` 폴더 안으로 이동


### 3. 서버 실행

열려있는 터미널에서 아래 명령어를 실행하여 웹 서버를 가동합니다.

```
python App/app.py
```

- 첫 실행 시 시간이 다소 걸릴 수 있습니다 (1분 이내).

- 터미널에 로딩 완료 메시지가 뜨면 브라우저에서 `http://127.0.0.1:5000` 으로 접속하여 이용하실 수 있습니다.

- 컴퓨터와 스마트폰이 같은 Wi-Fi 네트워크에 있다면, 핸드폰 브라우저에 내부 IP(예: `192.168.x.x:5000`)를 입력하여 모바일에서도 모든 기능을 사용할 수 있습니다.



## 프로그램 소개

https://github.com/user-attachments/assets/312e01b8-6e4f-461c-952e-8558454da2c9

### 1. 로그인


|**시작 화면**|**운용목표**|**로딩화면**|
|---|---|---|
|<img width="822" height="1322" alt="image" src="https://github.com/user-attachments/assets/ed50981e-7b78-47f7-afcb-d0ed331dc760" />|<img width="822" height="1322" alt="image" src="https://github.com/user-attachments/assets/3a186463-32c3-4eb1-b7ec-0ae9a511f623" />|<img width="822" height="1322" alt="image" src="https://github.com/user-attachments/assets/971fdeab-e792-4c5b-b5ec-2847626090ab" />
| 인적사항을 기입합니다 | 선택한 투자사항은 나의 신체자산을 계산하는 로직에 서로 다르게 활용됩니다   |로딩중...|


### 2-1. 검색 화면_사진,OCR


| **사진 인식** | **사진인식** | **영양 정보 OCR** | **영양정보 OCR** |
| -------------- | ------------- | -------------- | ------------- |
| <img width="822" height="1322" alt="image" src="https://github.com/user-attachments/assets/3b468217-c412-4942-b406-b0227a9f066c" />| <img width="822" height="1322" alt="image" src="https://github.com/user-attachments/assets/ce923e58-dac2-4003-abd6-d0a6639c859e" />| <img width="822" height="1322" alt="image" src="https://github.com/user-attachments/assets/88e8a8a8-55c5-48ab-a486-31313bbb6464" />| <img width="822" height="1322" alt="image" src="https://github.com/user-attachments/assets/8b121a75-baaa-40c5-ba93-85963c487cde" />|
| 사진을 분석해 음식의 종류와 양을 추정하고 | 그 비율에 맞게 영양소를 분석합니다 |영양 성분표를 분석해|영양소를 입력합니다|


### 2-2. 검색 화면_직접 검색


| **최근검색**  | **일반 음식**  | **가공식품**  | 
| -------------- | ------------- | -------------- | 
| <img width="822" height="1322" alt="image" src="https://github.com/user-attachments/assets/05f075ad-7f19-47a8-8019-409d75d0dcb3" />|<img width="822" height="1322" alt="image" src="https://github.com/user-attachments/assets/43415a58-351b-4e1a-8af9-ce3df720bf9c" /> | <img width="822" height="1322" alt="image" src="https://github.com/user-attachments/assets/a51679ff-ec91-484f-8359-6829015e734b" /> |
| 최근에 검색한 메뉴들을 보여줍니다 | 성분표가 없는 일반 음식들을 100g 단위로 보여줍니다 | 가공식품들의 영양정보를 고릅니다 | 


### 3. 주문화면



| **주문화면** | **체결** | **체결 수량** | 
| ----- | ----- | ----- | 
| <img width="822" height="1322" alt="image" src="https://github.com/user-attachments/assets/2a2b2d40-df16-486c-a6af-7049f5729073" />| <img width="822" height="1322" alt="image" src="https://github.com/user-attachments/assets/3f6aee6f-51d5-414d-a3d3-8f4b2337ac4f" />| <img width="822" height="1322" alt="image" src="https://github.com/user-attachments/assets/6ac9103f-3881-4180-bc28-d08f298396f3" />
| 선택한 음식을 먹었다는걸 체결로 표현하는 주문화면입니다 | 고른 음식의 영양성분을 보여줍니다 | 과자를 두 개 먹었다면 곱해진 영양성분을 계산합니다 |


### 4. 뉴스 및 자산


| **뉴스** | **자산** | **신체 자산 증식** |
| -------------- | ------------- | -------------- | 
| <img width="822" height="1322" alt="image" src="https://github.com/user-attachments/assets/121b7ba7-c256-4fec-b6b5-487381c74224" />| <img width="822" height="1322" alt="image" src="https://github.com/user-attachments/assets/af38ad45-00c5-4dda-9198-89b3325e6ede" />| <img width="822" height="1322" alt="image" src="https://github.com/user-attachments/assets/20eff789-5b60-4a23-8c2a-8683b6e617cf" />| 
| 먹은 음식이 건강에 좋은지, 안좋은지 간접적으로 뉴스를 통해 알려줍니다  | 내가 먹은 음식은 나의 신체자산의 가치를 떨어뜨릴수도, 올릴수도 있습니다  | 이미 먹은 음식을 매도 할 수는 없습니다. 좋은 음식의 비중을 높여 신체자산을 증식하세요 |

## 전체 기능 및 구현 설명 _ for dev

### 사진인식
사진 인식 기능은 음식의 종류를 탐지하는 YOLO 모델과 양을 추정하는 ResNet 모델을 결합한 방식으로 구현되었습니다.

- **음식 종류 탐지(Yolo) :** `Darknet` 아키텍처를 활용하며, 400여개의 한식 클래스가 학습된 가중치를 사용합니다. 따라서 한식 위주의 400개 이외의 이미지에는 변별력이 현저히 떨어진다는 한계가 있습니다. 입력 이미지를 320x320 크기로 전처리하여 네트워크를 통과시킨 후, NMS알고리즘을 적용해 중첩된 객체의 바운딩 박스를 최적화합니다.탐지된 객체의 8자리 클래스 ID는 내부 매핑 데이터(`code_foodname.csv`)를 거쳐 실제 한식 명칭으로 치환되며, 최종 좌표와 함께 XML 파일로 구조화되어 Resnet으로 전달됩니다.

- **음식 양 추정 (ResNet):** YOLO를 통해 크롭된 영역을 입력받아, 감지된 음식의 양을 25% 간격의 5단계(Q1: 25% ~ Q5: 125%)로 추정합니다.

추론이 모두 완료되면, 추출된 라벨과 수량 단계(Q)는 내부 영양 DB(`NutriNomics/Fooddata/food_nutrition.csv`)와 결합되어 최종 영양소로 환산됩니다. 이 과정에서 연산의 기준점이 되는 Q4(100%)는 절대 무게(100g)가 아닌 DB에 정의된 해당 음식의 '평균 1회 제공량'으로 할당됩니다. (예: 쌀밥 탐지 시, Q4 100%를 100g이 아닌 210g으로 스케일링하여 영양소 계산)

---

### 영양성분 OCR 인식

영양성분 OCR 인식 기능은 OpenCV와 EasyOCR을 사용하여 이미지에서 텍스트를 추출하고, 상태기계 기반 파서를 통해 구조화된 영양 정보를 복원하는 파이프라인입니다.

일반적인 정규식 파싱의 한계를 극복하기 위해, 영양성분 키워드(OCR 오인식 별칭 포함)를 탐색하여 해당 상태로 전환한 뒤 수치를 수집하는 방식으로 작동합니다. 이 과정에서 'O'를 '0'으로, '96'을 '%'로 변환하는 등 한국어 영양성분표에서 자주 발생하는 인식 오류와 텍스트 노이즈를 휴리스틱 기법으로 자동 보정하여 레이아웃이 어긋난 이미지에서도 안정적인 추출을 돕습니다.

데이터가 일부 누락되었을 경우, 대한민국 식약처 지정 1일 영양성분 기준치를 활용해 비율(%)에서 무게(g)를 역산하여 정보를 복원합니다. 또한 열량 정보가 누락되었을 때는 탄수화물, 단백질, 지방의 매크로 영양소 비율(4:4:9)을 적용해 총 열량을 스스로 계산합니다. 다만, 이 파이프라인은 한국 영양성분표 양식에 최적화되어 있어 심하게 훼손된 이미지에서는 OCR 품질 저하로 인식률이 떨어질 수 있으며, 기준치 기반의 자동 추정값을 사용하기 때문에 실제 제조사의 표기 수치와 미세한 차이가 발생할 수 있습니다.

사용자가 인식된 영양소의 수치를 조절할 수 있는 기능도 들어있습니다.

---

### 직접 입력
직접 입력 기능은 사용자가 섭취한 음식을 직접 검색해 기록하는 기능으로, 대상의 특성에 따라 '일반 음식'과 '가공식품' 두 가지 카테고리로 나누어 작동합니다.

- **일반 음식:** 식당 음식이나 직접 조리하여 영양성분을 정확히 알기 어려운 경우에 사용합니다. 내부 데이터베이스(`NutriNomics/Fooddata/19k_food.csv`)를 참조하여 계산하며, 사진 인식 기능(1회 제공량 기준)과 달리 **100g을 기준 단위**로 하여 영양소를 산출합니다.
    
- **가공식품:** 시중에 판매되는 완제품을 기록할 때 사용합니다. 식품의약품안전처 데이터베이스에 등록된 약 27만 개의 가공식품 정보가 담긴 파일(`NutriNomics/Fooddata/27M_product.csv`)을 참조하며, 100g 단위가 아닌 **해당 가공식품 1개(포장 단위)의 양을 기준**으로 영양소를 계산합니다.

---

### 뉴스 및 자산

뉴스 및 자산 기능은 영양성분 수치와 사용자 프로필(키, 체중, 나이, 투자 성향)을 결합한 다중 조건부 알고리즘을 통해 구현되었습니다.

- **자산 평가 및 주가 산출 (`account_manager.py`):** 매수(섭취)가 발생하면 입력된 영양소를 바탕으로 가중치 수식을 적용하여 `bad_score`(당류, 포화/트랜스지방, 나트륨 중심)와 `good_score`(단백질 중심)를 산출합니다. 이를 통해 해당 음식을 1차 분류합니다. 이후 사용자의 현재 섭취 시간(야식, 공복임에도 과한 당류 섭취 등), 나이, BMI 지수, 그리고 투자 성향에 따른 배수를 연산하여 주가 변동률을 결정하고 특정 뉴스 키워드를 트리거합니다.
    
- **동적 뉴스 생성 (`news_manager.py`):** 자산 평가 단계에서 반환된 `news_keywords`를 핵심 트리거로 사용합니다. 사용자가 설정한 5가지 투자 성향과 BMI 라벨에 따라 사전 정의된 기사 템플릿(제목, 서론, 본론, 결론)이 매핑되며 언론사 및 말머리 선택 로직이 결합되어 경제 시황 형태의 뉴스를 동적으로 생성합니다.
    
- **상태 관리 및 프론트엔드:** 사용자의 포트폴리오(섭취 내역), 누적 영양소, 주가 변동 히스토리는 백엔드의 인메모리 구조로 관리됩니다. 프론트엔드에서는 Jinja2 템플릿 엔진을 활용해 보유 종목별 영양성분과 포트폴리오 비중을 동적으로 렌더링합니다. 또한, 누적된 주가 데이터를 클라이언트로 전달하여 JavaScript와 순수 SVG만으로 경량화된 차트를 그려내어 틱 단위의 자산 추이를 시각화합니다. 사용자 식별을 위한 증권 계좌 및 종목 코드는 `hashlib.md5`를 활용해 결정론적으로 생성됩니다.

## Reference

- [AI Hub - 음식 이미지 및 영양정보 텍스트](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=74) _ 데이터셋 및 Yolo, Resnet 참고

- [https://github.com/JangMinSeong/Diet101](https://github.com/JangMinSeong/Diet101) _ OCR 및 Flask 디자인 참고

- [키움증권 영웅문S#](https://play.google.com/store/apps/details?id=com.kiwoom.heromts&hl=ko) _ Flask 디자인, 로고 오마주

- [식품의약품안전처 식품영양성분 데이터베이스](https://various.foodsafetykorea.go.kr/nutrient/general/down/historyList.do) _ 음식, 가공식품 DB
  
