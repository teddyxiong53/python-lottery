from crawler import Crawler
from config import Config
from chart_presenter import ChartPresenter
from forcaster import Forcaster

if __name__ == '__main__':
    HISTORY_FILE = 'daletou_history.txt'
    CHART_FILE = 'daletou_chart.html'

    print("程序开始")
    print("开始爬取数据")
    c = Crawler()
    c.setBaseUrl('https://www.lottery.gov.cn/historykj/history_{}.jspx?_ltype=dlt')
    for i in range(Config.PAGES):
        c.put(i)

    c.start()
    c.join()
    print("数据写入到文件")
    c.dumpToFile(HISTORY_FILE)
    print("开始分析数据")
    cp = ChartPresenter(HISTORY_FILE, CHART_FILE)
    cp.show_dlt()
    print("开始预测")
    f = Forcaster(HISTORY_FILE)
    f.forcast_dlt()
