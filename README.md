# Young_Yang_Moon

<img width="1762" height="893" alt="image" src="https://github.com/user-attachments/assets/c0c1bdc5-82ef-4cc9-a877-148d270f519c" />


## Young Yang Moon - 영양문 모바일
영양문 모바일은 주식 거래 플랫폼인 **영웅문 S#**을 오마주한 프로그램으로, 사용자의 신체 조건과 영양소 섭취 목표를 고려하여 MTS 인터페이스 기반의 목표 달성을 지원하는 것을 목표로 합니다. 비전 인식과 OCR 기능을 활용하여 개인의 일일 영양 자산을 실시간으로 기록, 누적, 분석하는 웰니스 플랫폼입니다.


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
    - [function/PCA_Report.py](#functionpca_reportpy)
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


## Reference

- [AI Hub - 음식 이미지 및 영양정보 텍스트](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=74) _ 데이터셋 및 Yolo, Resnet 참고

- [https://github.com/JangMinSeong/Diet101](https://github.com/JangMinSeong/Diet101) _ OCR 및 Flask 디자인 참고

- [키움증권 영웅문S#](https://play.google.com/store/apps/details?id=com.kiwoom.heromts&hl=ko) _ Flask 디자인, 로고 오마주

- [식품의약품안전처 식품영양성분 데이터베이스](https://various.foodsafetykorea.go.kr/nutrient/general/down/historyList.do) _ 음식, 가공식품 DB
  
