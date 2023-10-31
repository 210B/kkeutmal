from flask import Flask, request, jsonify, abort, render_template
from flask import *
import json
from flask_cors import CORS, cross_origin
from kkeut.Hangulize import Hanguel
from kkeut.get_word import Find
from gtts import gTTS
import os


app = Flask(__name__)
cors = CORS(app)

kkeut_log = []



def get_next(quest):

    quest = quest
    ret_data = Find.findword(quest)
    kkeut_log.append(ret_data)

    return ret_data

# user input foreign word -> hangulize
def get_hangulize(lang, user):

    # get request
    json_data = {
        'lang': lang,
        'user': user
    }

    lang = json_data['lang']
    user = json_data['user']

    # get hangulized word
    quest = Hanguel.generate_hanguel(lang,user)
    print(quest)

    if kkeut_log:
        # 유저가 이미 답한 적 있는 답을 입력했을 때
        if quest in kkeut_log:
            ret_data = {
                "hangulize": "",
                "reply": "이미 답한 적 있는 단어입니다."
            }

        else:
            # 유저가 유효한 답을 입력했을 때
            if kkeut_log[-1][-1] == quest[0]:
                kkeut_log.append(quest)
                reply = get_next(quest)
                # pc가 유효한 답을 냈을 때
                if kkeut_log[-1][-1] == reply[-1]:
                    ret_data = {
                        "hangulize": quest,
                        "reply": reply
                    }
                    kkeut_log.append(reply)
                # pc가 졌을 때
                else:
                    ret_data = {
                        "hangulize": quest,
                        "reply": reply+"\n당신의 승리입니다."
                    }
            # 유효하지 않을 때
            else:
                ret_data = {
                    "hangulize": quest,
                    "reply": "앞의 단어와 이어지는 단어를 입력해주세요."
                }
    # 시작
    else:
        kkeut_log.append(quest)
        reply = get_next(quest[-1])
        # pc가 유효한 답을 냈을 때
        if kkeut_log[-1][-1] == reply[-1]:
            ret_data = {
                "hangulize": quest,
                "reply": reply
            }
            kkeut_log.append(reply)
        # pc가 졌을 때
        else:
            ret_data = {
                "hangulize": quest,
                "reply": reply + "\n당신의 승리입니다."
            }

    return ret_data


def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    tts.save('response.mp3')


app = Flask(__name__, static_url_path='/static')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user = request.form['word']  # 사용자로부터 단어 입력 받음
        lang = 'spa'  # lang 값을 "spa"로 하드 코딩
        result = get_hangulize(lang, user)
        text_to_speech(result['reply'], "ko")  # 응답 텍스트를 음성으로 변환
        return render_template('home.html', response=result)
    else:
        # GET 요청일 때는 home.html 렌더링
        return render_template('home.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)