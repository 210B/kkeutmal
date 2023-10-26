from flask import Flask, request, jsonify, abort, render_template
from flask import *
import json
from flask_cors import CORS, cross_origin
from kkeut.Hangulize import Hanguel
from kkeut.get_word import findword

app = Flask(__name__)
cors = CORS(app)

kkeut_log = []

lang = 'spa'


def get_next(quest):

    quest = quest
    ret_data = findword(quest)
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

    if kkeut_log:
        # 유저가 이미 답한 적 있는 답을 입력했을 때
        if quest in kkeut_log:
            ret_data = {
                "hangulize":"",
                "reply":"err1"
            }

        else:
            # 유저가 유효한 답을 입력했을 때
            if kkeut_log[-1][-1] == quest[0]:
                kkeut_log.append(quest)
                reply = get_next(quest)
                # pc가 유효한 답을 냈을 때
                if kkeut_log[-1][-1] == reply[-1]:
                    ret_data = {
                        "hangulize":quest,
                        "reply":reply
                    }
                # pc가 졌을 때
                else:
                    ret_data = {
                        "hangulize": quest,
                        "reply": reply+"\n당신의 승리입니다."
                    }
            # 유효하지 않을 때
            else:
                ret_data = {
                    "hangulize":quest,
                    "reply":"err2"
                }
    # 시작
    else:
        kkeut_log.append(quest)
        reply = get_next(quest)
        # pc가 유효한 답을 냈을 때
        if kkeut_log[-1][-1] == reply[-1]:
            ret_data = {
                "hangulize": quest,
                "reply": reply
            }
        # pc가 졌을 때
        else:
            ret_data = {
                "hangulize": quest,
                "reply": reply + "\n당신의 승리입니다."
            }

    return ret_data



# API
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = request.json
        if 'lang' in data and 'user' in data:
            lang = data['lang']
            user = data['user']
            result = get_hangulize(lang, user)
            return jsonify(result)
        else:
            return jsonify({"error": "Invalid data format."})
    else:
        return jsonify({"error": "Unsupported HTTP method."})




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)