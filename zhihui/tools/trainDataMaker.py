__author__ = 'billzhou'
# this tool is used for crate train data from input quote data

from zhihui.web.extention.routing import route
from ultrafinance.dam.sqlDAM import SqlDAM, QuoteSql
import numpy as np
import pylab as pl
from sklearn import svm
from sklearn import linear_model
from sklearn import tree
import pandas as pd
from sklearn import datasets
from datetime import datetime
import time
from talib import abstract

# def svmtest():
#     clf = svm.SVC(kernel='linear')
#     fractalsList = getFractalsList()
#     fractalsFiltered, target = getFilteredFractalsList(fractalsList)
#     nft = np.array(fractalsFiltered)
#     ntarget = np.array(target)
#     clf.fit(nft, ntarget)
#     print nft
#     print ntarget
#     print clf.predict(nft)

def tablibtest():
    quotes = getSourceData()
    inputs = []
    for quote in quotes:
        inputs.append(quote.close)
    tainputs = np.array(inputs)

    myinput = {
    'open': tainputs,
    'high': tainputs,
    'low': tainputs,
    'close': tainputs,
    'volume': np.random.random(100)
    }

    print abstract.SMA(myinput)


def getSourceData():
    dam = SqlDAM()
    dam.setup({'db': 'sqlite:///../zhihui/data/ftest.sqlite'})
    dam.setSymbol('EURUSD')
    _quotes = dam.readQuotes(20000101, 20131231)
    return _quotes


# def processSelectData():
#     fratalsTimeKeyData = getTimeKeyFractals()
#     print len(selectdata)
#     selectfractls = []
#     for data in selectdata:
#         gmtime = time.gmtime(data/1000+24*60*60)
#         timestr = '%4d%02d%02d'%(gmtime.tm_year, gmtime.tm_mon, gmtime.tm_mday)
#         key = int(timestr)
#         selectfractls.append(fratalsTimeKeyData[key])
#
#     print len(selectfractls)

if __name__ == "__main__":
    # buildTrainData()
    # svmtest()
    # processSelectData()
    tablibtest()
