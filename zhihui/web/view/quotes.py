# coding=utf-8
import os,sys
import json
import tornado.web

from datetime import datetime
import time
from zhihui.web.extention.routing import route
from ultrafinance.dam.sqlDAM import SqlDAM
from ultrafinance.backTest.stateSaver.sqlSaver import SqlSaver
from zhihui.tools.trainDataMaker import getSourceData
from zhihui.ultrafinance.pyTaLib.fractal import Fractal
from zhihui.tools.trainDataMaker import FractalSelectManager


ORDER_ACTION = {'sell': 1,
                'buy': 2,
                'sell_short': 3,
                'buy_to_cover': 4}

F_TYPE = {
    1: 'D',
    2: 'U'
}

COLOR_TYPE ={
    0: '#0000ff',
    1: '#ff0000'
}

@route(r"/quotes", name="quotes")
class QuotesHandler(tornado.web.RequestHandler):
    """
        QuotesHandler
    """

    def get(self):
        """
            get quotes
        """
        dam = SqlDAM()

        print os.path.dirname(__file__)

        flags={}
        sqlsave = SqlSaver()
        sqlsave.setup({'db': 'sqlite:///../zhihui/data/output.sqlite'}, "['EURUSD']_sma")
        result = sqlsave.getStates(20000101,20131231)
        for row in result:
            if row.updateOrders != []:
                order = row.updateOrders[0]
                flags[row.time] = order.action

        dam.setup({'db': 'sqlite:///../zhihui/data/ftest.sqlite'})
        dam.setSymbol('EURUSD')
        _quotes = dam.readQuotes(20000101, 20131231)
        quotes = [quote.toDict() for quote in _quotes]

        self.write(json.dumps(quotes))

@route(r"/indicators", name="indicators")
class Indicators(tornado.web.RequestHandler):
    """
        Indicators
    """
    def get(self):
        """
            get
        """
        fratal = Fractal()
        fratalResult = fratal(getSourceData())
        fratalFilter = FractalSelectManager()

        retData = []
        for row in fratalResult:
            retRow = {}
            dt = time.strptime(str(row['time']), '%Y%m%d')
            retRow['x'] = time.mktime(dt)*1000
            retRow['y'] = row['price']
            retRow['title'] = F_TYPE.get(row['type'])
            retRow['text'] = "fractals " + retRow['title']
            colortype = COLOR_TYPE[0]
            if fratalFilter.isSelected(row['time']):
                colortype = COLOR_TYPE[1]
            retRow['fillColor'] = colortype

            retData.append(retRow)
        self.write(json.dumps(retData))

if __name__ == "__main__":
    test = datetime.strptime(str(20120505), "%Y%m%d")
    print test
    t = time.mktime(time.strptime("20120505", "%Y%m%d"))
    print t*1000