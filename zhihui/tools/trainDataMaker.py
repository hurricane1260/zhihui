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

def svmtest():
    clf = svm.SVC(kernel='rbf')
    fractalsList = getFractalsList()
    fractalsFiltered, target = getFilteredFractalsList(fractalsList)
    clf.fit(fractalsFiltered,target)
    # print fractalsFiltered
    # print target
    data = [[8, 0.02848000000000006]]
    # print clf.predict(data)
    # print fractalsFiltered
    # iris = datasets.load_iris()
    # print len(iris.data)
    # print len(iris.target)

def getSourceData():
    dam = SqlDAM()
    dam.setup({'db': 'sqlite:///../zhihui/data/ftest.sqlite'})
    dam.setSymbol('EURUSD')
    _quotes = dam.readQuotes(20000101, 20131231)
    return _quotes

def getFractalsList():
    _quotes = getSourceData()
    fractals = []
    for i in range(0, len(_quotes)):
        quoterow = _quotes[i].toDict()
        if i > 9:
            flagrow = {}
            if findUpFlag(i, _quotes):
                flagrow['index'] = i
                flagrow['findex'] = len(fractals)
                flagrow['quote'] = quoterow
                flagrow['type'] = 1
                fractals.append(flagrow)

            if findDownFlag(i, _quotes):
                flagrow['index'] = i
                flagrow['findex'] = len(fractals)
                flagrow['quote'] = quoterow
                flagrow['type'] = 2
                fractals.append(flagrow)
        # print quoterow
    return fractals

def getFilteredFractalRow(index, fractals):
    if not index in range(1, len(fractals) -1):
        return [0,0,0,0]
    i = index
    ft = fractals[i]
    curindex = ft['index']
    curprice = ft['quote']['close']
    x1 = curindex - fractals[i-1]['index']
    x2 = fractals[i+1]['index'] - curindex
    y1 = curprice - fractals[i-1]['quote']['close']
    y2 = fractals[i+1]['quote']['close'] - curprice
    type = ft['type']
    if x1 >= 3 and x2 >= 3 and abs(y1) > 0.014 and abs(y2) > 0.014:
        result = [1, x1, y1, type]
    else:
        result = [0, x1, y1, type]
    # print result
    return result

    # fromat:
    # [[use,x1,y1,type],
    #  [use,x1,y1,type]]
def getFilteredFractalsList(fractalsList):

    fractals = fractalsList
    fractalsFliteredResult = []
    target = []
    for i in range(1, len(fractals)-1):
        result =getFilteredFractalRow(i, fractals)
        data = [result[1], abs(result[2])]
        target.append(result[0])
        fractalsFliteredResult.append(data)
        # val ='-1'
        # if result[0] == 1:
        #     val ='+1'
        # val1 =str.format('1:%d'%result[1])
        # val2 = str.format('2:%f'%abs(result[2]))
        # print val,val1,val2


    # print '\nfractal: ', len(fractals), 'result: ', len(fractalsResult)
    return fractalsFliteredResult, target

def getTimeKeyFractals():
    fractals = getFractalsList()
    timekeyfractals = {}
    for ft in fractals:
        timekeyfractals[ft['quote']['time']] = ft
    return timekeyfractals


def buildTrainData():
    getTimeKeyFractals()

def High(i, quotes):
    return quotes[i].toDict()['close']

def Low(i,quotes):
    return quotes[i].toDict()['close']


def findUpFlag(i,quotes):
    bFound=False
    dCurrent=High(i,quotes)
    type = -1
    if dCurrent>High(i+1*type,quotes) and dCurrent>High(i+2*type,quotes) and dCurrent>High(i-1*type,quotes) and dCurrent>High(i-2*type,quotes):
        bFound=True
    Bars = len(quotes)
    # //----6 bars Fractal
    if not bFound:
        if dCurrent==High(i+1*type,quotes) and dCurrent>High(i+2*type,quotes) and dCurrent>High(i+3*type,quotes) and \
            dCurrent>High(i-1*type,quotes) and dCurrent>High(i-2*type,quotes):
            bFound=True
    # //----7 bars Fractal
    if not bFound:
        if dCurrent>=High(i+1*type,quotes) and dCurrent==High(i+2*type,quotes) and dCurrent>High(i+3*type,quotes) and dCurrent>High(i+4*type,quotes) and \
            dCurrent>High(i-1*type,quotes) and dCurrent>High(i-2*type,quotes):
            bFound=True

    # //----8 bars Fractal
    if not bFound:
        if dCurrent>=High(i+1*type,quotes) and dCurrent==High(i+2*type,quotes) and dCurrent==High(i+3*type,quotes) and dCurrent>High(i+4*type,quotes) and \
            dCurrent>High(i+5*type,quotes) and dCurrent>High(i-1*type,quotes) and dCurrent>High(i-2*type,quotes):
            bFound=True
    # //----8 bars Fractal
    if not bFound :
        if dCurrent>=High(i+1*type,quotes) and dCurrent==High(i+2*type,quotes) and dCurrent==High(i+3*type,quotes) and dCurrent==High(i+4*type,quotes) and \
            dCurrent>High(i+5*type,quotes) and dCurrent>High(i+6*type,quotes) and dCurrent>High(i-1*type,quotes) and dCurrent>High(i-2*type,quotes):
            bFound=True

    return bFound

def findDownFlag(i,quotes):
    bFound=False
    dCurrent=Low(i,quotes)
    type = -1
    if dCurrent<Low(i+1*type,quotes) and dCurrent<Low(i+2*type,quotes) and dCurrent < Low(i-1*type,quotes) and dCurrent<Low(i-2*type,quotes):
        bFound=True
    # //----6 bars Fractal
    if not bFound:
        if dCurrent==Low(i+1*type,quotes) and dCurrent<Low(i+2*type,quotes) and dCurrent<Low(i+3*type,quotes) and \
            dCurrent<Low(i-1*type,quotes) and dCurrent<Low(i-2*type,quotes):
            bFound=True
    # //----7 bars Fractal
    if not bFound:
        if dCurrent<=Low(i+1*type,quotes) and dCurrent==Low(i+2*type,quotes) and dCurrent<Low(i+3*type,quotes) and dCurrent<Low(i+4*type,quotes) and \
            dCurrent<Low(i-1*type,quotes) and dCurrent<Low(i-2*type,quotes):
            bFound=True

    # //----8 bars Fractal
    if not bFound:
        if dCurrent<=Low(i+1*type,quotes) and dCurrent==Low(i+2*type,quotes) and dCurrent==Low(i+3*type,quotes) and dCurrent<Low(i+4*type,quotes) and \
            dCurrent<Low(i+5*type,quotes) and dCurrent<Low(i-1*type,quotes) and dCurrent<Low(i-2*type,quotes):
            bFound=True
    # //----8 bars Fractal
    if not bFound:
        if dCurrent<=Low(i+1*type,quotes) and dCurrent==Low(i+2*type,quotes) and dCurrent==Low(i+3*type,quotes) and dCurrent==Low(i+4*type,quotes) and \
            dCurrent<Low(i+5*type,quotes) and dCurrent<Low(i+6*type,quotes) and dCurrent<Low(i-1*type,quotes) and dCurrent<Low(i-2*type,quotes):
            bFound=True

    return bFound

if __name__ == "__main__":
    # buildTrainData()
    svmtest()
