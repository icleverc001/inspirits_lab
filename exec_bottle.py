#!/usr/bin/python
# -*- coding: utf-8 -*-
#import sys
#sys.path.append("C:\\Users\\tagawa\\AppData\\Local\\Continuum\\Anaconda3\\Lib")

import os
from bottle import route, run
import main

print("start")

@route("/")
def hallo():
    print("exec")
    return main.exec_get_html()

run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
#run(host='localhost', port=8080, debug=True)
