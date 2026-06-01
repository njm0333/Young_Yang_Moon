# -*-coding:utf-8-*-
import random
import socket
import os
import sys
import hashlib
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from werkzeug.utils import secure_filename

# 📰 [모듈화 링킹] 외부 격리 매니저 부품들 일제히 소환
from news_manager import get_all_news, generate_dynamic_combination_news
from diet_manager import calculate_diet_nutrition
from account_manager import execute_buy_order, MECORP_ASSET, get_bmi_status # 🚀 통합 자산 매니저 & 메타데이터 분석기 소환

app = Flask(__name__)
# 🚀 [신규 추가] 세션 암호화 키 (로그인 데이터 유지용)
app.secret_key = 'young_yang_moon_secret_key'

# ====================================================================
# 🛠️ [경로 주입 및 인라인 모듈 결합 파트]
# ====================================================================
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)

ocr_folder_path = os.path.join(root_dir, 'OCR')
yolo_folder_path = os.path.join(root_dir, 'Yolo')

if ocr_folder_path not in sys.path: sys.path.append(ocr_folder_path)
if yolo_folder_path not in sys.path: sys.path.append(yolo_folder_path)

try:
    from ocr import process_nutrition_image
    print("🔤 [시스템 신호] 형의 EasyOCR 크로스체크 엔진 결합 완료.")
except Exception as e:
    print(f"⚠️ [경고] OCR 모듈 임포트 실패: {e}")

try:
    from detection import init_yolo_model, run_yolo_detection
    init_yolo_model()
except Exception as e:
    print(f"⚠️ [경고] YOLO 딥러닝 모듈 함수 링킹 실패: {e}")

# ====================================================================
# 📊 [CSV 데이터 통합 로드 파트]
# ====================================================================
try:
    food_df = pd.read_csv('../Fooddata/19k_food.csv', encoding='utf-8')
    processed_df = pd.read_csv('../Fooddata/27M_product.csv', encoding='utf-8')
    nutrient_df = pd.read_csv('../Fooddata/food_nutrition.csv', encoding='utf-8')
    nutrient_df['음 식 명'] = nutrient_df['음 식 명'].astype(str).str.strip()
    print("\n" + "═"*60)
    print("📊 [영양문 거래소] 상장 음식/가공식품/식단 CSV 로드 완료!")
    print("═"*60 + "\n")
except Exception as e:
    print(f"⚠️ [경고] CSV 상장 데이터 로드 실패: {e}")
    nutrient_df = pd.DataFrame()

# ====================================================================
# 🌐 [웹 브라우저 라우팅 파트]
# ====================================================================
@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login_process', methods=['POST'])
def login_process():
    user_name = request.form.get('username', '무명주주')

    # 🚀 [핵심 연결부] 프론트엔드에서 넘어온 신체 펀더멘털을 세션에 영구 저장
    session['user_profile'] = {
        'age': int(request.form.get('age', 24)),
        'height': float(request.form.get('height', 175.0)),
        'weight': float(request.form.get('weight', 70.0)),
        'invest_type': request.form.get('invest_type', '가치투자형')
    }

    random_code = random.randint(100000, 999999)
    full_stock_name = f"{user_name}({random_code})"

    acc_part1 = random.randint(1000, 9999)
    acc_part2 = random.randint(1000, 9999)
    account_types = ["위탁종합", "증권종합", "종합계좌", "MTS종합", "해외종합"]
    full_account_name = f"{acc_part1}-{acc_part2} [{random.choice(account_types)}]"

    return redirect(url_for('universal_router', stock_name=full_stock_name, account_name=full_account_name, page='main'))


@app.route('/main')
def universal_router():
    stock_name = request.args.get('stock_name', '무명주주(000000)')
    account_name = request.args.get('account_name', '0000-0000 [위탁종합]')
    target_page = request.args.get('page', 'main')

    hash_val = int(hashlib.md5(stock_name.encode('utf-8')).hexdigest(), 16)
    stock_code = str((hash_val % 900000) + 100000)
    base_price = int(request.args.get('forced_price', (random.randint(10000, 100000) // 50) * 50))

    # 검색창에서 넘어온 영양소 데이터를 먼저 안전하게 파싱합니다.
    nutrients = {
        'kcal': request.args.get('kcal', '0'),
        'carbo': request.args.get('carbo', '0'),
        'sugar': request.args.get('sugar', '0'),
        'protein': request.args.get('protein', '0'),
        'fat': request.args.get('fat', '0'),
        'sfat': request.args.get('sfat', '0'),
        'tfat': request.args.get('tfat', '0'),
        'chol': request.args.get('chol', '0'),
        'sodium': request.args.get('sodium', '0')
    }

    # 📡 [수술 완료] 이제 kcal가 아니라 'execute_trade' 플래그가 있어야만 실제 결제를 진행합니다!
    is_execute = request.args.get('execute_trade', 'false')

    if is_execute == 'true':
        food_title = request.args.get('food_name', stock_name)
        buy_qty = int(request.args.get('qty', 1))

        user_profile = session.get('user_profile', {'age': 24, 'height': 175.0, 'weight': 70.0, 'invest_type': '가치투자형'})
        bmi_label, _ = get_bmi_status(user_profile['height'], user_profile['weight'])
        age_label = f"{user_profile['age'] // 10 * 10}대"
        meta_labels = {'bmi_label': bmi_label, 'age_label': age_label}

        news_keywords = execute_buy_order(food_title, buy_qty, base_price, nutrients, user_profile)
        generate_dynamic_combination_news(food_title, news_keywords, user_profile, meta_labels)

        # 결제 완료 후 새로고침 방지용 리다이렉트 (영양소 꼬리표 떼어내기)
        return redirect(url_for('universal_router', stock_name=stock_name, account_name=account_name, page=target_page))

    # 화면 렌더링 분기 (결제가 아닐 땐 영양소 딕셔너리를 HTML로 예쁘게 내려줌)
    if target_page == 'main':
        return render_template('main.html', stock_name=stock_name, stock_code=stock_code, base_price=base_price, account_name=account_name, nutrients=nutrients)

    elif target_page == 'search':
        return render_template('search.html', stock_name=stock_name, account_name=account_name)

    elif target_page == 'news':
        return render_template('news.html', stock_name=stock_name, account_name=account_name, news_list=get_all_news())

    elif target_page == 'account':
        return render_template('account.html', stock_name=stock_name, account_name=account_name, asset=MECORP_ASSET)

    return render_template(f'{target_page}.html', stock_name=stock_name, account_name=account_name)


# ====================================================================

# ====================================================================
# ⚡ [AI 연동 비동기 통신 비즈니스 라우터 파트]
# ====================================================================

@app.route('/api/upload_ocr', methods=['POST'])
def api_upload_ocr():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': '파일이 전달되지 않았습니다.'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': '선택된 사진 파일이 없습니다.'}), 400

    try:
        save_dir = os.path.join(root_dir, 'OCR', 'Images')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        filename = secure_filename(file.filename)
        if not filename or len(filename.split('.')) < 2:
            filename = f"ocr_input_{random.randint(1000, 9999)}.jpg"

        saved_image_path = os.path.join(save_dir, filename)
        file.save(saved_image_path)

        final_nutrition_dto = process_nutrition_image(saved_image_path)
        web_image_url = f"/api/ocr_image/{filename}"

        return jsonify({
            'status': 'success',
            'result': final_nutrition_dto,
            'image_url': web_image_url
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': f'AI 연산 중 장애 발생: {str(e)}'}), 500

@app.route('/api/ocr_image/<filename>')
def serve_ocr_image(filename):
    from flask import send_from_directory
    save_dir = os.path.join(root_dir, 'OCR', 'Images')
    return send_from_directory(save_dir, filename)


@app.route('/api/upload_yolo', methods=['POST'])
def api_upload_yolo():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': '파일이 없습니다.'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': '파일명이 비어있습니다.'}), 400

    try:
        save_dir = os.path.join(root_dir, 'Yolo', 'Images')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        filename = secure_filename(file.filename)
        if not filename:
            filename = f"yolo_input_{random.randint(1000, 9999)}.jpg"

        saved_image_path = os.path.join(save_dir, filename)
        file.save(saved_image_path)

        print(f"\n🚀 [AI 파이프라인] YOLOv3 내부 엔진 가동 시작: {filename}")
        xml_output_dir = os.path.join(root_dir, 'Yolo_output')

        yolo_success, detected_code = run_yolo_detection(saved_image_path, xml_output_dir)

        if not yolo_success:
            print(f"⚠️ [탐지 실패] XML 미생성 혹은 인식물체 없음 ➔ 직접 검색 이동!")
            return jsonify({'status': 'fail', 'code': 'YOLO_FAIL'})

        final_result = calculate_diet_nutrition(filename, xml_output_dir, nutrient_df)
        print(f"✅ [탐지 성공] 코드: {detected_code} ➔ 찐 이름 매칭 완료: '{final_result['food_name']}'")

        web_image_url = f"/api/yolo_image/{filename}"

        return jsonify({
            'status': 'success',
            'result': final_result,
            'image_url': web_image_url
        })

    except Exception as e:
        print(f"❌ [YOLO/ResNet 연동 내부 장애]: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/yolo_image/<filename>')
def serve_yolo_image(filename):
    from flask import send_from_directory
    save_dir = os.path.join(root_dir, 'Yolo', 'Images')
    return send_from_directory(save_dir, filename)


# ====================================================================
# ⚡ 초고속 실시간 종목 검색 백엔드 API
# ====================================================================
@app.route('/api/search_food')
def api_search_food():
    query = request.args.get('q', '').strip().lower()
    mode = request.args.get('mode', 'recent')

    if mode == 'food':
        df = food_df
    elif mode == 'processed':
        df = processed_df
    else:
        if not food_df.empty and not processed_df.empty:
            df = pd.concat([food_df, processed_df], ignore_index=True)
        elif not food_df.empty: df = food_df
        else: df = processed_df

    if df.empty: return jsonify([])

    if query:
        name_series = df.get('식품명', df.get('대표식품명', pd.Series(dtype=str)))
        cat_series = df.get('식품대분류명', df.get('대표식품명', pd.Series(dtype=str)))
        mask = name_series.fillna('').astype(str).str.lower().str.contains(query) | \
               cat_series.fillna('').astype(str).str.lower().str.contains(query)
        result_df = df[mask]
    else:
        result_df = df.sample(n=min(6, len(df))) if mode == 'recent' else df.head(50)

    output = []
    for _, row in result_df.iterrows():
        name = row.get('식품명', row.get('대표식품명', '이름 없음'))
        # 🚀 [오류 수정 완료] 가공식품의 경우 원래 형님이 짰던 '대표식품명' 폴백으로 롤백!
        cat = row.get('식품대분류명', row.get('대표식품명', '분류 없음'))

        def clean_val(val):
            if pd.isna(val) or str(val).strip() == '-' or str(val).strip() == '': return 0
            try: return round(float(str(val).replace(',', '')), 1)
            except: return 0

        output.append({
            'name': str(name),
            'cat': str(cat),
            'kcal': int(clean_val(row.get('열량', row.get('에너지(kcal)', 0)))),
            'carbo': clean_val(row.get('탄수화물', row.get('탄수화물(g)', 0))),
            'sugar': clean_val(row.get('당류', row.get('당류(g)', 0))),
            'protein': clean_val(row.get('단백질', row.get('단백질(g)', 0))),
            'fat': clean_val(row.get('지방', row.get('지방(g)', 0))),
            'sfat': clean_val(row.get('포화지방', row.get('포화지방(g)', 0))),
            'tfat': clean_val(row.get('트랜스지방', row.get('트랜스지방(g)', 0))),
            'chol': clean_val(row.get('콜레스테롤', row.get('콜레스테롤(mg)', 0))),
            'sodium': clean_val(row.get('나트륨', row.get('나트륨(mg)', 0)))
        })

    return jsonify(output[:30])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)