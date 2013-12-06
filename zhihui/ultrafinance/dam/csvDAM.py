# coding=utf-8

import os
import csv
from ultrafinance.dam.baseDAM import BaseDAM
from ultrafinance.dam.excelLib import ExcelLib
from ultrafinance.model import TICK_FIELDS, QUOTE_FIELDS, Quote, Tick
from ultrafinance.lib.errors import UfException, Errors

#from os import path

import logging
LOG = logging.getLogger()


class CsvDAM(BaseDAM):
    """
        Csv DAO
    """
    QUOTE = 'quote'
    TICK = 'tick'

    def __init__(self):
        """ constructor """
        super(CsvDAM, self).__init__()
        self.__dir = None

    def targetPath(self,kind):
        """

        :param kind:
        :return:
        """
        #return os.path.join(self.__dir, "%s-%s.csv" % (self.symbol, kind))
        return os.path.join(self.__dir, "%s.csv" % (self.symbol,))

    def __readData(self, targetPath, start, end):
        """ read data """
        ret = []
        if not os.path.exists(targetPath):
            LOG.error("Target file doesn't exist: %s" % os.path.abspath(targetPath) )
            return ret

        with os.open(targetPath, 'rb') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                ret.append(row)
        return ret

    def __writeData(self, targetPath, fields, rows):
        """ write data """
        if os.path.exists(targetPath):
            LOG.error("Target file exists: %s" % os.path.abspath(targetPath) )
            raise UfException(Errors.FILE_EXIST, "can't write to a existing file") #because xlwt doesn't support it

        with os.open(targetPath, 'wb') as csvfile:
            csv_writer = csvfile.writerows(rows)


    def readQuotes(self, start, end):
        """ read quotes """
        quotes = self.__readData(self.targetPath(), start, end)
        return [Quote(*quote) for quote in quotes]

    def writeQuotes(self, quotes):
        """ write quotes """
        self.__writeData(self.targetPath(),
                         QUOTE_FIELDS,
                         [[getattr(quote, field) for field in QUOTE_FIELDS] for quote in quotes])

    def readTicks(self, start, end):
        """ read ticks """
        ticks =  self.__readData(self.targetPath(), start, end)
        return [Tick(*tick) for tick in ticks]

    def writeTicks(self, ticks):
        """ read quotes """
        self.__writeData(self.targetPath(),
                         TICK_FIELDS,
                         [[getattr(tick, field) for field in TICK_FIELDS] for tick in ticks])

    def setDir(self, path):
        """ set dir """
        self.__dir = path


def testCSV(path):
    """
    testCSV
    """
    print path

    with open(path, "rb") as csvfile:
        _csvReader = csv.reader(csvfile)
        for row in _csvReader:
            print row

if __name__ == "__main__":
    testCSV("../../data/EURUSD20130101-20131112.csv")