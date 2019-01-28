#!/usr/bin/python
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
from matplotlib import image
import pandas as pd
import datetime
import json
import urllib.request
import template

col_headers = ["会場", "日時", "購入", "タイトル", "在庫", "申込開始"]
pd.set_option("display.max_colwidth", 80)
weekdaylst = ["月", "火", "水", "木", "金", "土", "日"]
def test(idx):
    urlstr = "http://inspirits-tennis-club.com/entry/index.html" if idx == 0 else "http://inspirits-tennis-club.com/entry/index_{}.html".format(idx + 1)
    html = urlopen(urlstr)
    return html

def get_table_data(idx):
    urlstr = "http://inspirits-tennis-club.com/entry/index.html" if idx == 0 else "http://inspirits-tennis-club.com/entry/index_{}.html".format(idx + 1)
    html = urlopen(urlstr)
    soup = BeautifulSoup(html, "html.parser")

    #テーブルを指定
    table = soup.findAll("table", {"class": "chart01_br"})[0]
    rows = table.findAll("tr")
    rows.pop(0) # 先頭のHeaderを削除
    lst = []
    for row in rows:
        rowary = []
        for ic, cel in enumerate(row.findAll(['td', 'th'])):
            if ic == 3:
                val = cel.find("img")['src']
            elif ic == 1:
                tmpdate = cel.get_text().split('～')[0]
                mn = tmpdate.split('/')[0]
                dy = tmpdate.split('/')[1].split('(')[0]
                tm = tmpdate.split(')')[1]
                #val = "2019-{0}-{1} {2}".format(mn, dy, tm)
                val = datetime.datetime(2019, int(mn), int(dy), int(tm.split(':')[0]), int(tm.split(':')[1]), 0)
            elif ic == 2:
                link = cel.find("a")['href']
                val = cel.get_text()
                rowary.append(link)
            else:
                val = cel.get_text()
            rowary.append(val)
        # lst.append([c.get_text() for c in row.findAll(['td', 'th'])])
        lst.append(rowary)
    return lst

def check_date_weekday(dat, holidays):
    if dat.weekday() > 4: # 土日か
        return True
    for holi in holidays: # 指定祝日か
        ds = [int(h) for h in holi.split('/')]
        tmp = datetime.datetime(ds[0], ds[1], ds[2])
        if dat == tmp:
            return True
    return False

def check_status(url):
    filename = 'check_status.jpg'
    urllib.request.urlretrieve(url, filename)
    I = image.imread(filename)[6, 6, :]
    if I[0] == 153 and I[1] == 51 and I[2] == 51:
        return False
    return True

def filter_dataframe(df_ori):
#    with open('filter.json', 'r', encoding='utf-8') as f:
#        jsondata = json.load(f)
    df_result = df_ori

#    for place in jsondata["会場NG"]:
#        df_result = df_result[df_result.apply(lambda x: place not in x[col_headers[0]], axis=1)]
#    for ngtitle in jsondata["タイトルNG"]:
#        df_result = df_result[df_result.apply(lambda x: ngtitle not in x[col_headers[3]], axis=1)]
#    df_result = df_result[df_result.apply(lambda x: check_date_weekday(x[col_headers[1]], jsondata["日時"]), axis=1)]
    df_result = df_result[df_result.apply(lambda x: check_status(x[col_headers[4]]), axis=1)]

    return df_result


def exec_get_html():
    #URLの指定
    first_html = urlopen("http://inspirits-tennis-club.com/entry/index.html")
    first_soup = BeautifulSoup(first_html, "html.parser")

    pagelink = first_soup.find("p", attrs={"class": "txlinkR"})
    page_count = len(pagelink.findAll(attrs={"class": "link_page"})) + 1

    ary = []
    for ip in range(page_count):
        ary.extend(get_table_data(ip))

    df = pd.DataFrame(columns=col_headers)
    for lst in ary:
        tmp_se = pd.Series(lst, index=df.columns)
        df = df.append(tmp_se, ignore_index=True)

    #print(df)
    #pd = pd.to_datetime(df[col_headers[1]])

    df_print = filter_dataframe(df)
    #df_print["会場"] = df_print["会場"].map(lambda s: "<a href='https://www.google.com/maps/place/{0}/'>{0}</a>".format(s))
    df_print["在庫"] = df_print["在庫"].map(lambda s: "<img src='{}'/>".format(s))
    df_print["購入"] = df_print["購入"].map(lambda s: "<a href='{}'>購入画面</a>".format(s))
    df_print["日時"] = df_print["日時"].map(lambda s: "{0:%m/%d}({1}) {0:%H:%M}".format(s, weekdaylst[s.weekday()]))

    table = df_print.to_html(classes=["table", "table-bordered", "table-hover"], escape=False)
    html = template.get_html_template().format(table=table)

    return html

if __name__ == '__main__':
    html = exec_get_html()
    with open("out.html", "w", encoding='utf-8') as f:
        f.write(html)