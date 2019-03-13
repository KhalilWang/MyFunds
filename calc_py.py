# -*- coding:utf-8 -*-
import requests
import time
import json
import datetime

ts = int(time.time())
my_stock = [('001593', 2260), ('001550', 4749), ('002974', 1815.8381350000002), ('001133', 4421.290867199999), ('001071', 3048.6177877), ('161024', 4260.23118256), ('161017', 5285.64030785), ('502003', 5838.60841679)]

# my_stock = [('502003',11029.4), ('000962',10072.6), ('001592',5655.3), ('002974',4015.5)]

# a = requests.get('http://fundgz.1234567.com.cn/js/502003.js?rt=1551342960000&tdsourcetag=s_pctim_aiomsg')

with open('newstock.txt', 'r') as f:
    lines = f.readlines()
    timestr, stock = lines[-2:]
    last_time_dt = datetime.datetime.strptime(timestr[:-1], '%Y-%m-%d %H:%M:%S.%f')
    now = datetime.datetime.now()
    if now.day - last_time_dt.day == 1:
        my_stock = eval(stock)
    

new_stock = []
total_income = 0
for number, money in my_stock:
    url = 'http://fundgz.1234567.com.cn/js/' + number + '.js?rt=' + str(ts) + '&tdsourcetag=s_pctim_aiomsg'
    r = requests.get(url)
    result = r.text

    result = result[result.find('{'):-2]
    rst_dict = json.loads(result)

    income = money * float(rst_dict['gszzl']) / 100
    total_income += income
    new_stock.append((number, money + income))
    print rst_dict['name'] + '-' + number, '\n\t\t\tincome:', income, '\trate:', rst_dict['gszzl'] + '\tmoney:' + str(money)

with open('newstock.txt', 'a+') as f:
    f.write('\n' + str(datetime.datetime.now()) + '\n')
    f.write(str(new_stock))

# print new_stock
print '----'
print 'total_income:' + str(total_income)

