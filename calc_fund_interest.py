# -*— coding: utf-8 -*-
__author__ = 'ws'
__date__ = '2019/3/28 10:41'
__doc__ = """"""

from datetime import datetime

import requests

# 基金代码和持仓份额
fund_pool = {
    '502003': 1576.83,
    '110011': 352.74,
    '110022': 626.05,
    '110020': 304.22,
    '002199': 3145.83,
    '001178': 212.3,
    '006130': 1695.95,
    '001550': 4099.21,
    '420003': 267.02,
    '162605': 1017.81,
    '519697': 417.46,
    '001938': 1157.03,
    '090020': 267.31,
    '160716': 114.61,
    '000008': 271.42,
    '001616': 90.63,
    '163412': 179.59,
    '519671': 306.16,
    '501029': 477.25,
    '001064': 485.4
}


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Host': 'danjuanapp.com'
}

get_va_url = 'https://danjuanapp.com/djapi/fund/estimate-nav/{fundcode}'
get_info_url = 'https://danjuanapp.com/djapi/fund/{fundcode}'


def get_va_info(fundcode):
    """
    获取估值信息
    :param fundcode:
    :return: {'time': '2019-03-28 11:10:00', 'nav': 2.431, 'percentage': 0.747}
    """
    res = requests.get(get_va_url.format(fundcode=fundcode), headers=headers)
    if res.status_code == 200:
        res = res.json()
        if res['result_code'] == 0:
            res = res['data']['items'][-1]
            # 格式化时间
            res['time'] = datetime.fromtimestamp(res['time']/1000).strftime('%Y-%m-%d %H:%M:%S')
            return res
    return None

def get_fund_info(fundcode):
    """
    获取基金进本信息
    :param fundcode:
    :return: {
        'fd_code': '基金代码',
        'fd_name': '基金名称',
        'fund_derived': '上个交易日信息'{end_date, unit_nav, }
    }
    """
    res = requests.get(get_info_url.format(fundcode=fundcode), headers=headers)
    if res.status_code == 200:
        res = res.json()
        if res['result_code'] == 0:
            return res['data']
    return None

def Main(is_need_sort=False):
    today_total_interest = 0.0
    res = []
    print('---------------------------------')
    for fundcode, share in fund_pool.items():
        fundinfo = get_fund_info(fundcode)
        fundva = get_va_info(fundcode)
        # 当前市值 = 昨日单位净值 * 持仓份额
        mv = float(fundinfo['fund_derived']['unit_nav']) * share
        # 今日预估收益 = 市值 * 今日预估涨幅 / 100%
        va = fundva['percentage'] * mv / 100
        today_total_interest += va
        res.append((fundcode, fundinfo['fd_name'], mv, va, fundva['percentage']))
        if not is_need_sort:
            print(fundcode, fundinfo['fd_name'], '当前市值:', format(mv, '.2f'), '今日涨跌幅', format(fundva['percentage'], '.2f') + '%')
            print('今日预估收益:', format(va, '.2f'))
    if is_need_sort:
        # 按照涨跌幅排序
        res = sorted(res, key=lambda x: x[-1])
        res.reverse()
        for fundcode, fundname, mv, va, percentage in res:
            print(fundcode, fundname, '当前市值:', format(mv, '.2f'), '今日涨跌幅', format(percentage, '.2f') + '%')
            print('今日预估收益:', format(va, '.2f'))
    print('---------------------------------')
    print('今日累计收益:', format(today_total_interest, '.2f'))


if __name__ == '__main__':
    Main(is_need_sort=True)
