# -*-coding:utf-8-*-
import random
import socket
import os
import sys
import hashlib
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ====================================================================
# 🛠️ [경로 주입 및 원격 모듈 소환 파트]
# 외부 폴더(OCR, Yolo)에 있는 형의 AI 핵심 엔진들을 부품처럼 호출합니다.
# ====================================================================
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)

# OCR과 Yolo 디렉토리를 파이썬 참조 경로에 등록
ocr_folder_path = os.path.join(root_dir, 'OCR')
yolo_folder_path = os.path.join(root_dir, 'Yolo')

if ocr_folder_path not in sys.path:
    sys.path.append(ocr_folder_path)
if yolo_folder_path not in sys.path:
    sys.path.append(yolo_folder_path)

# 형이 기막히게 짜둔 OCR 메인 처리 함수 임포트
try:
    from ocr import process_nutrition_image
    print("🔤 [시스템 신호] 형의 EasyOCR 크로스체크 엔진이 백엔드에 결합되었습니다.")
except Exception as e:
    print(f"⚠️ [경고] OCR 모듈 임포트 실패 (3단계 라이브러리 설치 전 대비): {e}")

# ====================================================================
# 📊 [CSV 데이터 통합 로드 파트]
# 서버 가동 시 30MB CSV 파일들을 메모리에 미리 고속 탑재합니다.
# ====================================================================
try:
    food_df = pd.read_csv('../Fooddata/19k_food.csv', encoding='utf-8')
    processed_df = pd.read_csv('../Fooddata/27M_product.csv', encoding='utf-8')
    nutrient_df = pd.read_csv('../Fooddata/food_nutrition.csv', encoding='utf-8')
    print("\n" + "═"*60)
    print("📊 [영양문 거래소] 상장 음식/가공식품 데이터 로드 성공!")
    print(f"   • 일반 음식 데이터: {len(food_df)}개 행 로드 완료")
    print(f"   • 가공 식품 데이터: {len(processed_df)}개 행 로드 완료")
    print("═"*60 + "\n")
except Exception as e:
    print("\n" + "❌"*30)
    print(f"⚠️ [경고] CSV 상장 데이터 로드에 실패했습니다! 경로를 확인하세요: {e}")
    print("❌"*30 + "\n")
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

    acc_part1 = random.randint(1000, 9999)
    acc_part2 = random.randint(1000, 9999)

    account_types = ["위탁종합", "증권종합", "종합계좌", "MTS종합", "해외종합"]
    chosen_type = random.choice(account_types)
    full_account_name = f"{acc_part1}-{acc_part2} [{chosen_type}]"

    return redirect(url_for('universal_router', stock_name=full_stock_name, account_name=full_account_name, page='main'))

# 3. 만능 레이아웃 라우터 (MTS 프론트 연동 허브)
@app.route('/main')
def universal_router():
    stock_name = request.args.get('stock_name', '무명주주(000000)')
    account_name = request.args.get('account_name', '0000-0000 [위탁종합]')
    target_page = request.args.get('page', 'main')

    # 1. 📈 메인 주식 주문 거래소 홈그라운드 렌더링
    if target_page == 'main':
        # 음식 이름을 기반으로 고유한 6자리 종목코드 파싱
        hash_val = int(hashlib.md5(stock_name.encode('utf-8')).hexdigest(), 16)
        stock_code = str((hash_val % 900000) + 100000)

        # 🎰 [50원 단위 난수 생성 공식 유지]
        forced_price = request.args.get('forced_price', None)
        if forced_price:
            base_price = int(forced_price)
        else:
            raw_random_price = random.randint(10000, 100000)
            base_price = (raw_random_price // 50) * 50

        # ⚡ [신규 파이프라인] search.html 수동교정창에서 넘어온 9대 영양학 스펙 가로채기
        is_ocr = request.args.get('is_ocr', 'false')

        # 주소창에서 영양 수치를 안전하게 받아 기본값 0 세팅
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

        # 중요: 계산된 주가와 함께 9대 영양스펙 묶음을 main.html로 투하바인딩!
        return render_template('main.html',
                               stock_name=stock_name,
                               stock_code=stock_code,
                               base_price=base_price,
                               account_name=account_name,
                               is_ocr=is_ocr,
                               nutrients=nutrients)

    # 2. 🔍 독립된 '종목검색' 창 서빙
    elif target_page == 'search':
        return render_template('search.html', stock_name=stock_name, account_name=account_name)

    # 3. 📰 💰 시황뉴스 및 보유자산 서빙
    return render_template(f'{target_page}.html', stock_name=stock_name, account_name=account_name)


# ====================================================================
# ⚡ [신규 추가] AI 연동 비동기 통신 비즈니스 라우터 파트
# ====================================================================

# 🔤 [트랙 B] 가공식품 전용 EasyOCR 비동기 파싱 엔진 가동 관문
@app.route('/api/upload_ocr', methods=['POST'])
def api_upload_ocr():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': '파일이 전달되지 않았습니다.'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': '선택된 사진 파일이 없습니다.'}), 400

    try:
        # 형 규칙 저격: 사진 수신 시 OCR/Images/ 폴더에 정밀 격리 저장
        save_dir = os.path.join(root_dir, 'OCR', 'Images')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        filename = secure_filename(file.filename)
        # 만약 파일명이 깨지거나 공백일 경우 대비 방어선
        if not filename or len(filename.split('.')) < 2:
            filename = f"ocr_input_{random.randint(1000, 9999)}.jpg"

        saved_image_path = os.path.join(save_dir, filename)
        file.save(saved_image_path)

        # 형의 오독 보정 상태 머신 엔진 긴급 구동!!
        final_nutrition_dto = process_nutrition_image(saved_image_path)

        # 프론트엔드 교정 모달창 인풋 필드로 데이터 바스 릴레이 수송
        return jsonify({
            'status': 'success',
            'result': final_nutrition_dto
        })

    except Exception as e:
        print(f"❌ [OCR 연동 내부 에러 발생]: {str(e)}")
        return jsonify({'status': 'error', 'message': f'AI 연산 중 장애 발생: {str(e)}'}), 500


# 📸 [트랙 A] 일반 식단 전용 YOLOv3 + ResNet 비동기 관문 (뼈대 가이드 내장)
@app.route('/api/upload_yolo', methods=['POST'])
def api_upload_yolo():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': '파일이 없습니다.'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': '파일명이 비어있습니다.'}), 400

    try:
        # 형 규칙 저격: 사진 수신 시 Yolo/Images/ 폴더에 격리 저장
        save_dir = os.path.join(root_dir, 'Yolo', 'Images')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        filename = secure_filename(file.filename)
        if not filename:
            filename = f"yolo_input_{random.randint(1000, 9999)}.jpg"

        saved_image_path = os.path.join(save_dir, filename)
        file.save(saved_image_path)

        # 🛡️ 형이 기획한 YOLO 탐지 에러/실패 시 예외 처리 마일스톤 예시 구역
        # XML 전수조사 후 실패 판정 시 -> 'YOLO_FAIL' 응답을 보내 search.html이 직접 검색 탭으로 튕기게 유도!
        """
        yolo_success, detected_food = run_yolov3_detection(saved_image_path)
        if not yolo_success:
            return jsonify({'status': 'fail', 'code': 'YOLO_FAIL', 'message': '음식을 감지하지 못했습니다.'})
        """

        return jsonify({'status': 'success', 'message': 'YOLO/ResNet 파이프라인 대기 상태 완료'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ====================================================================
# ⚡ [기존 원본 유지] 초고속 실시간 종목 검색 백엔드 API
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

    app.run(host='0.0.0.0', port=5000, debug=True)