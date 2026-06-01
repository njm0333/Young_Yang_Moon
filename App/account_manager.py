# -*-coding:utf-8-*-
import time
from datetime import datetime

# 💰 [Me.corp 전역 자산 스토리지 통합본]
MECORP_ASSET = {
    'current_price': 100000.0,
    'prev_price': 100000.0,
    'change_amt': 0,
    'change_rate': 0.0,
    'kcal': 0.0, 'carbo': 0.0, 'sugar': 0.0, 'protein': 0.0, 'fat': 0.0,
    'sfat': 0.0, 'tfat': 0.0, 'chol': 0.0, 'sodium': 0.0,

    # 🎯 [account.html 렌더링용 포트폴리오 확장]
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
    except:
        return "정상", 22.0

def execute_buy_order(food_name, qty, buy_price, nutrients, user_profile):
    """
    🛒 [매수 체결 및 포트폴리오 누적 관제탑]
    app.py에서 체결 신호가 오면 개별 종목을 장바구니에 담고 복리 엔진을 가동합니다.
    """
    global MECORP_ASSET

    # 1. 포트폴리오(개별 종목) 누적
    if food_name in MECORP_ASSET['portfolio']:
        MECORP_ASSET['portfolio'][food_name]['quantity'] += qty
        MECORP_ASSET['portfolio'][food_name]['eval_amount'] += (buy_price * qty)
    else:
        MECORP_ASSET['portfolio'][food_name] = {
            'quantity': qty,
            'eval_amount': buy_price * qty,
            'eval_profit': 0, # 현재는 데모용 0 (추후 시세 변동 로직 연동 가능)
            'eval_rate': 0.0
        }

    # 2. 총 자산 업데이트
    total_amt = sum(item['eval_amount'] for item in MECORP_ASSET['portfolio'].values())
    MECORP_ASSET['total_asset'] = total_amt

    # 3. 하이엔드 복리 엔진으로 주가 타격 계산
    news_keywords = update_asset_and_calculate_stock(nutrients, user_profile)
    return news_keywords

def update_asset_and_calculate_stock(nutrients, user_profile):
    """ 🎰 [Me.corp 하이엔드 복리 엔진] """
    global MECORP_ASSET

    MECORP_ASSET['prev_price'] = MECORP_ASSET['current_price']
    for key in ['kcal', 'carbo', 'sugar', 'protein', 'fat', 'sfat', 'tfat', 'chol', 'sodium']:
        MECORP_ASSET[key] += float(nutrients.get(key, 0))

    age = int(user_profile.get('age', 24))
    height = float(user_profile.get('height', 175.0))
    weight = float(user_profile.get('weight', 70.0))
    invest_type = user_profile.get('invest_type', '가치투자형')

    bmi_label, _ = get_bmi_status(height, weight)

    req_kcal = float(nutrients.get('kcal', 0))
    req_carbo = float(nutrients.get('carbo', 0))
    req_sugar = float(nutrients.get('sugar', 0))
    req_protein = float(nutrients.get('protein', 0))
    req_fat = float(nutrients.get('fat', 0))
    req_sodium = float(nutrients.get('sodium', 0))

    rate_impact = 0.0
    news_keywords = []

    kcal_penalty = 1.5 if bmi_label == "비만" else (0.4 if bmi_label == "저체중" else 1.0)

    if invest_type == '가치투자형':
        if req_protein >= 20 and req_kcal <= 600: rate_impact += 0.02
        if req_sodium >= 800: rate_impact -= 0.03
        if req_sugar >= 20: rate_impact -= 0.03
    elif invest_type == '배당성장형':
        if req_protein >= 25:
            rate_impact += 0.04
            news_keywords.append("대규모_배당(단백질)_지급")
        if req_kcal >= 800: rate_impact -= (0.015 * kcal_penalty)
    elif invest_type == '스몰캡_클린주':
        if req_sugar >= 10 or req_fat >= 15:
            rate_impact -= 0.05
            news_keywords.append("클린주_불순물_악재")
        elif req_protein >= 20 and req_carbo <= 60:
            rate_impact += 0.035
    elif invest_type == '숏스퀴즈형':
        if req_kcal >= 500 or req_carbo >= 70:
            rate_impact -= (0.04 * kcal_penalty)
        elif req_kcal <= 350 and req_protein >= 15:
            rate_impact += 0.045
            news_keywords.append("지방_공매도_청산")
    elif invest_type == '레버리지형':
        if req_kcal >= 1000 and req_protein >= 30:
            rate_impact += 0.06
            news_keywords.append("레버리지_초대형_매수")
        elif req_kcal < 400:
            rate_impact -= 0.05
            news_keywords.append("벌크업_동력_상실")

    if 40 <= age < 60:
        if req_sodium >= 1000 or req_sugar >= 25:
            rate_impact -= 0.025
            news_keywords.append("4050_만성질환_경고")
    elif age >= 60:
        if req_carbo >= 120: rate_impact -= 0.02
    elif age < 40:
        if req_sugar >= 30: rate_impact -= 0.015

    current_hour = datetime.now().hour
    if 5 <= current_hour < 11 and req_sugar >= 15:
        rate_impact -= 0.025
        news_keywords.append("오전장_혈당_스파이크")
    elif (22 <= current_hour or current_hour < 4):
        if req_sodium >= 600 or req_kcal >= 500:
            rate_impact -= (0.035 * kcal_penalty)
            news_keywords.append("시간외_야식_악재")

    # 복리 적용
    MECORP_ASSET['current_price'] = MECORP_ASSET['current_price'] * (1.0 + rate_impact)
    if MECORP_ASSET['current_price'] < 1000.0: MECORP_ASSET['current_price'] = 1000.0

    # 변동액을 자산 탭 UI 호환을 위해 정수형(int)으로 캐스팅
    MECORP_ASSET['change_amt'] = int(round(MECORP_ASSET['current_price'] - MECORP_ASSET['prev_price']))
    MECORP_ASSET['change_rate'] = (MECORP_ASSET['change_amt'] / MECORP_ASSET['prev_price']) * 100

    return news_keywords