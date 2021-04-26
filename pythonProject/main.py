import lxml
import xlwt
from bs4 import BeautifulSoup
from pip._vendor import requests


def request(url):
    try:

        head = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Host': 'movie.douban.com',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15'}
        response = requests.get(url, headers=head)
        print(response.status_code)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


def main(page):
    url = 'https://movie.douban.com/top250?start=' + str(page) + '&filter='
    html = request(url)
    soup = BeautifulSoup(html, 'lxml')
    temp = soup.find(class_='grid_view').find_all('li')
    return temp


book = xlwt.Workbook(encoding='utf-8', style_compression=0)

sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)
sheet.write(0, 0, '名称')
sheet.write(0, 1, '图片')
sheet.write(0, 2, '排名')
sheet.write(0, 3, '评分')
sheet.write(0, 4, '作者')
sheet.write(0, 5, '简介')

n = 1
for x in range(0, 10):
    temp = main(x * 25)
    for item in temp:
        item_name = item.find(class_='title').string
        item_img = item.find('a').find('img').get('src')
        item_index = item.find(class_='').string
        item_score = item.find(class_='rating_num').string
        item_author = item.find('p').text
        item_intr = item.find(class_='inq')
        if item_intr is not None:
            inter = item.find(class_='inq').string
        else:
            inter = ''
        print('爬取电影：' + item_index + ' | ' + item_name + ' | ' + item_score + ' | ' + inter)
        sheet.write(n, 0, item_name)
        sheet.write(n, 1, item_img)
        sheet.write(n, 2, item_index)
        sheet.write(n, 3, item_score)
        sheet.write(n, 4, item_author)
        sheet.write(n, 5, inter)
        n += 1
book.save(u'test.xls')
