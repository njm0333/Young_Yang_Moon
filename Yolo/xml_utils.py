# -*-coding:utf-8-*-
import os
import pandas as pd
from xml.etree.ElementTree import Element, SubElement, ElementTree

def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def load_food_name_map(csv_path="../Fooddata/code_foodname.csv"):
    food_map = {}
    if not os.path.exists(csv_path):
        print(f"⚠️ 경고: {csv_path} 파일을 찾을 수 없어 한글 이름 매핑을 생략합니다.")
        return food_map

    try:
        try:
            df = pd.read_csv(csv_path, encoding='cp949', dtype=str)
        except UnicodeDecodeError:
            df = pd.read_csv(csv_path, encoding='utf-8-sig', dtype=str)

        code_col = 'food_code' if 'food_code' in df.columns else df.columns[0]
        name_col = 'food_name' if 'food_name' in df.columns else df.columns[1]

        for _, row in df.iterrows():
            code_str = str(row[code_col]).strip()
            name_str = str(row[name_col]).strip()

            if code_str.endswith('.0'):
                code_str = code_str[:-2]

            if code_str.isdigit() and len(code_str) < 8:
                code_str = code_str.zfill(8)

            food_map[code_str] = name_str

        print(f"📊 [DB 로드 성공] 총 {len(food_map)}종의 한식 이름 매핑 데이터셋 동기화 완료.")

    except Exception as e:
        print(f"⚠️ 경고: 음식 리스트 CSV 파싱 중 오류 발생: {e}")

    return food_map

def build_and_save_xml(out_folder, file_path, save_path, detections, names, food_map):
    root = Element('annotation')
    SubElement(root, 'folder').text = str(out_folder)
    SubElement(root, 'filename').text = str(file_path)
    SubElement(root, 'path').text = str(save_path)

    valid_object_count = 0

    for *xyxy, conf, cls in reversed(detections):
        current_code = names[int(cls)]

        if current_code == "00000000":
            continue

        real_food_name = food_map.get(current_code, "Unknown_Food")

        xmin = str(int(xyxy[0]))
        ymin = str(int(xyxy[1]))
        xmax = str(int(xyxy[2]))
        ymax = str(int(xyxy[3]))

        object_xml = SubElement(root, 'object')
        SubElement(object_xml, 'name').text = current_code
        SubElement(object_xml, 'food_name').text = real_food_name

        bndbox = SubElement(object_xml, 'bndbox')
        SubElement(bndbox, 'xmin').text = xmin
        SubElement(bndbox, 'ymin').text = ymin
        SubElement(bndbox, 'xmax').text = xmax
        SubElement(bndbox, 'ymax').text = ymax

        valid_object_count += 1

    if valid_object_count > 0:
        indent(root)
        tree = ElementTree(root)
        tree.write(save_path[:save_path.rfind('.')] + '.xml', encoding='utf-8', xml_declaration=True)
        return True
    return False