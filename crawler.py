import requests
from bs4 import BeautifulSoup as bs
import threading
import queue

class Crawler(threading.Thread):
    headers = {
            'user-agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 75.0.3770.142Safari / 537.36',
            'Upgrade-Insecure-Requests': '1',
            'Host': 'www.lottery.gov.cn'
        }

    def __init__(self):
        '''

        :param urls: url队列。
        :param results: 结果队列
        '''
        super().__init__()
        self.urls = queue.Queue()
        self.results = queue.Queue()

    def run(self):
        while True:
            if not self.urls.empty():
                url = self.urls.get()
                one_result = self.crawl(url)
                self.results.put(one_result)
                print("url {} 爬取完成".format(url))
                print(one_result)
            else:
                print("所有连接爬取完成")
                break

    def crawl(self, url):
        r = requests.get(url, headers=self.headers)
        text = bs(r.text, "lxml")
        result = text.find_all('div',class_='result' )
        result = result[0].find_all('tbody')
        result = result[0].find_all('td')
        result_list = []
        for item in result:
            result_list.append(item.get_text())
        # print(result_list)
        # print(result_list[19])
        one_page = []
        one_page.append([result_list[19]] + result_list[0:8])
        # print(one_page)
        # print("len:{}".format(len(result_list)))
        for i in range(1,20):
            # print("i:{}".format(i))
            open_data = result_list[19+ (20*i)]
            number_list = result_list[20 + (20 * (i - 1)):21 + (20 * (i - 1)) + 7]
            one_page.append([open_data] + number_list)
            # print(open_data)
        return one_page

    def dumpToFile(self, filename):
        '''
        把数据写入到文件
        :return:
        '''
        with open(filename, 'w') as f:
            while not self.results.empty():
                for one in self.results.get():
                    one_line = ''
                    for item in one:
                        one_line += item
                    f.write(one_line+'\n')

    def put(self, url):
        if not self.baseUrl:
            raise Exception('baseUrl不能为空，要先进行设置')
        realUrl = self.baseUrl.format(url)
        self.urls.put(realUrl)


    def setBaseUrl(self, baseUrl):
        self.baseUrl = baseUrl

if __name__ == '__main__':
    c = Crawler()
    c.setBaseUrl('https://www.lottery.gov.cn/historykj/history_{}.jspx?_ltype=dlt')
    c.put(1)
    c.start()
    c.join()
    c.dumpToFile('daletou_history.txt')


