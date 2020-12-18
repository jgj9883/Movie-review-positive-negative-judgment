import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_reple(page=1):
    url = 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=182234&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=' +str(page)
    response = requests.get(url.format(page))
    soup = BeautifulSoup(response.text, 'html.parser')
    s = []
    t = []
    for li in soup.find('div', {'class': 'score_result'}).find_all('li'):
        # print("점수:",li.em.text)
        # #print("댓글:",li.p.text.strip())
        if int(li.em.text) >= 8:
            s.append(1)
            t.append(li.p.text.replace('\n','').replace('\t','').replace('\r',''))
        elif int(li.em.text) <= 5:
            s.append(0)
            t.append(li.p.text.replace('\n','').replace('\t','').replace('\r',''))
    return s, t

score, text = [], []
for i in range(1, 350):
    print("요청 횟수 : ",i, end='\r')
    s, t = get_reple(i)
    score += s
    text += t

df = pd.DataFrame([score, text]).T
df.columns = ['score','text']
df.to_csv('test.csv')


