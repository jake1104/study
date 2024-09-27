from sanic import Sanic, response
import spacy

app = Sanic(__name__)

# SpaCy 영어 모델 로드
nlp = spacy.load('en_core_web_sm')

def analyze_sentence_structure(sentence):
    # 문장을 SpaCy로 처리
    doc = nlp(sentence)

    # 문장 구조 분석
    structure = {
        'S': False,
        'V': False,
        'O': False,
        'C': False,
        'IO': False,
        'DO': False,
    }
    
    for token in doc:
        if token.pos_ == 'VERB':  # 동사
            structure['V'] = True
        elif token.pos_ in ['NOUN', 'PROP', 'PROPN']:  # 명사 또는 대명사
            if structure['V']:  # 동사 뒤에 나오면 목적어로 간주
                if structure['O']:
                    structure['IO'] = True
                    structure['DO'] = True
                else:
                    structure['O'] = True
            else:  # 동사 앞에 나오면 주어로 간주
                structure['S'] = True
        elif token.pos_ in ['ADJ']:  # 형용사
            structure['C'] = True  # 보어로 간주

    # 문장 형식 결정
    if structure['S'] and structure['V']:
        if structure['C'] and structure['O']:
            return 5  # 주어 + 동사 + 목적어 + 보어
        elif structure['C']:
            return 2  # 주어 + 동사 + 보어
        elif structure['O']:
            if structure['DO'] and structure['IO']:
                return 4  # 주어 + 동사 + 간접목적어 + 직접목적어
            return 3  # 주어 + 동사 + 목적어
        return 1  # 주어 + 동사
    return 0  # 불확실

def determine_structure(docs, sentence):
    # 문장 성분의 이름을 지정하기 위한 함수
    structure = []
    has_do = False
    has_io = False
    has_s = False
    has_v = False
    has_o = False
    
    a = analyze_sentence_structure(sentence)
    
    for token in docs:
        if token.pos_ == 'VERB':  # 동사
            structure.append([token.text, 'V'])
            has_v = True
        elif token.pos_ == 'AUX':
            structure.append([token.text, '보조 동사'])
        elif token.pos_ in ['NOUN', 'PRON', 'PROPN']:  # 명사
            if has_s:
                if a == 4:
                    if has_do:
                        structure.append([token.text, 'DO'])
                    else:
                        structure.append([token.text, 'IO'])
                        has_do = True  # 직접목적어가 존재함
                else:
                    structure.append([token.text, 'O'])
                    has_o = True
            else:
                structure.append([token.text, 'S'])
                has_s = True
        elif token.pos_ == 'ADJ':  # 형용사
            if a == 2:
                if has_s:
                    structure.append([token.text, 'SC'])
                else:
                    structure.append([token.text, 'a'])
            elif a == 5:
                if has_o:
                    structure.append([token.text, 'OC'])
                elif not has_s:
                    structure.append([token.text, 'a'])
                elif has_s and not has_o:
                    structure.append([token.text, 'a'])
            else:
                structure.append([token.text, 'a'])
        elif token.pos_ == 'ADV':  # 부사
            structure.append([token.text, '부사구'])
        elif token.pos_ == 'ADP':  # 전치사
            structure.append([token.text, '전치사구'])
        else:
            structure.append([token.text, token.pos_])
            
    print(structure)
    
    return structure

@app.route('/')
async def index(request):
    return response.html('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>영어 문장 분석기</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 20px;
            }
            h1 {
                color: #333;
            }
            form {
                background: #fff;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }
            textarea {
                width: 100%;
                padding: 10px;
                margin-top: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
                resize: none;
            }
            button {
                background-color: #5cb85c;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background-color: #4cae4c;
            }
            #result {
                margin-top: 20px;
                font-size: 1.2em;
                color: #555;
            }
            #inputDisplay {
                margin-top: 20px;
                font-size: 1.1em;
                color: #333;
            }
            .word-role {
                display: inline-block;
                margin: 10px;
                text-align: center;
            }
            .word {
                text-decoration: underline;
                font-weight: bold;
            }
            .role {
                font-size: 0.9em;
                color: #777;
            }
            .pos {
                font-size: 0.9em;
                color: #777;
            }
        </style>
    </head>
    <body>
        <h1>영어 문장 분석기</h1>
        <form id="sentenceForm">
            <textarea id="sentenceInput" rows="4" placeholder="문장을 입력하세요..."></textarea><br>
            <button type="submit">분석하기</button>
        </form>
        <div id="inputDisplay"></div>
        <div id="result"></div>

        <script>
            document.getElementById('sentenceForm').addEventListener('submit', async function(event) {
                event.preventDefault();
                const sentence = document.getElementById('sentenceInput').value;

                // 입력된 문장을 아래에 표시
                document.getElementById('inputDisplay').innerText = sentence;

                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ sentence })
                });
                const result = await response.json();
                document.getElementById('result').innerHTML = result.wordsWithRoles.map(w => 
                    `<div class="word-role">
                        <div class="role">${w.role}</div>
                        <span class="word">${w.word}</span><br>
                        <div class="pos">${w.pos}</div>
                    </div>`
                )
            });
        </script>
    </body>
    </html>
    ''')

@app.route('/analyze', methods=['POST'])
async def analyze(request):
    sentence = request.json.get('sentence')
    # SpaCy를 사용하여 단어와 품사 태깅
    doc = nlp(sentence)
    
    # 문장 구조 판단
    structure = determine_structure(doc, sentence)

    # 결과를 리스트 형태로 변환
    words_with_roles = [{'word': doc[i].text, 'role': str(doc[i].pos_), 'pos': structure[i][1]} for i in range(len(doc))]
    
    print(doc)
    print(structure)
    print(words_with_roles)

    return response.json({'wordsWithRoles': words_with_roles, 'structure': structure})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
