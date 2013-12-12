__author__ = 'billzhou'
# this tool is used for crate train data from input quote data

from zhihui.web.extention.routing import route
from ultrafinance.dam.sqlDAM import SqlDAM, QuoteSql

def buildTrainData():
    dam = SqlDAM()
    dam.setup({'db': 'sqlite:///../../zhihui/data/ftest.sqlite'})
    dam.setSymbol('EURUSD')
    _quotes = dam.readQuotes(20000101, 20131231)
    for quote in _quotes:
        quoterow = quote.toDict()
        print quoterow
    print len(_quotes)

if __name__ == "__main__":
    buildTrainData()