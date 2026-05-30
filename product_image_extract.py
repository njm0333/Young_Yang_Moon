import requests
from io import BytesIO
from PIL import Image
from duckduckgo_search import DDGS

def get_small_product_image(product_name, save_filename="product_img.jpg", max_size=(300, 300)):
    """
    제품 이름을 검색하여 작은 사이즈의 이미지를 다운로드하고 저장하는 함수
    """
    print(f"[{product_name}] 이미지를 검색 중입니다...")

    # 최신 버전 라이브러리 기준 수정 (with DDGS() 사용 및 키워드 인자 제거)
    try:
        with DDGS() as ddgs:
            # max_results 대신 라이브러리 내부에서 순회할 수 있도록 generator를 반환하므로,
            # 검색 후 첫 번째 결과만 가져오도록 수정했습니다.
            results = [r for r in ddgs.images(product_name)]
    except Exception as e:
        print(f"❌ 검색 중 오류가 발생했습니다: {e}")
        return

    if not results:
        print("❌ 이미지를 찾을 수 없습니다.")
        return

    # 첫 번째 검색 결과의 이미지 URL 가져오기
    image_url = results[0]['image']
    print(f"🔗 이미지 URL 발견: {image_url}")

    try:
        # 2. 이미지 다운로드
        response = requests.get(image_url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()

        # 3. 이미지를 메모리에 열고 크기 조절
        img = Image.open(BytesIO(response.content))
        img.thumbnail(max_size)

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # 4. 이미지 저장
        img.save(save_filename, format="JPEG")
        print(f"✅ 이미지가 성공적으로 저장되었습니다!")
        print(f"📁 파일명: {save_filename} / 최종 크기: {img.size}")

    except requests.exceptions.RequestException as e:
        print(f"❌ 이미지를 다운로드하는 중 네트워크 오류가 발생했습니다: {e}")
    except Exception as e:
        print(f"❌ 이미지 처리 중 오류가 발생했습니다: {e}")

# --- 실행 예시 ---
if __name__ == "__main__":
    search_query = input("검색할 제품 이름을 입력하세요: ")
    # 파일명에 공백이나 특수문자가 들어갈 수 있으므로 안전하게 저장
    safe_filename = "".join([c for c in search_query if c.isalpha() or c.isdigit() or c==' ']).rstrip()
    get_small_product_image(search_query, save_filename=f"{safe_filename}.jpg")