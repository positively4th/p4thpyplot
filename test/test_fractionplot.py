import unittest
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import uniform

from src.fractionplot import FractionPlot


class TestFractionPlot(unittest.TestCase):

    def testFractionPlot(self):
        # fractionPlots
        N = 10
        df = pd.DataFrame()
        df['label'] = [str(i*i) for i in range(N)]
        df['1'] = 1.0
        df['x'] = uniform(loc=1, scale=10).rvs(N)
        df['0x'] = df['1'] * [v for v in range(N)] + 2
        df['0y'] = df['1'] * [v for v in range(N)] + 1
        df['45x'] = 2 * df['x']
        df['45y'] = uniform(loc=0, scale=1).rvs(N) * df['45x']
        df['90x'] = 3 * df['x']
        df['90y'] = uniform(loc=0, scale=1).rvs(N) * df['90x']
        df['135x'] = 4 * df['x']
        df['135y'] = uniform(loc=0, scale=1).rvs(N) * df['135x']
        df['180x'] = 5 * df['x']
        df['180y'] = uniform(loc=0, scale=1).rvs(N) * df['180x']
        df['225x'] = 6 * df['x']
        df['225y'] = uniform(loc=0, scale=1).rvs(N) * df['225x']
        df['270x'] = 7 * df['x']
        df['270y'] = uniform(loc=0, scale=1).rvs(N) * df['270x']
        df['315x'] = 8 * df['x']
        df['315y'] = uniform(loc=0, scale=1).rvs(N) * df['315x']

        ax, fig = FractionPlot.fractionPlots(df, [

            {
                'area': '1',
                'label': '0-45',
                'xColumn': '0x',
                'yColumn': '0y',
                'xLabel': '0-45',
                'yLabel': '0.9',
            },


            {
                'area': '2',
                'label': '45-90',
                'xColumn': '45x',
                'yColumn': '45y',
                'xLabel': '45-90',
                'yLabel': '0.45',
            },

            {
                'area': '3',
                'label': '90-135',
                'xColumn': '90x',
                'yColumn': '90y',
                'xLabel': '90-135',
                'yLabel': '0.225',
            },

            {
                'area': '4',
                'label': '135-180',
                'xColumn': '135x',
                'yColumn': '135y',
                'xLabel': '135-180',
                'yLabel': '0.225/2',
            },

            {
                'area': '5',
                'label': '180-225',
                'xColumn': '180x',
                'yColumn': '180y',
                'xLabel': '180-225',
                'yLabel': '0.225/4',
            },

            {
                'area': '6',
                'label': '225-270',
                'xColumn': '225x',
                'yColumn': '225y',
                'xLabel': '225-270',
                'yLabel': '0.225/8',
            },

            {
                'area': '7',
                'label': '270-315',
                'xColumn': '270x',
                'yColumn': '270y',
                'xLabel': '270-315',
                'yLabel': '0.225/16',
            },

            {
                'area': '8',
                'label': '315-360',
                'xColumn': '315x',
                'yColumn': '315y',
                'xLabel': '315-360',
                'yLabel': '0.225/32',
            }
        ], labelGetter=lambda row, xColumn, yColumn, i, *_, **__: str(i) + ': (' + xColumn + ',' + yColumn + ')'
        )
        plt.show()


if __name__ == '__main__':
    unittest.main()
