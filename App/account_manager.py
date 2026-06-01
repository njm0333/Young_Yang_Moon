# -*-coding:utf-8-*-
import time
from datetime import datetime

# ====================================================================
# 💰 [Me.corp 전역 기업 가치 및 자산 장부]
# ====================================================================
MECORP_ASSET = {
    'current_price': 100000000.0,
    'prev_price': 100000000.0,
    'change_amt': 0,
    'change_rate': 0.0,
    'kcal': 0.0, 'carbo': 0.0, 'sugar': 0.0, 'protein': 0.0, 'fat': 0.0,
    'sfat': 0.0, 'tfat': 0.0, 'chol': 0.0, 'sodium': 0.0,
    'portfolio': {},
    'total_asset': 0,
    'total_eval_profit': 0,
    'total_eval_rate': 0.0,
    'today_realized_profit': 0
}

def get_bmi_status(height, weight):
    try:
        bmi = weight / ((height / 100) ** 2)
        if bmi < 18.5: return "저체중", bmi
        elif bmi < 23.0: return "정상", bmi
        elif bmi < 25.0: return "과체중", bmi
        else: return "비만", bmi
    except ZeroDivisionError:
        return "정상", 22.0

def execute_buy_order(food_name, qty, buy_price, nutrients, user_profile):
    """
    🛒 [MTS 주문 체결 및 자산 포트폴리오 스토리지 누적 제어기]
    """
    global MECORP_ASSET

    if food_name in MECORP_ASSET['portfolio']:
        MECORP_ASSET['portfolio'][food_name]['quantity'] += qty
        MECORP_ASSET['portfolio'][food_name]['eval_amount'] += (buy_price * qty)
        for key in ['kcal', 'carbo', 'sugar', 'protein', 'fat', 'sfat', 'tfat', 'chol', 'sodium']:
            MECORP_ASSET['portfolio'][food_name][key] = float(MECORP_ASSET['portfolio'][food_name].get(key, 0)) + (float(nutrients.get(key, '0')) * qty)
    else:
        MECORP_ASSET['portfolio'][food_name] = {
            'quantity': qty,
            'eval_amount': buy_price * qty,
            'eval_profit': 0,
            'eval_rate': 0.0
        }
        for key in ['kcal', 'carbo', 'sugar', 'protein', 'fat', 'sfat', 'tfat', 'chol', 'sodium']:
            MECORP_ASSET['portfolio'][food_name][key] = float(nutrients.get(key, '0')) * qty

    MECORP_ASSET['total_asset'] = sum(item['eval_amount'] for item in MECORP_ASSET['portfolio'].values())
    return update_asset_and_calculate_stock(nutrients, user_profile)

def update_asset_and_calculate_stock(nutrients, user_profile):
    """
    🎰 [Me.corp 계량 퀀트 기반 기업가치 산출 복리 엔진]
    """
    global MECORP_ASSET
    MECORP_ASSET['prev_price'] = MECORP_ASSET['current_price']

    # 누적 성분 업데이트
    for key in ['kcal', 'carbo', 'sugar', 'protein', 'fat', 'sfat', 'tfat', 'chol', 'sodium']:
        MECORP_ASSET[key] += float(nutrients.get(key, 0))

    # 하이퍼파라미터 로드
    age = int(user_profile.get('age', 24))
    invest_type = user_profile.get('invest_type', '가치투자형')
    bmi_label, _ = get_bmi_status(float(user_profile.get('height', 175.0)), float(user_profile.get('weight', 70.0)))
    current_hour = datetime.now().hour

    # 현 자산 입력 명세 변수화
    v = {k: float(nutrients.get(k, 0)) for k in ['kcal', 'carbo', 'sugar', 'protein', 'fat', 'sfat', 'tfat', 'chol', 'sodium']}

    # 1. 퀀트 자산 평가지표 산출 (Score Matrix 계산)
    bad_score = (v['sugar'] * 2.5) + (v['sfat'] * 1.8) + (v['tfat'] * 15.0) + (v['sodium'] / 80.0)
    good_score = v['protein'] * 3.0

    rate_impact = 0.0
    news_keywords = []

    # 2. 자산 클래스 절대 분류 모델 매핑 테이블 (Blue Chip / Junk Bond / Growth / Speculative)
    is_blue_chip = (0 < v['kcal'] <= 200 and bad_score <= 12.0)
    is_junk_bond = (bad_score >= 35.0 or v['kcal'] >= 800 or v['sodium'] >= 1100 or v['sugar'] >= 25)
    is_growth_stock = (good_score >= 45.0 or (v['protein'] >= 15.0 and bad_score <= 20.0))

    if is_blue_chip:
        rate_impact = 0.050
        news_keywords.append("오전장_공복_웰빙매수")
    elif is_junk_bond:
        rate_impact = -0.055
        news_keywords.append("클린주_불순물_악재")
    elif is_growth_stock:
        rate_impact = 0.035
        news_keywords.append("정규장_단백질_순매수")
    else:
        # 가치 한계 및 보합 종목 분류 내재 연산
        if v['protein'] < 5.0 and v['carbo'] >= 50.0:
            rate_impact = -0.015
            news_keywords.append("클린주_불순물_악재")
        else:
            rate_impact = 0.005
            news_keywords.append("정규장_단백질_순매수")

    # 3. 투자 전략(컨셉) 매트릭스 계수 가중치 최적화
    strategy_multipliers = {
        '가치투자형': 0.8,
        '레버리지형': 2.0,
        '배당성장형': 1.0,
        '스몰캡_클린주': 1.0,
        '숏스퀴즈형': 1.0
    }

    # 기본 가중치 스케일링 적용
    rate_impact *= strategy_multipliers.get(invest_type, 1.0)

    # 투자 전략별 특수 알파 오프셋 반영
    if invest_type == '레버리지형' and rate_impact > 0:
        news_keywords.append("레버리지_초대형_매수")
    elif invest_type == '배당성장형' and v['protein'] >= 20.0:
        rate_impact += 0.015
        news_keywords.append("대규모_배당(단백질)_지급")
    elif invest_type == '스몰캡_클린주' and (v['sugar'] >= 8.0 or v['fat'] >= 12.0):
        rate_impact -= 0.025
    elif invest_type == '숏스퀴즈형' and v['kcal'] <= 300.0 and v['carbo'] <= 35.0:
        rate_impact += 0.025
        news_keywords.append("지방_공매도_청산")
    elif invest_type == '레버리지형' and v['kcal'] < 400.0 if 'is_junk_bond' not in locals() else False:
        # 벌크업 동력 상실 패널티 조건
        rate_impact -= 0.02
        news_keywords.append("벌크업_동력_상실")

    # 펀더멘털 리스크 패널티 (비만일 경우 가중 오염 타격 누적)
    if bmi_label == "비만" and rate_impact < 0:
        rate_impact *= 1.5

    # 4. 거시 타임라인 변동성 이벤트 반영
    if 5 <= current_hour < 11 and v['sugar'] >= 15.0:
        rate_impact -= 0.03
        news_keywords = ["오전장_공복_당류쇼크"]
    elif (21 <= current_hour or current_hour < 4) and v['kcal'] >= 450.0:
        rate_impact -= 0.04
        news_keywords = ["시간외_야식_폭탄투하"]

    # 나이 제한 리스크 헷징
    if age >= 40 and (v['sodium'] >= 1200 or v['sugar'] >= 25):
        rate_impact -= 0.02
        if rate_impact < 0:
            news_keywords.append("4050_만성질환_경고")

    # 5. [인과관계 싱크로율 정밀 동기화 레이어]
    positive_signals = ["오전장_공복_웰빙매수", "정규장_단백질_순매수", "지방_공매도_청산", "레버리지_초대형_매수"]
    if rate_impact > 0:
        if not any(signal in news_keywords for signal in positive_signals):
            news_keywords.append("정규장_단백질_순매수")
    elif rate_impact < 0:
        news_keywords = [kw for kw in news_keywords if kw not in positive_signals]
        if not news_keywords:
            news_keywords.append("클린주_불순물_악재")

    # 6. 전역 자산 밸류에이션 확정 및 누적 총합 산출
    MECORP_ASSET['current_price'] = MECORP_ASSET['current_price'] * (1.0 + rate_impact)
    if MECORP_ASSET['current_price'] < 100.0:
        MECORP_ASSET['current_price'] = 100.0

    # 상장가 원금(1억 원) 대비 불변식 마크투마켓(Mark-to-Market) 누적 손익 연산
    MECORP_ASSET['change_amt'] = int(round(MECORP_ASSET['current_price'] - 100000000.0))
    MECORP_ASSET['change_rate'] = ((MECORP_ASSET['current_price'] - 100000000.0) / 100000000.0) * 100

    return news_keywords