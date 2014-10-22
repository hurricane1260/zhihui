# coding=utf-8
import os,sys
import json
import tornado.web

from datetime import datetime
import time
try:
    import zhihui
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from zhihui.web.extention.routing import Route
from ultrafinance.dam.sqlDAM import SqlDAM
from ultrafinance.backTest.stateSaver.sqlSaver import SqlSaver
from zhihui.ultrafinance.pyTaLib.fractal import Fractal
from zhihui.tools.trainDataMaker import FractalSelectManager
from zhihui.ultrafinance.pyTaLib.indicator import Sma, Macd, Stoch
import numpy as np
import copy
import MySQLdb


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

''' indicator data format:
[ [ [open,high,low,close],..]   # one result
  [ [open,high,low,close],..]   # two reslut
]
'''
def genIndicatorData(quote, indicator, resultIndicatorData):
    _value = indicator(quote.close)
    if _value:
        indicatordata = []
        dt = time.strptime(str(quote.time), '%Y%m%d')
        _time = time.mktime(dt)*1000
        if isinstance(_value, list):
            for _val in _value:
                tmpval = _val
                if isinstance(_val, np.ndarray):
                    tmpval = _val[len(_val)-1]
                rowdata = []
                rowdata.append(_time)
                rowdata.append(round(tmpval, 4))
                rowdata.append(round(tmpval, 4))
                rowdata.append(round(tmpval, 4))
                rowdata.append(round(tmpval, 4))
                indicatordata.append(rowdata)
        else:
            rowdata = []
            rowdata.append(_time)
            rowdata.append(round(_value, 4))
            rowdata.append(round(_value, 4))
            rowdata.append(round(_value, 4))
            rowdata.append(round(_value, 4))
            indicatordata.append(rowdata)

        # construct the indicator data format
        if len(resultIndicatorData) == 0:
            for i in range(0, len(indicatordata)):
                resultIndicatorData.append([])

        for i in range(0, len(indicatordata)):
            resultIndicatorData[i].append(indicatordata[i])

        return resultIndicatorData
    else:
        return None

def getMysqlStockData():
    # 打开数据库连接
    db = MySQLdb.connect("localhost","root","ty200","stock_db" )

    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()

    quotes = []
    # SQL 查询语句
    sql = "SELECT Date,Open,High,Low,Close,Volume,Adjusted FROM stock_data "
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        
        results = cursor.fetchall()
        for row in results:
            quote ={}
            quote['time'] = row[0]
            quote['open'] = row[1]
            quote['high'] = row[2]
            quote['low'] = row[3]
            quote['close'] = row[4]
            quote['volume'] = row[5]
            quote['adjusted'] = row[6]
            # 打印结果
            print quote
    except:
        print "Error: unable to fecth data"

    # 关闭数据库连接
    db.close()
    return quotes

@route(r"/mysqlQuotes", name="mysqlQuotes")
class MysqlQuotesHandler(tornado.web.RequestHandler):
    """
        MysqlQuotesHandler
    """

    def get(self):
        """
            get mysqlQuotes
        """   
        #quotes = getMysqlStockData()

        #self.write(json.dumps(quotes))
        self.write("hello ok!")

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
[ {'name':'first indicator', 'yAxis':0, 'type':'flags', 'data':[{'x':0,'y':0,'title':0,'text':0},...]},
  {'name':'second indicator', 'yAxis':0, 'type':'spline', 'data':[[time, open, high, low, close],...]},
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
        allindicatordata = []

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
        fractalIndicator['yAxis'] = 0
        fractalIndicator['data'] = fractalData

        smaIndicator = {}
        maData = []
        sma = Sma(5)

        sma20Indicator = {}
        ma20Data = []
        sma20 = Sma(20)

        macd20Indicator = {}
        macd20Data = []
        macd20 = Macd(20)

        stoch20Indicator = {}
        stoch20Data = []
        stoch20 = Stoch(20)

        for quote in quotes:
            genIndicatorData(quote, sma, maData)
            genIndicatorData(quote, sma20, ma20Data)
            genIndicatorData(quote, macd20, macd20Data)
            genIndicatorData(quote, stoch20, stoch20Data)

        # sma indicator
        smaIndicator['name'] = 'sma 5'
        smaIndicator['type'] = 'spline'
        smaIndicator['fillColor'] = '#0000ff'
        smaIndicator['yAxis'] = 0
        smaIndicator['data'] = maData[0]

        sma20Indicator['name'] = 'sma 20'
        sma20Indicator['type'] = 'spline'
        sma20Indicator['fillColor'] = '#ff0000'
        sma20Indicator['yAxis'] = 0
        sma20Indicator['data'] = ma20Data[0]

        # macd20 indicator
        macd20Indicator['name'] = 'macd 20'
        macd20Indicator['type'] = 'spline'
        macd20Indicator['fillColor'] = '#ff0000'
        macd20Indicator['yAxis'] = 1
        macd20Indicator['data'] = macd20Data[0]
        macd20Indicator2 = copy.copy(macd20Indicator)
        macd20Indicator2['fillColor'] = '#00ff00'
        macd20Indicator2['data'] = macd20Data[1]
        macd20Indicator3 = copy.copy(macd20Indicator)
        macd20Indicator3['fillColor'] = '#0000ff'
        macd20Indicator3['data'] = macd20Data[2]

        #stoch 20 indicator
        stoch20Indicator['name'] = 'stoch 20'
        stoch20Indicator['type'] = 'spline'
        stoch20Indicator['fillColor'] = '#ff0000'
        stoch20Indicator['yAxis'] = 2
        stoch20Indicator['data'] = stoch20Data[0]

        # add all indicators
        allindicatordata.append(fractalIndicator)
        allindicatordata.append(smaIndicator)
        allindicatordata.append(sma20Indicator)
        allindicatordata.append(macd20Indicator)
        allindicatordata.append(macd20Indicator2)
        allindicatordata.append(macd20Indicator3)
        allindicatordata.append(stoch20Indicator)

        self.write(json.dumps(allindicatordata))


if __name__ == "__main__":
    data = getMysqlStockData()
    print data
    # test = datetime.strptime(str(20120505), "%Y%m%d")
    # print test
    # t = time.mktime(time.strptime("20120505", "%Y%m%d"))
    # print t*1000