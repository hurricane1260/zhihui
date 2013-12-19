# coding=utf-8
import os,sys
import json
import tornado.web

from datetime import datetime
import time
from zhihui.web.extention.routing import route
from ultrafinance.dam.sqlDAM import SqlDAM
from ultrafinance.backTest.stateSaver.sqlSaver import SqlSaver
from zhihui.ultrafinance.pyTaLib.fractal import Fractal
from zhihui.tools.trainDataMaker import FractalSelectManager
from zhihui.ultrafinance.pyTaLib.indicator import Sma


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

def getSourceData():
    dam = SqlDAM()
    dam.setup({'db': 'sqlite:///../zhihui/data/ftest.sqlite'})
    dam.setSymbol('EURUSD')
    _quotes = dam.readQuotes(20000101, 20131231)
    return _quotes

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
'''
Indicator Data format:
[ {'name':'first indicator', 'type':'flags', 'data':[{'x':0,'y':0,'title':0,'text':0},...]},
  {'name':'second indicator', 'type':'spline', 'data':[[time, open, high, low, close],...]},
]
'''
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
        quotes = getSourceData()
        print 'quotes: ', len(quotes)
        fratalResult = fratal(quotes)
        fratalFilter = FractalSelectManager()
        indicatordata = []

        fractalIndicator = {}
        fractalData = []

        for row in fratalResult:
            rowdata = {}
            dt = time.strptime(str(row['time']), '%Y%m%d')
            rowdata['x'] = time.mktime(dt)*1000
            rowdata['y'] = row['price']
            rowdata['title'] = F_TYPE.get(row['type'])
            rowdata['text'] = "fractals " + rowdata['title']
            colortype = COLOR_TYPE[0]
            if fratalFilter.isSelected(row['time']):
                colortype = COLOR_TYPE[1]
            rowdata['fillColor'] = colortype
            fractalData.append(rowdata)

        # fractl indicator
        fractalIndicator['name'] = 'fractal'
        fractalIndicator['type'] = 'flags'
        fractalIndicator['data'] = fractalData

        smaIndicator = {}
        maData = []
        sma = Sma(5)

        sma20Indicator = {}
        ma20Data = []
        sma20 = Sma(20)

        count = 0
        count2 = 0
        for quote in quotes:
            if sma(quote.close):
                # temp use
                rowdata = []
                dt = time.strptime(str(quote.time), '%Y%m%d')
                rowdata.append(time.mktime(dt)*1000)
                rowdata.append(round(sma.getLastValue(), 4))
                rowdata.append(round(sma.getLastValue(), 4))
                rowdata.append(round(sma.getLastValue(), 4))
                rowdata.append(round(sma.getLastValue(), 4))
                maData.append(rowdata)
            if sma20(quote.close):
                # temp use
                rowdata = []
                dt = time.strptime(str(quote.time), '%Y%m%d')
                rowdata.append(time.mktime(dt)*1000)
                rowdata.append(round(sma20.getLastValue(), 4))
                rowdata.append(round(sma20.getLastValue(), 4))
                rowdata.append(round(sma20.getLastValue(), 4))
                rowdata.append(round(sma20.getLastValue(), 4))
                ma20Data.append(rowdata)

        # sma indicator
        smaIndicator['name'] = 'sma 5'
        smaIndicator['type'] = 'spline'
        smaIndicator['fillColor'] = '#0000ff'
        smaIndicator['data'] = maData

        sma20Indicator['name'] = 'sma 20'
        sma20Indicator['type'] = 'spline'
        sma20Indicator['fillColor'] = '#ff0000'
        sma20Indicator['data'] = ma20Data

        # add all indicators
        indicatordata.append(fractalIndicator)
        indicatordata.append(smaIndicator)
        indicatordata.append(sma20Indicator)
        print 'fractal: ', len(fractalData), fractalData
        print 'sma 20: ', len(maData), maData

        self.write(json.dumps(indicatordata))

if __name__ == "__main__":
    test = datetime.strptime(str(20120505), "%Y%m%d")
    print test
    t = time.mktime(time.strptime("20120505", "%Y%m%d"))
    print t*1000