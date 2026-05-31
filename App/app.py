# -*-coding:utf-8-*-
import random
import socket
import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# ====================================================================
# 📊 [CSV 데이터 통합 로드 파트]
# 서버 가동 시 30MB CSV 파일들을 메모리에 미리 고속 탑재합니다.
# ====================================================================
try:
    # 경로 규칙: 프로젝트 루트 폴더 내 data 폴더 안의 파일들
    food_df = pd.read_csv('../Fooddata/19k_food.csv', encoding='utf-8')
    processed_df = pd.read_csv('../Fooddata/27M_product.csv', encoding='utf-8')
    print("\n" + "═"*60)
    print("📊 [영양문 거래소] 상장 음식/가공식품 데이터 로드 성공!")
    print(f"   • 일반 음식 데이터: {len(food_df)}개 행 로드 완료")
    print(f"   • 가공 식품 데이터: {len(processed_df)}개 행 로드 완료")
    print("═"*60 + "\n")
except Exception as e:
    print("\n" + "❌"*30)
    print(f"⚠️ [경고] CSV 상장 데이터 로드에 실패했습니다! 경로를 확인하세요.")
    print(f"    오류 내용: {e}")
    print("❌"*30 + "\n")
    # 파일이 없을 경우 빈 데이터프레임으로 백업하여 서버 다운 방지
    food_df = pd.DataFrame()
    processed_df = pd.DataFrame()


# ====================================================================
# 🌐 [웹 브라우저 라우팅 파트]
# ====================================================================

# 1. 처음 접속 시 로그인 화면을 보여줌
@app.route('/')
def login_page():
    return render_template('login.html')

# 2. 로그인 버튼을 누르면 처리하는 중간 통로 (랜덤 코드 및 랜덤 계좌 생성)
@app.route('/login_process', methods=['POST'])
def login_process():
    user_name = request.form.get('username')
    random_code = random.randint(100000, 999999)
    full_stock_name = f"{user_name}({random_code})"

    # 로그인 시 랜덤 계좌 정보 생성
    acc_part1 = random.randint(1000, 9999) # 앞 4자리
    acc_part2 = random.randint(1000, 9999) # 뒤 4자리

    account_types = ["위탁종합", "증권종합", "종합계좌", "MTS종합", "해외종합"]
    chosen_type = random.choice(account_types)
    full_account_name = f"{acc_part1}-{acc_part2} [{chosen_type}]"

    # 생성된 종목명과 계좌명을 가지고 만능 라우터로 리다이렉트
    return redirect(url_for('universal_router', stock_name=full_stock_name, account_name=full_account_name, page='main'))

@app.route('/main')
def universal_router():
    stock_name = request.args.get('stock_name', '무명주주(000000)')
    account_name = request.args.get('account_name', '0000-0000 [위탁종합]')
    target_page = request.args.get('page', 'main')

    if target_page == 'main':
        import hashlib
        # 음식 이름을 기반으로 고유한 6자리 종목코드 파싱
        hash_val = int(hashlib.md5(stock_name.encode('utf-8')).hexdigest(), 16)
        stock_code = str((hash_val % 900000) + 100000)

        # 🎰 [형의 필승 지침 반영: 50원 단위 난수 생성 공식]
        # 1. 먼저 10000에서 100000 사이의 임의의 숫자를 뽑아줍니다.
        raw_random_price = random.randint(10000, 100000)

        # 2. 50원으로 나눈 몫에 다시 50을 곱해서 완벽하게 50원 단위(50원, 100원, 150원...)로 가공합니다.
        base_price = (raw_random_price // 50) * 50

        # 중요: 계산된 50원 단위의 랜덤 주가를 프론트엔드로 바인딩
        return render_template('main.html',
                               stock_name=stock_name,
                               stock_code=stock_code,
                               base_price=base_price,
                               account_name=account_name,
                               session="정규장")

    return render_template(f'{target_page}.html', stock_name=stock_name, account_name=account_name, session="정규장")
# ====================================================================
# ⚡ [초고속 실시간 종목 검색 백엔드 API]
# 프론트엔드 자바스크립트(fetch) 요청을 받아 CSV에서 데이터를 즉시 추려냄
# ====================================================================
@app.route('/api/search_food')
def api_search_food():
    query = request.args.get('q', '').strip().lower()
    mode = request.args.get('mode', 'recent')  # recent, food, processed 탭 구분자

    # 1. 사용자가 클릭한 하단 탭 모드에 맞춰 검색 대상 데이터프레임 선정
    if mode == 'food':
        df = food_df
    elif mode == 'processed':
        df = processed_df
    else:
        # 최근(recent) 혹은 전체 모드일 때는 두 CSV 데이터를 하나로 바인딩
        if not food_df.empty and not processed_df.empty:
            df = pd.concat([food_df, processed_df], ignore_index=True)
        elif not food_df.empty:
            df = food_df
        else:
            df = processed_df

    if df.empty:
        return jsonify([])

    # 2. 실시간 다이내믹 타이핑 필터링 연산
    if query:
        # 형이 준 CSV 스펙 칼럼명 자동 감지 예외 처리 적용
        name_col = '식품명' if '식품명' in df.columns else ('대표식품명' if '대표식품명' in df.columns else '')
        cat_col = '식품대분류명' if '식품대분류명' in df.columns else ('대표식품명' if '대표식품명' in df.columns else '')

        if name_col == '':
            return jsonify([])  # 칼럼 매칭 안 되면 빈 배열 반환

        # 대소문자 구분 없이 상품명이나 분류명에 검색어가 포함되었는지 마스킹 연산
        mask = df[name_col].astype(str).str.lower().str.contains(query) | df[cat_col].astype(str).str.lower().str.contains(query)
        result_df = df[mask]
    else:
        # 검색어가 비어있고 '최근' 탭 세션이면 MTS 감성용으로 무작위 6개 샘플링 상장
        if mode == 'recent':
            result_df = df.sample(n=min(6, len(df)))
        else:
            # 검색어 없이 일반음식/가공식품 탭을 누르면 상위 50개 리스트 가이드 표출
            result_df = df.head(50)

    # 3. 프론트엔드 UI 컴포넌트(search.html) 규격에 최적화된 JSON 가공
    output = []
    for _, row in result_df.iterrows():
        name = row.get('식품명', row.get('대표식품명', '이름 없음'))
        cat = row.get('식품대분류명', row.get('대표식품명', '분류 없음'))
        kcal = row.get('열량', 0)

        output.append({
            'name': str(name),
            'cat': str(cat),
            'kcal': int(kcal) if pd.notnull(kcal) else 0
        })

    # 트래픽 및 스마트폰 렌더링 부하 최적화를 위해 상위 30개 종목으로 슬라이싱 반환
    return jsonify(output[:30])


# ====================================================================
# 🚀 [서버 부팅 파트]
# ====================================================================
if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()

    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        print("\n" + "="*60)
        print(f"🚀 영양문 터미널 서버가 가동되었습니다!")
        print(f"💻 PC 접속 주소: http://localhost:5000")
        print(f"📱 동일 와이파이 핸드폰 접속 주소: http://{local_ip}:5000")
        print("="*60 + "\n")

    # host='0.0.0.0' 외부 IP 치고 모바일 디바이스 진입 허용 옵션 유지
    app.run(host='0.0.0.0', port=5000, debug=True)