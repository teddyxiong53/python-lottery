from sklearn import svm
from config import Config

class Forcaster:
    def __init__(self, input_file):
        self.input_file = input_file

    def forcast_dlt(self):
        data=[]
        period=[]
        first_num=[]
        second_num=[]
        third_num=[]
        fourth_num=[]
        fifth_num=[]
        sixth_num=[]
        seventh_num=[]

        with open(self.input_file, 'r') as  f:
            for i in range(Config.ITEMS_PER_PAGE*Config.PAGES):
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


if __name__ == '__main__':
    f = Forcaster('daletou_history.txt')
    f.forcast_dlt()

