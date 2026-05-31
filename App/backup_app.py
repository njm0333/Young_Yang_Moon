# -*-coding:utf-8-*-
import random
import socket
import os
import sys
import hashlib
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ====================================================================
# 🛠️ [경로 주입 및 인라인 모듈 결합 파트]
# ====================================================================
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)

ocr_folder_path = os.path.join(root_dir, 'OCR')
yolo_folder_path = os.path.join(root_dir, 'Yolo')

if ocr_folder_path not in sys.path:
    sys.path.append(ocr_folder_path)
if yolo_folder_path not in sys.path:
    sys.path.append(yolo_folder_path)

# AI 핵심 엔진 임포트
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

    # 🎯 [트랙 A 저격] 일반 식단 전용 핵심 영양 성분표 로드 및 띄어쓰기 공백 정제
    nutrient_df = pd.read_csv('../Fooddata/food_nutrition.csv', encoding='utf-8')
    nutrient_df['음 식 명'] = nutrient_df['음 식 명'].astype(str).str.strip()

    print("\n" + "═"*60)
    print("📊 [영양문 거래소] 상장 음식/가공식품/식단 CSV 로드 완료!")
    print(f"   • 일반 식단 영양 데이터 수: {len(nutrient_df)}개 종목 상장 중")
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
    user_name = request.form.get('username')
    random_code = random.randint(100000, 999999)
    full_stock_name = f"{user_name}({random_code})"

    acc_part1 = random.randint(1000, 9999)
    acc_part2 = random.randint(1000, 9999)

    account_types = ["위탁종합", "증권종합", "종합계좌", "MTS종합", "해외종합"]
    chosen_type = random.choice(account_types)
    full_account_name = f"{acc_part1}-{acc_part2} [{chosen_type}]"

    return redirect(url_for('universal_router', stock_name=full_stock_name, account_name=full_account_name, page='main'))

@app.route('/main')
def universal_router():
    stock_name = request.args.get('stock_name', '무명주주(000000)')
    account_name = request.args.get('account_name', '0000-0000 [위탁종합]')
    target_page = request.args.get('page', 'main')

    if target_page == 'main':
        hash_val = int(hashlib.md5(stock_name.encode('utf-8')).hexdigest(), 16)
        stock_code = str((hash_val % 900000) + 100000)

        forced_price = request.args.get('forced_price', None)
        if forced_price:
            base_price = int(forced_price)
        else:
            raw_random_price = random.randint(10000, 100000)
            base_price = (raw_random_price // 50) * 50

        is_ocr = request.args.get('is_ocr', 'false')
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

        return render_template('main.html',
                               stock_name=stock_name,
                               stock_code=stock_code,
                               base_price=base_price,
                               account_name=account_name,
                               is_ocr=is_ocr,
                               nutrients=nutrients)

    elif target_page == 'search':
        return render_template('search.html', stock_name=stock_name, account_name=account_name)

    return render_template(f'{target_page}.html', stock_name=stock_name, account_name=account_name)


# ====================================================================
# ⚡ [AI 연동 비동기 통신 비즈니스 라우터 파트]
# ====================================================================

# 🔤 [트랙 B] 가공식품 전용 EasyOCR
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


# 📸 [트랙 A] 일반 식단 전용 YOLOv3 + ResNet 인라인 결합 라우터 (찐연동 패치)
@app.route('/api/upload_yolo', methods=['POST'])
def api_upload_yolo():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': '파일이 없습니다.'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': '파일명이 비어있습니다.'}), 400

    try:
        # 1. 사진 수신 및 세이브
        save_dir = os.path.join(root_dir, 'Yolo', 'Images')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        filename = secure_filename(file.filename)
        if not filename:
            filename = f"yolo_input_{random.randint(1000, 9999)}.jpg"

        saved_image_path = os.path.join(save_dir, filename)
        file.save(saved_image_path)

        # 2. YOLOv3 인라인 구동
        print(f"\n🚀 [AI 파이프라인] YOLOv3 내부 엔진 가동 시작: {filename}")
        xml_output_dir = os.path.join(root_dir, 'Yolo_output')

        yolo_success, detected_code = run_yolo_detection(saved_image_path, xml_output_dir)

        if not yolo_success:
            print(f"⚠️ [탐지 실패] XML 미생성 혹은 인식물체 없음 ➔ 직접 검색 이동!")
            return jsonify({'status': 'fail', 'code': 'YOLO_FAIL'})

        # 3. 🛡️ [XML 강제 파싱 디버깅] 숫자가 아닌 <food_name> 한글 명칭 진짜 가로채기
        file_basename = os.path.splitext(filename)[0]
        xml_path = os.path.join(xml_output_dir, f"{file_basename}.xml")

        real_food_name = "알 수 없는 음식"
        if os.path.exists(xml_path):
            import xml.etree.ElementTree as ET
            tree = ET.parse(xml_path)
            root_xml = tree.getroot()
            obj_tag = root_xml.find('object')
            if obj_tag is not None:
                fn_tag = obj_tag.find('food_name')
                if fn_tag is not None and fn_tag.text:
                    real_food_name = fn_tag.text.strip() # 숫자가 아닌 '콩나물국' 추출 성공!

        print(f"✅ [탐지 성공] 코드: {detected_code} ➔ 찐 이름 매칭 완료: '{real_food_name}'")

        # 4. ⚖️ ResNet 중량 비율 예측 바통 터치 구역
        # TODO: 추후 ResNet 연동 완료 시 아래의 mock_q 등급 자리에 실제 추론 코드 바인딩 가능!
        mock_q_level = "Q3" # ResNet 예측 등급 예시 (Q1~Q5)

        # 🎰 [정민's 내부 회로 중량 배율 맵 정의]
        q_ratio_map = {"Q1": 0.25, "Q2": 0.50, "Q3": 0.75, "Q4": 1.00, "Q5": 1.25}
        current_ratio = q_ratio_map.get(mock_q_level, 1.00)

        # 5. 📊 food_nutrition.csv 영양소 추적 및 결측치 치환 연산
        final_result = {
            'food_name': real_food_name,
            'quantity_level': mock_q_level,
            '열량': 0, '탄수화물': 0, '당류': 0, '단백질': 0, '지방': 0,
            '포화지방': 0, '트랜스지방': 0, '콜레스테롤': 0, '나트륨': 0
        }

        if not nutrient_df.empty:
            # CSV 내부에서 한글 명칭과 정확히 매치되는 행 탐색
            matched_rows = nutrient_df[nutrient_df['음 식 명'] == real_food_name]

            if not matched_rows.empty:
                row = matched_rows.iloc[0]

                # 안전한 실수/정수 파싱용 인라인 헬퍼 함수
                def parse_nut(val, multiplier=1.0):
                    if pd.isna(val) or str(val).strip() == '-' or str(val).strip() == '':
                        return 0
                    try:
                        return round(float(str(val).replace(',', '')) * multiplier, 2)
                    except:
                        return 0

                # 기본 중량 가져와서 Q비율 반영한 섭취 중량 계산
                base_weight = parse_nut(row.get('중량(g)', 200))
                calculated_g = round(base_weight * current_ratio, 1)

                # 형 회로 반영: 이제 UI에 Q3 문자가 아니라 계산된 실물 g수가 출력됨!
                final_result['quantity_level'] = f"{calculated_g}g"

                # 9대 영양성분 스펙 곱연산 정밀 추출
                final_result['열량'] = int(parse_nut(row.get('에너지(kcal)'), current_ratio))
                final_result['탄수화물'] = parse_nut(row.get('탄수화물(g)'), current_ratio)
                final_result['당류'] = parse_nut(row.get('당류(g)'), current_ratio)
                final_result['단백질'] = parse_nut(row.get('단백질(g)'), current_ratio)
                final_result['지방'] = parse_nut(row.get('지방(g)'), current_ratio)
                final_result['포화지방'] = parse_nut(row.get('포화지방(g)'), current_ratio) # 만약 없으면 아래 0 방어선 작동
                final_result['트랜스지방'] = parse_nut(row.get('트랜스지방(g)'), current_ratio)
                final_result['콜레스테롤'] = int(parse_nut(row.get('콜레스테롤(mg)'), current_ratio))
                final_result['나트륨'] = int(parse_nut(row.get('나트륨(mg)'), current_ratio))

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
        elif not food_df.empty:
            df = food_df
        else:
            df = processed_df

    if df.empty:
        return jsonify([])

    if query:
        name_series = df.get('식품명', df.get('대표식품명', pd.Series(dtype=str)))
        cat_series = df.get('식품대분류명', df.get('대표식품명', pd.Series(dtype=str)))

        mask = name_series.fillna('').astype(str).str.lower().str.contains(query) | \
               cat_series.fillna('').astype(str).str.lower().str.contains(query)
        result_df = df[mask]
    else:
        if mode == 'recent':
            result_df = df.sample(n=min(6, len(df)))
        else:
            result_df = df.head(50)

    output = []
    for _, row in result_df.iterrows():
        name = row.get('식품명')
        if pd.isna(name):
            name = row.get('대표식품명', '이름 없음')
        cat = row.get('식품대분류명')
        if pd.isna(cat):
            cat = row.get('대표식품명', '분류 없음')
        kcal = row.get('열량', 0)

        output.append({
            'name': str(name),
            'cat': str(cat),
            'kcal': int(kcal) if pd.notna(kcal) else 0
        })

    return jsonify(output[:30])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)