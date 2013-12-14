# coding=utf-8
import os,sys
import json
import tornado.web
from sqlalchemy import and_
from zhihui.web.extention.routing import route
from ultrafinance.dam.sqlDAM import SqlDAM, QuoteSql
from ultrafinance.backTest.stateSaver.sqlSaver import  SqlSaver
from zhihui.tools.trainDataMaker import findUpFlag
from zhihui.tools.trainDataMaker import findDownFlag


ORDER_ACTION = {'sell': 1,
                'buy': 2,
                'sell_short': 3,
                'buy_to_cover': 4}

@route(r"/quotes", name="quotes")
class QuotesHandler(tornado.web.RequestHandler):
    """
        QuotesHandler
    """
    SELL = 'sell'
    BUY = 'buy'
    SELL_SHORT = 'sell_short'
    BUY_TO_COVER = 'buy_to_cover'

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
        quotes = []
        # [quote.toDict() for quote in _quotes]

        for i in range(0,len(_quotes)):
            quote = _quotes[i]
            quoterow = quote.toDict()
            type = 0
            if quote.time in flags:
                action = flags[quote.time]
                type = ORDER_ACTION.get(action, 0)

            quoterow['order'] = type
            if i > 9:
                if findUpFlag(i, _quotes):
                    quoterow['fractal'] = 1
                elif findDownFlag(i, _quotes):
                    quoterow['fractal'] = 2
                else:
                    quoterow['fractal'] = 0
            else:
                quoterow['fractal'] = 0
            quotes.append(quoterow)
        self.write(json.dumps(quotes))


if __name__ == "__main__":
    pass
    # flags={}
    # sqlsave = SqlSaver()
    # sqlsave.setup({'db': 'sqlite:///../../../zhihui/data/output.sqlite'}, "['EURUSD']_sma")
    # result = sqlsave.getStates(20000101,20131231)
    # for row in result:
    #     if row.updateOrders != []:
    #         flags[row.time] = row.updateOrders
    # print flags
    # dam = SqlDAM()
    #
    # flags={}
    # sqlsave = SqlSaver()
    # sqlsave.setup({'db': 'sqlite:///../../../zhihui/data/output.sqlite'}, "['EURUSD']_sma")
    # result = sqlsave.getStates(20000101,20131231)
    # for row in result:
    #     if row.updateOrders != []:
    #         flags[row.time] = row.updateOrders
    #
    # dam.setup({'db': 'sqlite:///../../../zhihui/data/ftest.sqlite'})
    # dam.setSymbol('EURUSD')
    # _quotes = dam.readQuotes(20000101, 20131231)
    # quotes = []
    # # [quote.toDict() for quote in _quotes]
    # type = 1
    # for quote in _quotes:
    #     quoterow = quote.toDict()
    #     quoterow['order'] = 0
    #     if(quote.time in flags):
    #         quoterow['order'] = type
    #         type = 2
    #     quotes.append(quoterow)
    # print  json.dumps(quotes)
