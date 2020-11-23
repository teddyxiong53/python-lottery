from collections import Counter
from pyecharts.charts import Bar,Page
from pyecharts import options as opts
from config import Config

class ChartPresenter:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
    def show_dlt(self):
        red_balls = []
        blue_balls = []
        with open(self.input_file, 'r') as f:
            for i in range(Config.PAGES * Config.ITEMS_PER_PAGE):
                one_line_data = f.readline().strip()
                # print(one_line_data)
                red_balls.extend([int(one_line_data[15 + (2 * i):15 + (2 * (i + 1))]) for i in range(5)])
                blue_balls.append(int(one_line_data[-4:-2]))
                blue_balls.append(int(one_line_data[-2:]))

        red_counter = Counter(red_balls)
        blue_counter = Counter(blue_balls)
        # print(red_balls)
        # print(blue_balls)
        # print(red_counter)
        # print(blue_counter)
        # print(red_counter.most_common())
        # print(blue_counter.most_common())
        red_dict = {}
        blue_dict = {}
        for i in red_counter.most_common():
            red_dict['{}'.format(i[0])] = i[1]

        for j in blue_counter.most_common():
            blue_dict['{}'.format(j[0])] = j[1]

        print(red_dict)
        print(blue_dict)

        red_list = sorted(red_counter.most_common(), key=lambda number: number[0])
        blue_list = sorted(blue_counter.most_common(), key=lambda number: number[0])
        print(blue_list)
        print(red_list)

        # 红球图表添加
        red_bar = Bar()
        red_x = ['{}'.format(str(x[0])) for x in red_list]
        red_y = ['{}'.format(str(x[1])) for x in red_list]
        red_bar.add_xaxis(red_x)
        red_bar.add_yaxis('红色球出现的次数', red_y)
        # 篮球图表添加
        blue_bar = Bar()
        blue_x = ['{}'.format(str(x[0])) for x in blue_list]
        blue_y = ['{}'.format(str(x[1])) for x in blue_list]
        blue_bar.add_xaxis(blue_x)
        blue_bar.add_yaxis('蓝色球出现的次数',blue_y, itemstyle_opts=opts.ItemStyleOpts(color='blue'))

        page = Page(page_title='大乐透数据分析', interval=3)
        page.add(red_bar)
        page.add(blue_bar)

        page.render(self.output_file)


if __name__ == '__main__':
    c = ChartPresenter('daletou_history.txt', '1.html')
    c.show_dlt()
