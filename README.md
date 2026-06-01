# Young_Yang_Moon

<img width="1762" height="893" alt="image" src="https://github.com/user-attachments/assets/c0c1bdc5-82ef-4cc9-a877-148d270f519c" />


## Young Yang Moon - 영양문 모바일
영양문 모바일은 사용자의 신체 조건과 영양소 섭취 목표를 고려하여, MTS 인터페이스 기반의 목표 달성을 지원하는 것을 목표로 합니다. 비전 인식과 OCR 기능을 활용하여 개인의 일일 영양 자산을 실시간으로 기록, 누적, 분석하는 웰니스 플랫폼입니다.


## Introduction

최근 현대 사회에서 건강 관리와 다이어트는 단순한 체중 감량을 넘어, 개인이 관리해야 할 중요한 **‘신체 자산(Bodily Capital)’** 으로 인식되고 있습니다.

하지만 많은 사람들은 운동과 식단 관리의 중요성을 알고 있음에도 불구하고, 귀찮음이나 낮은 지속성 등의 이유로 꾸준한 관리를 어려워합니다. 특히 음식명을 직접 검색하고, 섭취량을 계산하여 기록해야 하는 번거로운 과정은 많은 사용자가 중도에 관리를 포기하게 만드는 구조적 한계로 작용하고 있습니다.

그러던 중, 저는 주식 시장에서 호가창을 바라보며 초 단위로 몰입하는 개인 투자자들의 모습을 보며 한 가지 질문을 떠올렸습니다.

**“내가 먹는 음식을 주식 종목처럼 매수하고, 내 몸의 영양 상태를 가상 계좌 장부처럼 실시간으로 추적한다면 어떨까?”**

이 질문에서 시작된 것이 바로 **영양문 모바일** 프로젝트입니다.

본 프로젝트는 투자 시스템의 사고방식을 식단 관리에 접목하였습니다. 사용자는 자신의 신체를 하나의 **Me.corp** 로 정의하고 이를 운영하게 됩니다.

음식을 섭취하는 행위는 단순한 소비가 아닌 **‘자산 매수’** 로 해석되며, 사용자의 선택과 매수 행위는 곧 Me.corp의 가치에 직접적인 영향을 미치게 됩니다.

영양문 모바일은 건강 관리를 단순한 기록이 아닌, 사용자가 직접 운영하는 **신체 자산 관리 경험**으로 바꾸는 것을 목표로 합니다.

이 프로젝트가 여러분의 건강한 신체 자산 관리 여정에 실질적인 도움이 되기를 바랍니다.



## 개발한 사람
- njm0333(노정민) : 전체 개발 총괄

## 목차
- [설치](#설치)
- [사용법](#사용법)
- [전체 기능 및 구현 설명 _ for dev](#전체-기능-및-구현-설명-_-for-dev)
    - [windows/survey_window.py](#windowssurvey_windowpy)
    - [windows/pca_window.py](#windowspca_windowpy)
    - [function/PCA_Report.py](#functionpca_reportpy)
- [추가 개발예정 사항](#추가-개발예정-사항)
- [Reference](#reference)
- [License](#license)


- [best_403food_e200b150v2.pt](https://drive.google.com/file/d/1iwbbaJjO-zrD2FTxpRU-vVZOjIEGDvu0/view?usp=sharing) : NutriNomics\Yolo\best_403food_e200b150v2.pt
- [new_opencv_ckpt_b84_e200.pth](https://drive.google.com/file/d/1M7tH-za2Y9kbN08J5GD7yYgnwNGecNLJ/view?usp=drive_link) : NutriNomics\Resnet\weights\new_opencv_ckpt_b84_e200.pth


