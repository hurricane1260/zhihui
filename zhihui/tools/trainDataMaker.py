__author__ = 'billzhou'
# this tool is used for crate train data from input quote data

from zhihui.web.extention.routing import route
from ultrafinance.dam.sqlDAM import SqlDAM, QuoteSql

def getSourceData():
    dam = SqlDAM()
    dam.setup({'db': 'sqlite:///../zhihui/data/ftest.sqlite'})
    dam.setSymbol('EURUSD')
    _quotes = dam.readQuotes(20000101, 20131231)
    return _quotes

def getFractalsData():
    _quotes = getSourceData()
    lastValue = 0
    lasttime = 0
    fractals = []
    for i in range(0, len(_quotes)):
        quoterow = _quotes[i].toDict()
        # print
        time = quoterow['time']
        if i > 9:
            flagrow = {}
            if findUpFlag(i, _quotes):
                found = True
                flagrow['index'] = i
                flagrow['findex'] = len(fractals)
                flagrow['quote'] = quoterow
                flagrow['type'] = 1
                fractals.append(flagrow)

            if findDownFlag(i, _quotes):
                found = True
                flagrow['index'] = i
                flagrow['findex'] = len(fractals)
                flagrow['quote'] = quoterow
                flagrow['type'] = 2
                fractals.append(flagrow)
        # print quoterow
    return fractals

def getFilteredFractalRow(index, fractals):
    if not index in range(1, len(fractals) -1):
        print [0,0,0,0]
        return [0,0,0,0]
    i = index
    ft = fractals[i]
    curindex = ft['index']
    curprice = ft['quote']['close']
    x1 = curindex - fractals[i-1]['index']
    x2 = fractals[i+1]['index'] - curindex
    y1 = curprice - fractals[i-1]['quote']['close']
    y2 = fractals[i-1]['quote']['close'] - curprice
    type = ft['type']
    if x1 >= 3 and x2 >= 3 and abs(y1) > 0.014 and abs(y2) > 0.014:
        result = [1,x1, y1, type]
    else:
        result = [0,x1, y1, type]
    print result
    return result

def getFilteredFractals():
    fractals = getFractalsData()

    # fromat:
    # [[use,x1,y1,type],
    #  [use,x1,y1,type]]
    fractalsResult = []

    for i in range(1, len(fractals)-1):
        ft = fractals[i]
        curindex = ft['index']
        curprice = ft['quote']['close']
        x1 = curindex - fractals[i-1]['index']
        x2 = fractals[i+1]['index'] - curindex
        y1 = curprice - fractals[i-1]['quote']['close']
        y2 = fractals[i-1]['quote']['close'] - curprice
        type = ft['type']

        if x1 >= 3 and x2 >= 3 and abs(y1) > 0.014 and abs(y2) > 0.014:
            result = [1,x1, y1, type]
        else:
            result = [0,x1, y1, type]
        fractalsResult.append(result)
        print result


    # print '\nfractal: ', len(fractals), 'result: ', len(fractalsResult)
    return fractalsResult

def getTimeKeyFractals():
    fractals = getFractalsData()
    timekeyfractals = {}
    for ft in fractals:
        timekeyfractals[ft['quote']['time']] = ft
    return timekeyfractals


def buildTrainData():
    getTimeKeyFractals()

def High(i, quotes):
    return quotes[i].toDict()['high']

def Low(i,quotes):
    return quotes[i].toDict()['low']


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
    buildTrainData()