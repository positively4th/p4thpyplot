import unittest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

from src.scatterplot import ScatterPlot


class TestScatterPlot(unittest.TestCase):

    def testScatterPlot(self):

        # scatterPlot

        N = 20
        df = {}
        df = pd.DataFrame(df)
        df['i'] = [1.0] * N
        df['xExp'] = norm(loc=1, scale=1).rvs(N)
        df['x'] = df['xExp'] + norm(loc=0, scale=0.5).rvs(N)

        df['yExp'] = df['i'] + 2 * df['xExp']
        df['y'] = df['i'] + 2 * df['x'] + norm(loc=0, scale=10).rvs(N)
        print(df)
        ax, fig = ScatterPlot.plot(df,
                                   xLabel='Observed x',
                                   yLabel=lambda *_, **__: 'Observed y',
                                   x=lambda r, *_: r['x'],
                                   y=lambda r, *_: r['y'],
                                   color=lambda r, *
                                   _: 'green' if r['y'] >= r['yExp'] else 'red',
                                   text=lambda r, i, *
                                   _: 'Point ' + str(i),
                                   ellipse=lambda r, *_: {
                                       'width': r['x']-r['xExp'],
                                       'height': r['y']-r['yExp'],
                                       'alpha': 0.1,
                                       'linewidth': 1,
                                       'edgecolor': 'blue',
                                   },
                                   box=lambda r, *_: {
                                       'width': r['x']-r['xExp'],
                                       'height': r['y']-r['yExp'],
                                       'alpha': 0.1,
                                       'linewidth': 1,
                                       'edgecolor': 'green',
                                   },
                                   cross=lambda r, *_: {
                                       'width': r['x']-r['xExp'],
                                       'height': r['y']-r['yExp'],
                                       'alpha': 1,
                                       'linewidth': 1,
                                       'color': 'orange',
                                   },
                                   ols=lambda rows, *_, **__: [
                                       {
                                           'xys': [(r['x'], r['x']) for r in rows if r['x'] <= np.mean(df['x'])],
                                           'alpha': 1,
                                           'linewidth': 1,
                                           'color': 'gold',
                                       }, {
                                           'xys': [(r['x'], r['x']) for i, r in df.iterrows() if r['x'] > np.mean(df['x'])],
                                           'alpha': 1,
                                           'linewidth': 1,
                                           'color': 'purple',
                                       },
                                   ],
                                   rays=lambda r, i, *_: [
                                       {'x': 0.90 * r['x'], 'y': 0.9 * r['y'],
                                        'line': {'linestyle': ':'},
                                        } if i % 4 == 0 else (
                                           {'x': 1.10 * r['x'], 'y': 1.1 * r['y'],
                                            'point': {'marker': '+'}
                                            } if i % 4 == 1 else (
                                               {'x': 1.10 * r['x'], 'y': 1.1 * r['y'],
                                                'arrow': {'color': 'purple', 'head_starts_at_zero': True}
                                                } if i % 4 == 2 else None
                                           )
                                       )
                                   ],
                                   limits=lambda xs, ys, ax: {
                                       'bottom': -2,
                                   }
                                   )

        plt.show()


if __name__ == '__main__':
    unittest.main()
