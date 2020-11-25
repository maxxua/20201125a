#ch11_p_1.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#设置中文标签的显示
plt.rcParams['font.sans-serif']=['SimHei']

#数据清洗并获取有效数据
def get_data(path):
    #读取数据
    film_data = pd.read_csv(path,delimiter=';', encoding='utf8', names=['电影名称','上线时间','下线时间','公司','导演','主演','类型','票房','城市'])
    # 去重
    film_data = film_data.drop_duplicates().reset_index().drop('index', axis=1)
    # 选择需要的列,并去空
    film_data=film_data[['电影名称','导演','类型','票房']].dropna()
    #对电影类型进行处理
    film_data['类型'] = film_data['类型'].str.strip()
    film_data['类型'] = film_data['类型'].str[0:2]
    # 获取票房列数据，去除")"，转换成浮点数
    film_data['票房'] = film_data['票房'].str.split('）', expand=True)[1].astype(np.float64)
    print(film_data)
    return film_data

#取得清洗后的数据
data = get_data('d:\\dianying.csv')

#对电影的票房进行求和
film_box_office = data.groupby(data['电影名称'])['票房'].sum()
#将统计结果的Series格式转换为DataFrame,并按降序排序
film_box_office = film_box_office.reset_index().sort_values(by='票房',ascending=False)
#取票房前5名的
film_box_office_5 = film_box_office.head()
#输出统计结果
print(film_box_office_5)

#对电影类型进行计数
film_type = data.groupby(data['类型'])['电影名称'].count().reset_index()
film_type.rename(columns = {'电影名称':'小计'},inplace = True)
print(film_type)

#对导演的票房进行统计
director_box_office = data.groupby(['导演'])['票房'].sum().reset_index().sort_values(by='票房',ascending=False)
director_box_office_5 = director_box_office.head()
print(director_box_office_5)

#对导演的所导电影类型进行统计
director = data.groupby(['导演','类型'])['票房'].count().reset_index()
director.rename(columns = {'票房':'小计'},inplace = True)
print(director)

# 画图
fig = plt.figure(figsize=(15,15)) #创建画布
ax_1 = fig.add_subplot(2,2,1) #添加子图
ax_2 = fig.add_subplot(2,2,2)
ax_3 = fig.add_subplot(2,2,3)
ax_4 = fig.add_subplot(2,2,4)

#票房前五的电影
ax_1.set_title("票房总计")
#ax_1.set_xlabel('电影名称')
ax_1.set_ylabel('万元')
ax_1.set_xticklabels(film_box_office_5['电影名称'],rotation=15) #文字显示旋转15度
ax_1.bar(film_box_office_5['电影名称'],film_box_office_5['票房'])

#电影类型统计
ax_2.set_title("电影类型统计")
ax_2.pie(film_type['小计'],labels=film_type['类型'],autopct='%1.2f%%',shadow=True)

#导演票房前五的统计
ax_3.set_title("导演票房总计")
ax_3.set_xlabel('导演')
ax_3.set_ylabel('万元')
ax_3.set_xticklabels(director_box_office_5['导演'])
ax_3.bar(director_box_office_5['导演'],director_box_office_5['票房'],color='r')

#导演与类型统计
ax_4.set_title("导演与电影类型统计")
ax_4.set_xticklabels(director['导演'],rotation=90)#文字显示旋转90度
ax_4.set_yticklabels(director['类型'])
ax_4.scatter(director['导演'],director['类型'],s=director['小计']*50,edgecolors="red")#点的大小由分类统计的数量决定

plt.show()
