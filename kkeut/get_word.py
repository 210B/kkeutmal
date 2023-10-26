from flask import request, json
import random


def findword(query):

    query = query
    # API 요청 보내기
    url = "https://stdict.korean.go.kr/api/search.do"
    params = {
        "certkey_no": "6091",
        "key": "",
        "type_search": "word",
        "req_type": "json",
        "q": query,
        "start": 3,
        "advanced": "y",
        "target": 1,
        "method": "start",
        "type1": "word",
        "pos": 1,
        "letter_s": 3,
        "letter_e": 5
    }
    response = request.get(url, params=params)

    # JSON 응답 파싱
    if response.status_code == 200:
        data = response.json()  # JSON 데이터 파싱
        items = data.get("channel", {}).get("item", [])  # item 키에서 데이터 가져오기

        # 단어 출력
        word_list = []
        for item in items:
            word = item.get("word", "")
            # "-" 문자 제거
            word = word.replace("-", "")
            word_list.append(word)

        print("단어 목록:", word_list)

        # 랜덤으로 단어 선택
        random_word = random.choice(word_list)

    else:
        print("API 요청에 실패하였습니다.")


    return random_word
