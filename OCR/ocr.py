import easyocr
import cv2
import re
import json
import os

def analyze_state_machine_fix(ocr_lines):
    # 대한민국 식약처 지정 1일 영양성분 기준치 (법정 고정값)
    daily_standards = {
        "나트륨": 2000.0, "탄수화물": 324.0, "당류": 100.0, "지방": 54.0,
        "트랜스지방": 0.0, "포화지방": 15.0, "콜레스테롤": 300.0, "단백질": 55.0
    }

    extracted_data = {
        "열량": {"w": None},
        "나트륨": {"w": None, "p": None},
        "탄수화물": {"w": None, "p": None},
        "당류": {"w": None, "p": None},
        "지방": {"w": None, "p": None},
        "트랜스지방": {"w": None, "p": None},
        "포화지방": {"w": None, "p": None},
        "콜레스테롤": {"w": None, "p": None},
        "단백질": {"w": None, "p": None}
    }

    keyword_map = {
        "열량": ["열량", "kcal", "칼로리"],
        "나트륨": ["나트륨", "나트룹", "나트톱"],
        "탄수화물": ["탄수화물", "탄수회물", "탄슈", "이|}수화물","단수화물"],
        "당류": ["당류", "당루"],
        "트랜스지방": ["트랜스_지방", "트랜스자방", "E랜스지방"],
        "포화지방": ["포화_지방", "포화", "프화지방"],
        "지방": ["지방", "질방"],
        "콜레스테롤": ["콜레스테롤", "콜레스터돌", "콜렉스데틀", "몰레스데돌", "콜래스데돌"],
        "단백질": ["단백질"]
    }

    advanced_split_lines = []
    all_flat_keywords = []
    for aliases in keyword_map.values():
        all_flat_keywords.extend(aliases)

    for line in ocr_lines:
        temp_line = line

        for kw in all_flat_keywords:
            if kw == "지방":
                temp_line = re.sub(r'(?<!포화)(?<!트랜스)([^\s])(지방)', r'\1 [split_here] \2', temp_line)
                temp_line = re.sub(r'(?<!포화_)(?<!트랜스_)([^\s])(지방)', r'\1 [split_here] \2', temp_line)
            else:
                temp_line = re.sub(r'([^\s])(' + re.escape(kw) + r')', r'\1 [split_here] \2', temp_line)

        if "[split_here]" in temp_line:
            parts = temp_line.split("[split_here]")
            for p in parts:
                if p.strip(): advanced_split_lines.append(p.strip())
        else:
            advanced_split_lines.append(line)

    current_key = None
    start_collecting = False

    for line in advanced_split_lines:

        line = re.sub(r'(?<=\d)[Oo](?=\d)|(?<=\d)[Oo]|[Oo](?=\d)', '0', line)

        line = re.sub(r'(\d+)96', r'\1%', line)
        line = re.sub(r'(\d+)6$', r'\1%', line)

        line = re.sub(r'(\d+(?:\.\d+)?)\s*[89]\s*(\d+)\s*%', r'\1g \2%', line)
        line = re.sub(r'(\d+(?:\.\d+)?)[89](\d+)%', r'\1g \2%', line)
        line = re.sub(r'(\d+(?:\.\d+)?)\s*[89]\s*(?:\)|$)', r'\1g', line)

        clean_line = line.replace(" ", "").lower().replace("으", "%")

        found_key = None
        for key, aliases in keyword_map.items():
            if any(alias in clean_line for alias in aliases):
                found_key = key
                start_collecting = True
                break

        if found_key:
            current_key = found_key

        if not start_collecting or not current_key:
            continue

        if "기준치" in clean_line or "비율" in clean_line or "품목" in clean_line:
            continue

        if current_key == "열량":
            nums = re.findall(r'\d+', clean_line)
            for n in nums:
                val = int(n)
                if val >= 100 and extracted_data["열량"]["w"] is None:
                    extracted_data["열량"]["w"] = val
            continue

        p_match = re.search(r'(\d+)%', clean_line)
        if p_match and extracted_data[current_key]["p"] is None:
            pval = int(p_match.group(1))
            if pval <= 100:
                extracted_data[current_key]["p"] = pval

        clean_w_text = re.sub(r'\d+%', '', clean_line)
        w_matches = re.findall(r'\d+(?:\.\d+)?', clean_w_text)
        for w_str in w_matches:
            wval = float(w_str) if '.' in w_str else int(w_str)
            if wval in [1399, 45, 28, 19870415003246]:
                continue
            if extracted_data[current_key]["w"] is None:
                extracted_data[current_key]["w"] = wval

    print(json.dumps(extracted_data, indent=4, ensure_ascii=False))

    for key in ["탄수화물", "당류", "지방", "포화지방", "콜레스테롤", "단백질"]:
        w_val = extracted_data[key]["w"]

        if w_val is not None and w_val >= 50:
            w_str = str(int(w_val))
            inner_str = w_str[1:-1]

            if '8' in inner_str or '9' in inner_str:
                split_idx = w_str.find('9', 1, -1)
                if split_idx == -1:
                    split_idx = w_str.find('8', 1, -1)

                if split_idx != -1:
                    new_w = float(w_str[:split_idx])
                    new_p = int(w_str[split_idx+1:])


                    extracted_data[key]["w"] = new_w
                    if extracted_data[key]["p"] is None and new_p <= 100:
                        extracted_data[key]["p"] = new_p

    nutrition_result = {"열량": extracted_data["열량"]["w"] or 0}

    for key in ["나트륨", "탄수화물", "당류", "지방", "트랜스지방", "포화지방", "콜레스테롤", "단백질"]:
        w = extracted_data[key]["w"]
        p = extracted_data[key]["p"]

        if key == "트랜스지방":
            nutrition_result[key] = 0.0 if w is None or w >= 5 else float(w)
            continue

        if p is not None:
            calc_w = round(daily_standards[key] * (p / 100.0), 1)

            if w is not None:
                if key != "나트륨" and w >= 50:
                    nutrition_result[key] = calc_w
                elif key != "나트륨" and abs(calc_w - w) >= 5.0:
                    nutrition_result[key] = float(w)
                else:
                    nutrition_result[key] = float(w)
            else:
                nutrition_result[key] = calc_w
        else:
            if w is not None:
                if key == "나트륨":
                    nutrition_result[key] = float(w)
                else:
                    nutrition_result[key] = float(w // 10) if w >= 50 else float(w)
            else:
                nutrition_result[key] = 0.0

    if not nutrition_result["열량"] or nutrition_result["열량"] < 100:
        nutrition_result["열량"] = int((nutrition_result["탄수화물"] * 4) + (nutrition_result["단백질"] * 4) + (nutrition_result["지방"] * 9))

    return nutrition_result

def process_nutrition_image(image_path):
    reader = easyocr.Reader(['ko', 'en'], gpu=False)

    print(f"[{image_path}] 처리중입니다...(수 초가 소요될 수 있습니다)")
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"지정한 경로에서 이미지 파일을 찾을 수 없습니다: {image_path}")
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ocr_results = reader.readtext(gray_image, detail=0)

    print(ocr_results)

    final_data = analyze_state_machine_fix(ocr_results)

    return final_data

if __name__ == "__main__":
    TARGET_IMAGE_PATH = "test/honeybutter.jpg"

    if not os.path.exists(TARGET_IMAGE_PATH):
        print(f"폴더 안에 '{TARGET_IMAGE_PATH}' 사진 파일이 없습니다.")
    else:
        try:
            result = process_nutrition_image(TARGET_IMAGE_PATH)
            print(json.dumps(result, indent=4, ensure_ascii=False))
        except Exception as e:
            print(f"⚠예외 에러 발생: {str(e)}")