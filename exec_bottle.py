#!/usr/bin/python
# -*- coding: utf-8 -*-
#import sys
#sys.path.append("C:\\Users\\tagawa\\AppData\\Local\\Continuum\\Anaconda3\\Lib")

import os
from bottle import route, run
import main

print("start")
df = None
dic = None

@route("/")
def index():
    global df
    html, df = main.exec_get_html()

    return html


@route("/show")
def show():
    global dic
    if dic is None:
        tmp = main.filter_dataframe(df)
    # Filter
    print(tmp)
    return "sampl"

#run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
run(host='localhost', port=8080, debug=True)
