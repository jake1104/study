from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze')
def analyze():
    word = request.args.get('word')
    if not word:
        return jsonify({"error": "단어가 제공되지 않았습니다."})

    url = f"https://dictionary.example.com/{word}"  # 사용할 사전의 URL로 변경
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # 필요한 정보를 크롤링하기 (예시: 의미)
        meaning = soup.find('div', class_='meaning')  # 해당 HTML 구조에 맞게 조정 필요
        if meaning:
            return jsonify({"word": word, "meaning": meaning.text.strip()})
        else:
            return jsonify({"error": "단어의 의미를 찾을 수 없습니다."})
    else:
        return jsonify({"error": "단어를 찾을 수 없습니다."})

if __name__ == '__main__':
    app.run(debug=True)
