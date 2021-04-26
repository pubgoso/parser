from pip._vendor import requests
from bs4 import BeautifulSoup


def request(address):
    try:
        head = {
            'Host': 'codeforces.com',
        }
        response = requests.get(address, headers=head)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


url = 'http://codeforces.com/submissions/wzh520wzh/page/1'
html = request(url)
soup = BeautifulSoup(html, 'lxml')
temp = soup.find(class_='status-frame-datatable').find_all('tr')

for item in temp:
    data = ''
    print(item.get_text())
    if item.find(class_='rated-user user-orange') is not None:  # username
        data += '用户名=' + item.find(class_='rated-user user-orange').get_text()
    data += ' 评测信息: '
    if item.find(class_='verdict-accepted') is not None:  # ac
        data += item.find(class_='verdict-accepted').string
    if item.find(class_='verdict-rejected') is not None:  # reject
        data += item.find(class_='verdict-rejected').get_text()
    print(data)
    # if item.find(class_='verdict-format-judged') is not None:
    #     print(item.find(class_='verdict-format-judged').get_text())
