import requests
from bs4 import BeautifulSoup as bs
import threading
import queue

from collections import Counter
from pyecharts.charts import Bar,Page
from pyecharts import options as opts

from sklearn import svm

def forecast():
    data=[]
    period=[]
    first_num=[]
    second_num=[]
    third_num=[]
    fourth_num=[]
    fifth_num=[]
    sixth_num=[]
    seventh_num=[]

    with open('history.txt', 'r') as  f:
        for i in range(1860):
            oneLine_data = f.readline().strip()
            data.append(int(oneLine_data[0:10].replace('-','')))
            period.append(int(oneLine_data[10:15]))
            first_num.append(int(oneLine_data[15:17]))
            second_num.append(int(oneLine_data[17:19]))
            third_num.append(int(oneLine_data[19:21]))
            fourth_num.append(int(oneLine_data[21:23]))
            fifth_num.append(int(oneLine_data[23:25]))
            sixth_num.append(int(oneLine_data[25:27]))
            seventh_num.append(int(oneLine_data[27:29]))
    # print(data)
    # print(period)
    # print(first_num)
    # print(second_num)
    # print(third_num)
    # print(fourth_num)
    # print(fifth_num)
    # print(sixth_num)
    # print(seventh_num)
    x=[]
    for j in range(len(data)):
        x.append([data[j],period[j]])

    first_model=svm.SVR(gamma='auto')
    second_model=svm.SVR(gamma='auto')
    third_model=svm.SVR(gamma='auto')
    fourth_model=svm.SVR(gamma='auto')
    fifth_model=svm.SVR(gamma='auto')
    sixth_model=svm.SVR(gamma='auto')
    seventh_model=svm.SVR(gamma='auto')
    model_list=[first_model,second_model,third_model,fourth_model,fifth_model,sixth_model,seventh_model]
    y_list=[first_num,second_num,third_num,fourth_num,fifth_num,sixth_num,seventh_num]
    for k in range(7):
        model_list[k].fit(x,y_list[k])
    res_list=[]
    for model in model_list:
        res=model.predict([[20190803,19089]]).tolist()
        res_list.append(res)

    print(res_list)
    #res=first_model.predict([[20190729,19087]])
    #print(res)


def number_analyse():
    red_balls = []
    blue_balls = []
    with open('history.txt', 'r') as  f:
        for i in range(1860):
            oneLine_data = f.readline().strip()
            red_balls.extend([int(oneLine_data[15 + (2 * i):15 + (2 * (i + 1))]) for i in range(5)])
            blue_balls.append(int(oneLine_data[-4:-2]))
            blue_balls.append(int(oneLine_data[-2:]))

    red_counter = Counter(red_balls)
    blue_counter = Counter(blue_balls)
    print(red_balls)
    print(blue_balls)
    print(red_counter)
    print(blue_counter)
    print(red_counter.most_common())
    print(blue_counter.most_common())
    red_dict={}
    blue_dict={}
    for i in red_counter.most_common():#使用collections模块的counter统计红球和蓝球各个号码的出现次数
        red_dict['{}'.format(i[0])]=i[1]
    for j in blue_counter.most_common():
        blue_dict['{}'.format(j[0])]=j[1]

    print(red_dict)
    print(blue_dict)

    red_list=sorted(red_counter.most_common(),key=lambda number:number[0])#对红蓝球号码和次数重新进行排序
    blue_list=sorted(blue_counter.most_common(),key=lambda number:number[0])
    print(red_list)
    print(blue_list)

    red_bar=Bar()
    red_x=['{}'.format(str(x[0])) for x in red_list]
    red_y=['{}'.format(str(x[1])) for x in red_list]
    red_bar.add_xaxis(red_x)
    red_bar.add_yaxis('红色球出现次数',red_y)
    red_bar.set_global_opts(title_opts=opts.TitleOpts(title='大乐透彩票',subtitle='近12年数据'),toolbox_opts=opts.ToolboxOpts()
                            ,yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}/次")),
                            xaxis_opts=opts.AxisOpts(name='开奖号码'))
    red_bar.set_series_opts(markpoint_opts=opts.MarkPointOpts(
        data=[opts.MarkPointItem(type_='max',name='最大值'),opts.MarkPointItem(type_='min',name='最小值')]
    ))


    blue_bar=Bar()
    blue_x=['{}'.format(str(x[0])) for x in blue_list]
    blue_y=['{}'.format(str(x[1])) for x in blue_list]
    blue_bar.add_xaxis(blue_x)
    blue_bar.add_yaxis('蓝色球出现次数',blue_y,itemstyle_opts=opts.ItemStyleOpts(color='blue'))
    blue_bar.set_global_opts(title_opts=opts.TitleOpts(title='大乐透彩票',subtitle='近12年数据'),toolbox_opts=opts.ToolboxOpts()
                            ,yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}/次")),
                            xaxis_opts=opts.AxisOpts(name='开奖号码'))
    blue_bar.set_series_opts(markpoint_opts=opts.MarkPointOpts(
        data=[opts.MarkPointItem(type_='max',name='最大值'),opts.MarkPointItem(type_='min',name='最小值')]
    ))

    page=Page(page_title='大乐透历史开奖数据分析',interval=3)
    page.add(red_bar,blue_bar)
    page.render('大乐透历史开奖数据分析.html')


class get_history(threading.Thread):
    def __init__(self,task_q,result_q):
        super().__init__()
        self.task_queue=task_q
        self.result_queue=result_q


    def run(self):
        while True:
            if not self.task_queue.empty():
                page=self.task_queue.get()
                one_result=self.crawl(page)
                self.result_queue.put(one_result)
                self.task_queue.task_done()
                print('##第{}页爬取完毕~~~~~'.format(page))
            else:
                break


    def crawl(self,page):
        url = 'http://www.lottery.gov.cn/historykj/history_{}.jspx?_ltype=dlt'.format(page)
        headers = {
            'user-agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 75.0.3770.142Safari / 537.36',
            'Upgrade-Insecure-Requests': '1',
            'Host': 'www.lottery.gov.cn'
        }
        r = requests.get(url, headers=headers)
        text = bs(r.text, 'lxml')
        result = text.find_all('div', class_='result')
        result = result[0].find_all('tbody')
        result = result[0].find_all('td')
        result_list = []
        for item in result:
            result_list.append(item.get_text())
        one_page=[]
        one_page.append([result_list[19]] + result_list[0:8])
        for i in range(1, 20):
            open_data = result_list[19 + (20 * i)]
            number_list = result_list[20 + (20 * (i - 1)):21 + (20 * (i - 1)) + 7]
#            print([open_data] + number_list)
            one_page.append([open_data] + number_list)
        return one_page

def get_history():
    task_queue=queue.Queue()
    result_queue=queue.Queue()
    for i in range(1,94):
        task_queue.put(i)


    crawl=get_history(task_queue,result_queue)
    crawl.setDaemon(True)
    crawl.start()

    task_queue.join()



    with open('history.txt','a') as f :

        while not result_queue.empty():
            for one in result_queue.get():
                one_line=''
                for item in one:
                    one_line+=item
                f.write(one_line+'\n')
if __name__ == '__main__':
    # get_history()
    # number_analyse()
    forecast()
