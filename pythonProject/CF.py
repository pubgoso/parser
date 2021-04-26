import datetime

from pip._vendor import requests

from bs4 import BeautifulSoup

ListOfName = []


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


def get_interval(day):  # 获取日期
    localtime = datetime.date.today()
    pre_time = localtime - datetime.timedelta(days=day)
    return pre_time


def query(userName, page):
    url = 'http://codeforces.com/submissions/' + userName + '/page/' + str(page)
    html = request(url)
    soup = BeautifulSoup(html, 'lxml')
    temp = soup.find(class_='status-frame-datatable').find_all('tr')
    ac = 0
    tot = 0
    for item in temp:  # 统计当前页的提交次数 和ac数
        tot += 1
        if item.find(class_='verdict-accepted') is not None:  # ac
            ac += 1

    return tot, ac


def get_max_page(userName, index):  # 获取最大的页
    url = 'http://codeforces.com/submissions/' + userName + '/page/' + str(index)
    html = request(url)
    soup = BeautifulSoup(html, 'lxml')
    page = 0
    temp = soup.find_all(class_='page-index')
    for item in temp:
        if item.find('a') is not None:
            page = max(page, int(item.find('a').string))

    return page


def find_all_user():  # 获取需要的用户信息 这里选择一个organization了
    url = 'http://codeforces.com/ratings/organization/21265'
    html = request(url)
    soup = BeautifulSoup(html, 'lxml')

    vector = soup.find(class_='datatable ratingsDatatable').find_all(class_='rated-user user-cyan')
    for item in vector:
        ListOfName.append(item.string)
    vector = soup.find(class_='datatable ratingsDatatable').find_all(class_='rated-user user-green')
    for item in vector:
        ListOfName.append(item.string)
    vector = soup.find(class_='datatable ratingsDatatable').find_all(class_='rated-user user-gray')
    for item in vector:
        ListOfName.append(item.string)
    vector = soup.find(class_='datatable ratingsDatatable').find_all(class_='rated-user user-blue')
    for item in vector:
        ListOfName.append(item.string)


def solve():
    for item in ListOfName:
        max_page = get_max_page(item, 1)
        tot = 0
        ac = 0
        for i in range(1, max_page + 1):
            (x, y) = query(item, i)
            tot += x
            ac += y
        if tot == 0:
            print(item + '共提交' + str(tot) + '次' + ' ;通过 ' + str(ac) + '次 ; ' + '正确率为: ' + ' 0.00% ')
        else:
            print(item + '共提交' + str(tot) + '次' + ' ;通过 ' + str(ac) + '次 ; ' + '正确率为: ' + str(
                round(ac / tot, 4) * 100) + ' % ')


find_all_user()
solve()
