import unittest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.stats import uniform

from src.seriesplot import SeriesPlot


class TestSeriesPlot(unittest.TestCase):

    def testSeriesPlot(self):
        # seriesPlot
        N = 50
        df = {}
        df = pd.DataFrame(df)
        df['x'] = uniform(loc=0, scale=365).rvs(N)
        df['group'] = (['even' if int(x) % 2 == 0 else 'odd' for x in df['x']])
        df['y'] = [np.log(x) + (1.0 if int(x) % 2 == 0 else -1.0)
                   * norm(loc=1, scale=0.1).rvs() for x in df['x']]

        ax, fig = SeriesPlot.seriesPlot(df,
                                        xLabel='Week',
                                        yLabel='Y',
                                        x=lambda r, *_: r['x'],
                                        y=lambda r, g, *
                                        _: np.log(r['x']) if g == 'x' else r['y'],
                                        group=lambda r, *_: ('x', r['group']),
                                        sort=lambda r, g, *_: r['x'],
                                        lineOpts=lambda g, *_: None if g == 'x' else {
                                            'linewidth': 1.0,
                                            'linestyle': 'dashed' if g == 'even' else 'dotted',
                                            'color': 'green' if g == 'even' else 'red',
                                        },
                                        pointOpts=lambda r, g: None if g == 'x' else {
                                            'marker': '+' if r['x'] > 182 else 'x',
                                            'color': 'red' if g == 'even' else 'green',
                                        },
                                        text=lambda r, g: None if g == 'x' or uniform().rvs() < 0.7 else {
                                            'txt': 'T',
                                            'color': 'red' if g == 'even' else 'green',
                                        },
                                        xTicks=lambda xs, groups, XAxis: [
                                            {'tick': x, 'label': str(
                                                round(x, 2))}
                                            for x in np.linspace(min(XAxis.get_ticklocs()), max(XAxis.get_ticklocs()), 3)
                                        ],
                                        lineLegend=lambda group: None if group == 'x' else (
                                            'ODD' if group == 'odd' else 'EVEN'),
                                        ellipse=lambda r, g, *_: None if g == 'x' else {
                                            'left': 0.9 * r['x'],
                                            'right': 1.1 * r['x'],
                                            'bottom': 0.8 * r['y'],
                                            'top': 1.2 * r['y'],
                                            'height': 0.5 * (r['y']-np.log(r['y'])),
                                            'alpha': 0.2,
                                            'linewidth': 1,
                                            'color': 'purple',
                                        },
                                        box=lambda r, g, *_: None if g == 'x' else {
                                            'left': 0.9 * r['x'],
                                            'right': 1.1 * r['x'],
                                            'bottom': 0.8 * r['y'],
                                            'top': 1.2 * r['y'],
                                            'height': 0.5 * (r['y']-np.log(r['y'])),
                                            'alpha': 0.2,
                                            'linewidth': 1,
                                            'color': 'purple',
                                        },
                                        cross=lambda r, g, *_: None if g == 'x' else {
                                            'left': 0.9 * r['x'],
                                            'right': 1.1 * r['x'],
                                            'bottom': 0.8 * r['y'],
                                            'top': 1.2 * r['y'],
                                            'height': 0.5 * (r['y']-np.log(r['y'])),
                                            'alpha': 0.2,
                                            'linewidth': 1,
                                            'color': 'purple',
                                        },
                                        )

        plt.show()


if __name__ == '__main__':
    unittest.main()
