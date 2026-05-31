# -*-coding:utf-8-*-
import os
import xml.etree.ElementTree as ET
import pandas as pd

def calculate_diet_nutrition(filename, xml_output_dir, nutrient_df):
    """
    🧠 [YOLO 결과 가공 및 영양소 계산 엔진]
    app.py에서 주차한 사진 이름을 받아 XML 파싱 및 CSV 매칭 연산을 전담합니다.
    """
    file_basename = os.path.splitext(filename)[0]
    xml_path = os.path.join(xml_output_dir, f"{file_basename}.xml")

    real_food_name = "알 수 없는 음식"
    if os.path.exists(xml_path):
        tree = ET.parse(xml_path)
        root_xml = tree.getroot()
        obj_tag = root_xml.find('object')
        if obj_tag is not None:
            fn_tag = obj_tag.find('food_name')
            if fn_tag is not None and fn_tag.text:
                real_food_name = fn_tag.text.strip()

    # ResNet 예측 등급 예시 (기본 가이드 유지)
    mock_q_level = "Q3"
    q_ratio_map = {"Q1": 0.25, "Q2": 0.50, "Q3": 0.75, "Q4": 1.00, "Q5": 1.25}
    current_ratio = q_ratio_map.get(mock_q_level, 1.00)

    final_result = {
        'food_name': real_food_name,
        'quantity_level': mock_q_level,
        '열량': 0, '탄수화물': 0, '당류': 0, '단백질': 0, '지방': 0,
        '포화지방': 0, '트랜스지방': 0, '콜레스테롤': 0, '나트륨': 0
    }

    if not nutrient_df.empty:
        matched_rows = nutrient_df[nutrient_df['음 식 명'] == real_food_name]

        if not matched_rows.empty:
            row = matched_rows.iloc[0]

            def parse_nut(val, multiplier=1.0):
                if pd.isna(val) or str(val).strip() == '-' or str(val).strip() == '':
                    return 0
                try:
                    return round(float(str(val).replace(',', '')) * multiplier, 2)
                except:
                    return 0

            base_weight = parse_nut(row.get('중량(g)', 200))
            calculated_g = round(base_weight * current_ratio, 1)

            final_result['quantity_level'] = f"{calculated_g}g"
            final_result['열량'] = int(parse_nut(row.get('에너지(kcal)'), current_ratio))
            final_result['탄수화물'] = parse_nut(row.get('탄수화물(g)'), current_ratio)
            final_result['당류'] = parse_nut(row.get('당류(g)'), current_ratio)
            final_result['단백질'] = parse_nut(row.get('단백질(g)'), current_ratio)
            final_result['지방'] = parse_nut(row.get('지방(g)'), current_ratio)
            final_result['포화지방'] = parse_nut(row.get('포화지방(g)'), current_ratio)
            final_result['트랜스지방'] = parse_nut(row.get('트랜스지방(g)'), current_ratio)
            final_result['콜레스테롤'] = int(parse_nut(row.get('콜레스테롤(mg)'), current_ratio))
            final_result['나트륨'] = int(parse_nut(row.get('나트륨(mg)'), current_ratio))

    return final_result