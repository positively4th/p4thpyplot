import unittest
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.stats import uniform


from src.tools import Tools
from src.barplot import BarPlot


class TestBarPlot(unittest.TestCase):

    def testBarPlot(self):
        # barPlot
        N = 10
        df = pd.DataFrame()
        df['uniform'] = uniform(loc=0, scale=1).rvs(10)
        df['normal'] = norm(loc=0, scale=1).rvs(10)
        df['group'] = range(10)

        catColorGetter = Tools.createColorGetter()
        grpColorGetter = Tools.createColorGetter()

        ax, fig = BarPlot.barPlot(df, {
            'Uniform': 'uniform',
            'Normal': 'normal'
        }, xLabel='X', yLabel='Y',
            color=lambda cat, row: catColorGetter(cat),
            group=lambda row, *_: str(row['group']),
            groupColor=lambda row, *_: grpColorGetter(row['group']),
        )

        plt.show()


if __name__ == '__main__':
    unittest.main()
