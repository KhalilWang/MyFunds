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

print new_stock
print '----'
print '今日收益:' + str(total_income)
