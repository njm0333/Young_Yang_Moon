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

from news_manager import get_all_news, generate_dynamic_combination_news
from diet_manager import calculate_diet_nutrition
from account_manager import execute_buy_order, MECORP_ASSET, get_bmi_status

app = Flask(__name__)
app.secret_key = 'young_yang_moon_secret_key'

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)

ocr_folder_path = os.path.join(root_dir, 'OCR')
yolo_folder_path = os.path.join(root_dir, 'Yolo')

if ocr_folder_path not in sys.path: sys.path.append(ocr_folder_path)
if yolo_folder_path not in sys.path: sys.path.append(yolo_folder_path)


try:
    from ocr import process_nutrition_image
    print("OCR 로딩완료.")
except Exception as e:
    print(f"⚠OCR 모듈 임포트 실패: {e}")

try:
    from detection import init_yolo_model, run_yolo_detection
    init_yolo_model()
except Exception as e:
    print(f"⚠YOLO 딥러닝 모듈 함수 링킹 실패: {e}")

try:
    food_df = pd.read_csv('../Fooddata/19k_food.csv', encoding='utf-8')
    processed_df = pd.read_csv('../Fooddata/27M_product.csv', encoding='utf-8')
    nutrient_df = pd.read_csv('../Fooddata/food_nutrition.csv', encoding='utf-8')
    nutrient_df['음 식 명'] = nutrient_df['음 식 명'].astype(str).str.strip()
except Exception as e:
    print(f"⚠CSV 상장 데이터 로드 실패: {e}")
    nutrient_df = pd.DataFrame()

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login_process', methods=['POST'])
def login_process():
    user_name = request.form.get('username', '무명주주')

    session['user_profile'] = {
        'age': int(request.form.get('age', 24)),
        'height': float(request.form.get('height', 175.0)),
        'weight': float(request.form.get('weight', 70.0)),
        'invest_type': request.form.get('invest_type', '가치투자형')
    }

    full_stock_name = f"{user_name}({random.randint(100000, 999999)})"
    full_account_name = f"{random.randint(1000, 9999)}-{random.randint(1000, 9999)} [{random.choice(['위탁종합', '증권종합', '종합계좌', 'MTS종합', '해외종합'])}]"

    return redirect(url_for('universal_router', stock_name=full_stock_name, account_name=full_account_name, page='main'))

@app.route('/main')
def universal_router():
    stock_name = request.args.get('stock_name', '무명주주(000000)')
    account_name = request.args.get('account_name', '0000-0000 [위탁종합]')
    target_page = request.args.get('page', 'main')

    hash_val = int(hashlib.md5(stock_name.encode('utf-8')).hexdigest(), 16)
    stock_code = str((hash_val % 900000) + 100000)
    base_price = int(request.args.get('forced_price', (random.randint(10000, 100000) // 50) * 50))

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

    if request.args.get('execute_trade', 'false') == 'true':
        food_title = request.args.get('food_name', stock_name)
        buy_qty = int(request.args.get('qty', 1))

        user_profile = session.get('user_profile', {'age': 24, 'height': 175.0, 'weight': 70.0, 'invest_type': '가치투자형'})
        bmi_label, _ = get_bmi_status(user_profile['height'], user_profile['weight'])

        news_keywords = execute_buy_order(food_title, buy_qty, base_price, nutrients, user_profile)
        generate_dynamic_combination_news(food_title, news_keywords, user_profile, {'bmi_label': bmi_label, 'age_label': f"{user_profile['age'] // 10 * 10}대"})

        return redirect(url_for('universal_router', stock_name=stock_name, account_name=account_name, page=target_page))

    if target_page == 'main':
        return render_template('main.html', stock_name=stock_name, stock_code=stock_code, base_price=base_price, account_name=account_name, nutrients=nutrients)
    elif target_page == 'search':
        return render_template('search.html', stock_name=stock_name, account_name=account_name)
    elif target_page == 'news':
        return render_template('news.html', stock_name=stock_name, account_name=account_name, news_list=get_all_news())
    elif target_page == 'account':
        if MECORP_ASSET.get('current_price', 0) < 1000000: MECORP_ASSET['current_price'] = 100000000.0
        return render_template('account.html', stock_name=stock_name, account_name=account_name, asset=MECORP_ASSET)

    return render_template(f'{target_page}.html', stock_name=stock_name, account_name=account_name)

@app.route('/api/upload_ocr', methods=['POST'])
def api_upload_ocr():
    if 'file' not in request.files or request.files['file'].filename == '':
        return jsonify({'status': 'error', 'message': '파일 오류'}), 400
    try:
        save_dir = os.path.join(root_dir, 'OCR', 'Images')
        os.makedirs(save_dir, exist_ok=True)
        filename = secure_filename(request.files['file'].filename) or f"ocr_{random.randint(1000, 9999)}.jpg"
        saved_path = os.path.join(save_dir, filename)
        request.files['file'].save(saved_path)
        return jsonify({'status': 'success', 'result': process_nutrition_image(saved_path), 'image_url': f"/api/ocr_image/{filename}"})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/ocr_image/<filename>')
def serve_ocr_image(filename):
    from flask import send_from_directory
    return send_from_directory(os.path.join(root_dir, 'OCR', 'Images'), filename)

@app.route('/api/upload_yolo', methods=['POST'])
def api_upload_yolo():
    if 'file' not in request.files or request.files['file'].filename == '':
        return jsonify({'status': 'error'}), 400
    try:
        save_dir = os.path.join(root_dir, 'Yolo', 'Images')
        os.makedirs(save_dir, exist_ok=True)
        filename = secure_filename(request.files['file'].filename) or f"yolo_{random.randint(1000, 9999)}.jpg"
        saved_path = os.path.join(save_dir, filename)
        request.files['file'].save(saved_path)

        xml_dir = os.path.join(root_dir, 'Yolo_output')
        yolo_success, _ = run_yolo_detection(saved_path, xml_dir)

        if not yolo_success: return jsonify({'status': 'fail', 'code': 'YOLO_FAIL'})
        return jsonify({'status': 'success', 'result': calculate_diet_nutrition(filename, xml_dir, nutrient_df), 'image_url': f"/api/yolo_image/{filename}"})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/yolo_image/<filename>')
def serve_yolo_image(filename):
    from flask import send_from_directory
    return send_from_directory(os.path.join(root_dir, 'Yolo', 'Images'), filename)

@app.route('/api/search_food')
def api_search_food():
    query = request.args.get('q', '').strip().lower()
    mode = request.args.get('mode', 'recent')

    if mode == 'food': df = food_df
    elif mode == 'processed': df = processed_df
    else: df = pd.concat([food_df, processed_df], ignore_index=True) if not food_df.empty and not processed_df.empty else food_df if not food_df.empty else processed_df

    if df.empty: return jsonify([])

    if query:
        name_s = df.get('식품명', df.get('대표식품명', pd.Series(dtype=str)))
        cat_s = df.get('식품대분류명', df.get('대표식품명', pd.Series(dtype=str)))
        mask = name_s.fillna('').astype(str).str.lower().str.contains(query) | cat_s.fillna('').astype(str).str.lower().str.contains(query)
        result_df = df[mask].head(50)
    else:
        result_df = df.head(50)

    output = []
    for _, row in result_df.iterrows():
        n1 = row.get('식품명')
        n2 = row.get('대표식품명')
        name = n1 if pd.notna(n1) and str(n1).strip().lower() != 'nan' else (n2 if pd.notna(n2) and str(n2).strip().lower() != 'nan' else '이름 없음')

        c1 = row.get('식품대분류명')
        c2 = row.get('대표식품명')
        cat = c1 if pd.notna(c1) and str(c1).strip().lower() != 'nan' else (c2 if pd.notna(c2) and str(c2).strip().lower() != 'nan' else '분류 없음')

        def clean_val(val):
            if pd.isna(val) or str(val).strip() == '-' or str(val).strip() == '' or str(val).strip().lower() == 'nan': return 0
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