# -*-coding:utf-8-*-
import time
from datetime import datetime

# 💰 [Me.corp 전역 자산 스토리지]
MECORP_ASSET = {
    'current_price': 100000.0,
    'prev_price': 100000.0,
    'change_amt': 0.0,
    'change_rate': 0.0,
    'kcal': 0.0, 'carbo': 0.0, 'sugar': 0.0, 'protein': 0.0, 'fat': 0.0,
    'sfat': 0.0, 'tfat': 0.0, 'chol': 0.0, 'sodium': 0.0
}

def get_bmi_status(height, weight):
    """ 키와 몸무게로 BMI 지수를 계산하여 체형 라벨링 """
    try:
        bmi = weight / ((height / 100) ** 2)
        if bmi < 18.5: return "저체중", bmi
        elif bmi < 23.0: return "정상", bmi
        elif bmi < 25.0: return "과체중", bmi
        else: return "비만", bmi
    except:
        return "정상", 22.0

def update_asset_and_calculate_stock(food_name, nutrients, user_profile):
    """
    🎰 [Me.corp 하이엔드 복리 엔진]
    나이, BMI, 투자성향(목표), 시간대가 유기적으로 맞물려 주가 등락률(%)을 산출함
    """
    global MECORP_ASSET

    MECORP_ASSET['prev_price'] = MECORP_ASSET['current_price']
    for key in ['kcal', 'carbo', 'sugar', 'protein', 'fat', 'sfat', 'tfat', 'chol', 'sodium']:
        MECORP_ASSET[key] += float(nutrients.get(key, 0))

    # 👤 [1] 유저 펀더멘털 파싱
    age = int(user_profile.get('age', 24))
    height = float(user_profile.get('height', 175.0))
    weight = float(user_profile.get('weight', 70.0))
    invest_type = user_profile.get('invest_type', '가치투자형')

    bmi_label, bmi_val = get_bmi_status(height, weight)

    # 영양소 수치
    req_kcal = float(nutrients.get('kcal', 0))
    req_carbo = float(nutrients.get('carbo', 0))
    req_sugar = float(nutrients.get('sugar', 0))
    req_protein = float(nutrients.get('protein', 0))
    req_fat = float(nutrients.get('fat', 0))
    req_sodium = float(nutrients.get('sodium', 0))

    # 기본 등락률 및 뉴스 키워드
    rate_impact = 0.0
    news_keywords = []

    # ⚙️ [2] 펀더멘털(BMI) 기반 칼로리 타격 계수 산정
    # 마른 사람은 고칼로리를 먹어도 타격이 적고, 뚱뚱할수록 타격이 배가됨
    kcal_penalty = 1.0
    if bmi_label == "비만": kcal_penalty = 1.5
    elif bmi_label == "저체중": kcal_penalty = 0.4

    # 📊 [3] 투자 성향별 코어 알고리즘 연산
    if invest_type == '가치투자형':  # 안정형
        if req_protein >= 20 and req_kcal <= 600: rate_impact += 0.02
        if req_sodium >= 800: rate_impact -= 0.03
        if req_sugar >= 20: rate_impact -= 0.03

    elif invest_type == '배당성장형':  # 근육형
        if req_protein >= 25:
            rate_impact += 0.04
            news_keywords.append("대규모_배당(단백질)_지급")
        # 단백질 투자를 위한 잉여 칼로리는 타격 경감
        if req_kcal >= 800: rate_impact -= (0.015 * kcal_penalty)

    elif invest_type == '스몰캡_클린주':  # 린매스업형
        if req_sugar >= 10 or req_fat >= 15:
            rate_impact -= 0.05
            news_keywords.append("클린주_불순물_악재")
        elif req_protein >= 20 and req_carbo <= 60:
            rate_impact += 0.035

    elif invest_type == '숏스퀴즈형':  # 다이어트형
        if req_kcal >= 500 or req_carbo >= 70:
            # 다이어트 중 고칼로리 투하는 대형 악재 (비만이면 더 심하게 떡락)
            rate_impact -= (0.04 * kcal_penalty)
        elif req_kcal <= 350 and req_protein >= 15:
            rate_impact += 0.045
            news_keywords.append("지방_공매도_청산")

    elif invest_type == '레버리지형':  # 벌크업형
        if req_kcal >= 1000 and req_protein >= 30:
            rate_impact += 0.06
            news_keywords.append("레버리지_초대형_매수")
        elif req_kcal < 400:
            # 벌크업인데 안 먹으면 동력 상실로 폭락
            rate_impact -= 0.05
            news_keywords.append("벌크업_동력_상실")

    # 🧬 [4] 연령대별 만성질환 리스크 팩터 반영 (질병청 통계 기반)
    if 40 <= age < 60:
        # 4050은 고혈압/당뇨 발병률이 높으므로 나트륨/당류 초과 시 추가 페널티
        if req_sodium >= 1000 or req_sugar >= 25:
            rate_impact -= 0.025
            news_keywords.append("4050_만성질환_경고")
    elif age >= 60:
        # 65세 이상 노년층의 탄수화물 과잉 섭취(에너지적정비율 초과) 리스크
        if req_carbo >= 120:
            rate_impact -= 0.02
    elif age < 40:
        # 2030의 급격한 비만율 증가 리스크 (단당류/트랜스지방)
        if req_sugar >= 30:
            rate_impact -= 0.015

    # ⏰ [5] 시간대(생체 리듬) 추가 가중치
    current_hour = datetime.now().hour
    if 5 <= current_hour < 11 and req_sugar >= 15:
        rate_impact -= 0.025
        news_keywords.append("오전장_혈당_스파이크")
    elif (22 <= current_hour or current_hour < 4):
        # 야식은 모두에게 악재지만, 비만 체형에게는 1.5배의 레버리지 악재로 작용
        if req_sodium >= 600 or req_kcal >= 500:
            rate_impact -= (0.035 * kcal_penalty)
            news_keywords.append("시간외_야식_악재")

    # 📈 [6] 복리 적용 및 방어선 구축
    MECORP_ASSET['current_price'] = MECORP_ASSET['current_price'] * (1.0 + rate_impact)
    if MECORP_ASSET['current_price'] < 1000.0:
        MECORP_ASSET['current_price'] = 1000.0

    MECORP_ASSET['change_amt'] = MECORP_ASSET['current_price'] - MECORP_ASSET['prev_price']
    MECORP_ASSET['change_rate'] = (MECORP_ASSET['change_amt'] / MECORP_ASSET['prev_price']) * 100

    # UI 렌더링용 정수 변환 복사본 반환
    display_asset = MECORP_ASSET.copy()
    for key in ['current_price', 'prev_price', 'change_amt']:
        display_asset[key] = int(round(display_asset[key]))

    return display_asset, news_keywords