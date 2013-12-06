# coding=utf-8

'''
Created on Nov 27, 2011

@author: ppa
'''
import unittest

import os
from ultrafinance.model import Tick, Quote
from ultrafinance.dam.csvDAM import CsvDAM


class testCSVDAM(unittest.TestCase):
    """
        test CSV DAM
    """
    def setUp(self):
        """

            setup
        """
        self.targetPath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
        print self.targetPath
        self.symbol = 'eurusd'

    def tearDown(self):
        """
            setup

        """
        pass

    def testWriteExcel(self):
        """

            test write
        """
        writeDam = CsvDAM()
        writeDam.setDir(self.targetPath)
        writeDam.setSymbol(self.symbol)

        for f in [writeDam.targetPath(CsvDAM.QUOTE), writeDam.targetPath(CsvDAM.TICK)]:
            if os.path.exists(f):
                os.remove(f)

        quote1 = Quote('2014.09.21', '00:00', '32.58', '32.58', '32.57', '32.57', '65212', None)
        quote2 = Quote('2014.09.22', '00:00', '32.59', '32.59', '32.58', '32.58', '65213', None)
        tick1 = Tick('2014.10.21', '00:00', '32.58', '32.58', '32.57', '32.57', '65212')
        tick2 = Tick('2014.10.22', '00:00', '32.59', '32.59', '32.58', '32.58', '65213')
        writeDam.writeQuotes([quote1, quote2])
        writeDam.writeTicks([tick1, tick2])

    def testReadCSV(self):
        """
            test read

        """
        readDam = CsvDAM()
        readDam.setDir(self.targetPath)
        readDam.setSymbol(self.symbol)

        print(readDam.readQuotes('2002.01.01', '2020.01.01'))
        print(readDam.readTicks('2002.01.01', '2020.01.01'))


def main():
    """
        main
    """
    unittest.main()

if __name__ == '__main__':
    main()