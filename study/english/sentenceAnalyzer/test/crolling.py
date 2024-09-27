import requests
from bs4 import BeautifulSoup

# 검색할 단어
word = 'example'
url = f'https://www.merriam-webster.com/dictionary/{word}'

# GET 요청
response = requests.get(url)

# 응답이 정상인지 확인
if response.status_code == 200:
    # HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 품사 찾기
    parts_of_speech = soup.select('h2 > a.important-blue-link') # 품사 CSS 선택자
    
    # 정의 찾기
    definitions = soup.select('.vg .dtText')  # 정의 CSS 선택자
    
    # 형태 찾기
    forms = soup.select('#dictionary-entry-1 > div.row.headword-row.header-ins > div > span > .if')
    
    if parts_of_speech and definitions:
        for part_of_speech in parts_of_speech:
          print(f'{word}의 품사: {part_of_speech.get_text(strip=True)}')
        print('정의:')
        for definition in definitions:
            print(f'- {definition.get_text(strip=True)[1:]}')
        for form in forms:
          print(f'형태: {form.get_text(strip=True)}')
    else:
        print('정보를 찾을 수 없습니다.')
else:
    print('웹페이지를 가져오는 데 실패했습니다.')
