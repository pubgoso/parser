from pip._vendor import requests
from bs4 import BeautifulSoup


def request(url):
    try:
        head={
            'Host': 'codeforces.com',
        }
        response=requests.get(url,headers=head)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None

url='http://codeforces.com/submissions/wzh520wzh/page/1'
html=request(url)
soup=BeautifulSoup(html,'lxml')
temp=soup.find(class_='status-frame-datatable').find_all('tr')

for item in temp:
    print(item.find(class_='verdict-accepted').string)