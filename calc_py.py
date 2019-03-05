# -*- coding:utf-8 -*-
import requests
import time
import json

ts = int(time.time())

my_stock = [
    ('110022', 3046.56),
    ('502003', 5209.13),
    ('001071', 6539.43),
    ('001593', 210.12),
    ('161024', 2989.63),
    ('161017', 3193.86),
    ('001133', 4176.87)
]

# my_stock = [('502003',11029.4), ('000962',10072.6), ('001592',5655.3), ('002974',4015.5)]

# a = requests.get('http://fundgz.1234567.com.cn/js/502003.js?rt=1551342960000&tdsourcetag=s_pctim_aiomsg')

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
    print rst_dict['name'] + '-' + str(money), '\nincome:', income, '\trate:', rst_dict['gszzl']

with open('newstock.txt', 'a+') as f:
    f.write('\n' + str(datetime.datetime.now()) + '\n')
    f.write(str(new_stock))

# print new_stock
print '----'
print 'total_income:' + str(total_income)

