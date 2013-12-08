# coding=utf-8

import csv
from ultrafinance.dam.sqlDAM import SqlDAM
from ultrafinance.model import Quote
import time
import logging
LOG = logging.getLogger()

def loadCsvToSqlDam(path):
    """
    convert csv format data to database
    """
    print path
    dam = SqlDAM()
    dam.setup({'db': "sqlite:///../../data/ftest.sqlite"})
    dam.setSymbol('EURUSD')
    with open(path, "rb") as csvfile:
        _csvReader = csv.reader(csvfile)
        quotes = []
        for row in _csvReader:
            newrow = []
            for col in row:
                newrow.append(col)
            newrow[0] = time.strftime('%Y%m%d', time.strptime(newrow[0], '%Y.%m.%d'))
            quote = Quote(newrow[0], newrow[2], newrow[3], newrow[4], newrow[5], newrow[6], newrow[5])
            quotes.append(quote)
        dam.writeQuotes(quotes)
        dam.commit()


def loadMt4CsvToSqlDam(path):
    """
    convert mt4 csv format data to database
    mt4 csv format:
    <TICKER>,<DTYYYYMMDD>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>
    EURUSD,20010102,230100,0.9507,0.9507,0.9507,0.9507,4
    EURUSD,20010102,230200,0.9506,0.9506,0.9505,0.9505,4
    EURUSD,20010102,230300,0.9505,0.9507,0.9505,0.9506,4
    """
    print path
    dam = SqlDAM()
    dam.setup({'db': "sqlite:///../../data/ftest.sqlite"})
    dam.setSymbol('EURUSD')
    skipfirst = True
    with open(path, "rb") as csvfile:
        _csvReader = csv.reader(csvfile)

        count = 0
        total_count = 0;
        for row in _csvReader:
            if(skipfirst):
                skipfirst = False
                continue

            newrow = []
            for col in row:
                newrow.append(col)
            # newrow[0] = time.strftime('%Y%m%d', time.strptime(newrow[0], '%Y.%m.%d'))
            quotes = []
            quote = Quote(newrow[1]+newrow[2], newrow[3], newrow[4], newrow[5], newrow[6], newrow[7], newrow[6])
            quotes.append(quote)
            dam.writeQuotes(quotes)
            count += 1
            if(count >= 5000):
                total_count += count
                count = 0
                dam.commit()
                print 'dam committed: '+total_count
        dam.commit()

        # dam.writeQuotes(quotes)
        # dam.commit()

# if __name__ == "__main__":
#     loadCsvToSqlDam("../../data/eurusd.csv")