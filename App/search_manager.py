# -*-coding:utf-8-*-
import pandas as pd

def filter_food_search(query, mode, food_df, processed_df):
    """
    🔍 [실시간 종목 검색 연산 엔진]
    app.py에서 메모리에 올려둔 대용량 데이터프레임을 받아 조건별로 필터링합니다.
    """
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
        return []

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

    return output[:30]