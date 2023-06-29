from collections import OrderedDict
import unittest
import pandas as pd
import matplotlib.pyplot as plt

from src.radarplot import RadarPlot


class TestRadarPlot(unittest.TestCase):

    def testRadarPlot(self):
        # radarPlot

        df = pd.DataFrame(OrderedDict([
            ('id', ['Blue Heighty', 'Red Widthy', 'Green Depthy']),
            ('h', [80, 20, 10, ]),
            ('w', [20, 60, 15, ]),
            ('d', [10, 5, 40, ]),
        ]))
        axes = OrderedDict((
            ('Height', 'h'),
            ('Width', 'w'),
            ('Depth', 'd'),
        ))

        colors = {
            'Blue Heighty': 'b',
            'Red Widthy': 'r',
            'Green Depthy': 'g'
        }

        def color(i, row): return colors[row['id']]
        def label(i, row): return row['id']

        # print(df);
        fig = plt.figure(figsize=(2*16, 1*16), dpi=None, facecolor=None, edgecolor=None, linewidth=0.0,
                         frameon=None, subplotpars=None, tight_layout=None, constrained_layout=None)
        fig = RadarPlot.radarPlot(df, axes, color=color,
                                  title='Plot TL', fig=fig, subplotargs=(2, 2, 1))
        fig = RadarPlot.radarPlot(df, axes, label=label, color=color,
                                  title='Plot TR', fig=fig, subplotargs=(2, 2, 2))
        fig = RadarPlot.radarPlot(df, axes, color=color,
                                  title='Plot BL', fig=fig, subplotargs=(2, 2, 3))
        fig = RadarPlot.radarPlot(df, axes, color=color, title='Plot BR', fig=fig, subplotargs=(2, 2, 4), minAxisFormater=None, maxAxisFormater=None,
                                  text=lambda val, axisLabel, axisKey, row: '{} {} {} {}'.format(str(val), axisLabel, str(axisKey), str(row[axisKey])))
        plt.show()

        # Scale to always min max
        fig = RadarPlot.radarPlot(df, axes, color=color, title='Plot',
                                  scaler=RadarPlot.minMaxScaler)
        plt.show()


if __name__ == '__main__':
    unittest.main()
