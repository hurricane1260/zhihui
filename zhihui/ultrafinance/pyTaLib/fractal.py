__author__ = 'billzhou'

from ultrafinance.dam.sqlDAM import SqlDAM
import time

class Fractal(object):
    FractalDirect = {
        'none': 0,
        'up': 1,
        'down': 2
    }
    __fractals = []

    def __init__(self, pricetype = 'close'):
        self.__pricetype = pricetype

    def __call__(self, quotes):
        if len(quotes) < 10:
            return self.__fractals
        for i in range(0, len(quotes)):
            quote = quotes[i]
            type = self.FractalDirect['none']
            if findUpFlag(i, quotes):
                type = self.FractalDirect['up']
            elif findDownFlag(i, quotes):
                type = self.FractalDirect['down']

            if type != self.FractalDirect['none']:
                fractal = {}
                fractal['time'] = quote.time
                fractal['type'] = type
                fractal['price'] = quote.toDict()[self.__pricetype]
                self.__fractals.append(fractal)

        return self.__fractals



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

selectFractalData =[1382630400000,1378310400000,1376928000000,1373299200000,1371484800000,1371052800000,1369670400000,1369152000000,1368720000000,1367337600000,1367942400000,1364313600000,1364313600000,1364832000000,1359648000000,1357142400000,1357660800000,1359648000000,1357660800000,1357142400000,1354809600000,1352736000000,1350403200000,1349798400000,1347552000000,1343059200000,1346688000000,1340121600000,1340899200000,1338393600000,1335715200000,1332691200000,1333036800000,1331654400000,1330012800000,1331136000000,1329235200000,1328716800000,1326643200000,1325779200000,1319644800000,1317571200000,1317225600000,1316016000000,1314547200000,1311609600000,1312387200000,1309708800000,1310400000000,1310400000000,1308844800000,1307376000000,1306080000000,1306080000000,1304265600000,1303056000000,1300982400000,1297699200000,1294329600000,1293724800000,1291046400000,1291046400000,1288800000000,1288800000000,1286985600000,1283788800000,1281024000000,1277740800000,1279641600000,1275840000000,1271174400000,1272556800000,1269446400000,1263139200000]
selectFractalData2 = [1128355200000, 11128528000000, 21129824000000, 31130342400000, 41130860800000, 51132070400000, 61134662400000, 71135094400000, 81135612800000, 91136476800000, 1137600000000, 11137945600000, 11138636800000, 11139500800000, 11140969600000, 11141228800000, 11142524800000, 11143043200000, 11143475200000, 11144166400000, 21144771200000, 21147363200000, 1149177600000, 1150128000000, 1150992000000, 1152201600000, 1153152000000, 1154620800000, 1155484800000, 1156089600000, 1156435200000, 1157299200000, 1157644800000, 1159718400000, 1160668800000, 1165161600000, 1165852800000, 1167667200000, 1168444800000, 1173369600000, 1174406400000, 1176048000000, 1177603200000, 1179158400000, 1180972800000, 1181577600000, 1184860800000, 1185465600000, 1186502400000, 1187625600000, 1192982400000, 1196006400000, 1198080000000, 1200240000000, 1200844800000, 1202313600000, 1205683200000, 1208793600000, 1210780800000, 1211299200000, 1222012800000, 1228406400000, 1229443200000, 1236182400000, 1237392000000, 1240156800000, 1242316800000, 1243872000000, 1251734400000, 1253548800000, 1254326400000, 1256140800000, 1259078400000, 1261411200000, 1260374400000, 1264348800000, 1272556800000, 1273420800000, 1283788800000, 1288800000000, 1291046400000, 1291305600000, 1293724800000, 1294329600000, 1295193600000, 1303056000000, 1304265600000, 1308844800000, 1309708800000, 1310400000000, 1311609600000, 1314547200000, 1317571200000, 1319644800000, 1320940800000, 1326643200000, 1327593600000, 1330012800000, 1331654400000, 1335715200000, 1340899200000, 1346688000000, 1347552000000, 1351526400000, 1352736000000, 1353945600000, 1357660800000, 1359648000000, 1364832000000, 1367942400000, 1369670400000, 1371484800000, 1373299200000, 1377532800000, 1378310400000, 1381766400000, 1382630400000, 1383840000000]

class FractalSelectManager(object):

    __filteredDict = {}

    def __init__(self, fractalTimeKey = selectFractalData):
        self.__selectData = fractalTimeKey
        for data in self.__selectData:
            gmtime = time.gmtime(data/1000+24*60*60)
            timestr = '%4d%02d%02d' % (gmtime.tm_year, gmtime.tm_mon, gmtime.tm_mday)
            key = int(timestr)
            self.__filteredDict[key] = data

    def isSelected(self, time):
        if time in self.__filteredDict:
            return True
        else:
            return False


def getSourceData():
    dam = SqlDAM()
    dam.setup({'db': 'sqlite:///../../../zhihui/data/ftest.sqlite'})
    dam.setSymbol('EURUSD')
    _quotes = dam.readQuotes(20000101, 20131231)
    return _quotes

if __name__ == "__main__":
    fractal = Fractal()
    quotes = getSourceData()
    print fractal(quotes)