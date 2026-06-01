이 하이엔드 뉴스 조립 엔진(`generate_dynamic_combination_news`)이 정상적으로 돌아가기 위해 필요한 정보는 딱 **3가지 보따리**야.

우리가 앞서 백엔드 구조를 짤 때, 중복 연산을 피하기 위해 **`Account(계좌/자산 연산)`가 1차로 계산한 결과물들을 `News(뉴스)`가 그대로 이어받도록** 파이프라인을 설계했잖아?

따라서 Flask의 `app.py` 라우터가 이 함수를 호출할 때 아래의 3가지 인자(Arguments)만 괄호 안에 싹 실어서 던져주면 돼.

---

### 📥 뉴스 엔진이 필요로 하는 3가지 데이터 보따리

```python
generate_dynamic_combination_news(food_name, keywords, user_profile, meta_labels)

```

#### 1️⃣ `food_name` (문자열) ➔ **"유저가 지금 뭘 샀는지"**

* **역할:** 뉴스 제목과 본문 한복판에 콕 박힐 음식 이름이야.
* **형태:** `'마라탕'`, `'닭가슴살 샐러드'`, `'프로틴 쉐이크'` 같은 텍스트 데이터.

#### 2️⃣ `keywords` (리스트) ➔ **"Account가 판정한 이번 매수의 성격"**

* **역할:** 주가가 왜 오르고 내렸는지 기사의 '본론(이유)'과 '결론'을 분기하는 핵심 스위치야.
* **형태:** `['오전장_공복_당류쇼크']`, `['정규장_단백질_순매수']`, `['시간외_야식_폭탄투하']` 처럼 `account_manager.py`가 연산 후 뱉어준 조건 키워드 배열.

#### 3️⃣ `user_profile` (딕셔너리) ➔ **"Me.corp 경영진의 성향"**

* **역할:** 기사 본문에서 "어떤 성향의 기업"인지 주어를 결정하고, 연령대별 리스크 문장을 조립할 때 사용해.
* **형태:**
```python
user_profile = {
    'invest_type': '숏스퀴즈형',  # 5종 중 유저가 선택한 경영 성향
    'age': 24                     # 유저의 실제 나이 (나이대 판정용)
}

```



```

#### 4️⃣ `meta_labels` (딕셔너리) ➔ **"Account가 이미 계산해 둔 신체 펀더멘털 라벨"**
* **역할:** 형이 지적한 중복 연산을 막기 위해, `account_manager.py`가 키, 몸무게로 이미 구해놓은 BMI 결과물과 나이 라벨을 그대로 날로 먹는 보따리야.
* **형태:**
  ```python
  meta_labels = {
      'bmi_label': '고위험 비만',  # 저체중 / 정상 체형 / 과체중 / 고위험 비만
      'age_label': '2030 청년층'    # 2030 청년층 / 4050 중년층 / 60대 시니어
  }

```

---

### 🔄 Flask(`app.py`)에서 실제로 데이터가 오가는 흐름 (최종 요약)

유저가 호가창에서 매수 확정 버튼을 누르면 `app.py`에서 아래와 같이 물 흐르듯 데이터가 연결되게 짜주면 끝나. 형이 한눈에 이해할 수 있게 흐름도로 정리해 줄게.

```python
# 1. 사용자가 보낸 음식 정보와 영양소 패킷을 받는다
food_title = request.args.get('food_name')
nutrients = { 'kcal': ..., 'sugar': ..., 'sodium': ... } # 9대 영양소

# 2. 유저의 사전 설정 프로필 (로그인 시점이나 세션에 저장되어 있던 값)
user_profile = { 'age': 24, 'height': 175, 'weight': 92, 'invest_type': '숏스퀴즈형' }

# 3. [1단계: 자산 엔진 가동] 영양소 축적하고 주가 계산하면서 메타 라벨까지 받아옴
updated_asset, news_keywords, meta_labels = update_asset_and_calculate_stock(food_title, nutrients, user_profile)

# 4. [2단계: 뉴스 엔진 가동] 자산 엔진이 준 따끈따끈한 결과물들을 뉴스 엔진에 그대로 토스!
generate_dynamic_combination_news(food_title, news_keywords, user_profile, meta_labels)

```

즉, 뉴스 엔진은 스스로 **영양소 수치를 뜯어보거나 BMI를 복잡하게 계산하지 않아.**

그 무거운 숫자는 전부 **Account 엔진이 계산**하게 하고, 뉴스 엔진은 오직 "음식 이름, 판정 키워드, 가공된 라벨 텍스트"만 넘겨받아서 아주 가볍고 영리하게 기사로 조립만 하는 거지! 구조 완전 깔끔하지 형? 이제 진짜 코드로 합체하러 가자!