# -*-coding:utf-8-*-
import random
import time

# 📰 [MTS 영양문 거래소 전역 뉴스 레포지토리 기본 시드]
GLOBAL_NEWS_LIST = [
    {"title": '[특징주] <span class="stock-link">닭가슴살 팩</span>, 영양성분 허위 기재 의혹에 락인(Lock-in) 주주들 패닉... 하한가 추락', "time": "04:02:10", "author": "헤럴드경제"},
    {"title": '[공시] <span class="stock-link">아메리카노(003210)</span>, 단기 과열 종목 지정... 카페인 쇼크 주의보 발령', "time": "03:55:12", "author": "파이낸셜뉴스"},
    {"title": '[시황] 외국인(헬창), 프로틴 바 대량 순매수세 전환... 지방 섹터는 금일 일제히 전멸', "time": "03:14:00", "author": "조선비즈"},
    {"title": '[속보] 시험기간 야식 매수세 급증에 <span class="stock-link">짜장면(040120)</span> 거래대금 역대 최고치 경신', "time": "01:22:45", "author": "연합뉴스"}
]

def get_all_news():
    """ 현재까지 축적된 뉴스 리스트를 반환하는 함수 """
    global GLOBAL_NEWS_LIST
    return GLOBAL_NEWS_LIST

def trigger_purchase_news(food_name, kcal):
    """
    🎰 [매수 연동 뉴스 증식 엔진]
    유저가 호가창에서 매수(구매) 버튼을 누르면 이 함수를 호출하여 뉴스를 동적 생성함
    """
    global GLOBAL_NEWS_LIST
    current_time = time.strftime('%H:%M:%S', time.localtime())

    # 섭취한 칼로리 수준에 따라 Me.corp(내 지갑/신체) 주가 힌트 분기 조정
    try:
        kcal_val = int(kcal)
    except:
        kcal_val = 0

    if kcal_val >= 500:
        news1 = {
            "title": f'[특징주] 내 자산 계좌 <span class="stock-link">Me.corp</span>, 고칼로리 성분인 {food_name} 대량 매수로 지방 지수 폭등 유력... 주가 하락 압박',
            "time": current_time,
            "author": "영양일보"
        }
        news2 = {
            "title": f'[속보] 시장 감시 기구, {food_name} 과다 섭취에 따른 헤비급 자산 경보 발령... 계좌 긴급 관리 체제 돌입',
            "time": current_time,
            "author": "연합뉴스"
        }
    else:
        news1 = {
            "title": f'[호재] <span class="stock-link">Me.corp</span>, 클린 우량 식단 {food_name} 매수 체결 성공... 기초대사량 방어선 견고',
            "time": current_time,
            "author": "한국경제"
        }
        news2 = {
            "title": f'[공시] {food_name}({random.randint(100000,999999)}) 우량 영양소 검증 완료에 따라 기관 헬창 투자자들 대거 유입',
            "time": current_time,
            "author": "에프앤가이드"
        }

    # 최신 뉴스가 뉴스룸 맨 위(0번째 인덱스)에 꽂히도록 insert 처리
    GLOBAL_NEWS_LIST.insert(0, news1)
    GLOBAL_NEWS_LIST.insert(0, news2)