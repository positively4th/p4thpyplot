import numpy as np
import uuid
import matplotlib.pyplot as plt
import pandas as pd

from contrib.p4thpymisc.src.misc import asFunction
from contrib.p4thpymisc.src.misc import filterByKey

from .tools import Tools


class SeriesPlot():

    def uuid(): return str(uuid.uuid4())

    @classmethod
    def seriesPlot(cls, df,
                   xLabel=lambda: 'X',
                   yLabel=lambda: 'Y',
                   y=lambda row, group: row['y'],
                   x=lambda row, group: row['x'],
                   group=lambda row: None,
                   sort=lambda row, group: None,
                   lineOpts=lambda group: {},
                   pointOpts=lambda row, group: {},
                   text=lambda row, group: {
                       'txt': 'o',
                       'color': 'red',
                   },
                   xTicks=lambda xs, groups, XAxis: [
                       {'tick': x, 'label': str(round(x, 2))}
                       for x in np.linspace(min(XAxis.get_ticklocs()), max(XAxis.get_ticklocs()), 10)
                   ],
                   yTicks=lambda ys, groups, YAxis: [
                       {'tick': y, 'label': str(round(y, 2))} for y in ys],
                   lineLegend=lambda group: group,
                   ellipse=lambda row, group: None,
                   box=None,
                   cross=lambda row, group: None,
                   fig=None,
                   ax=None
                   ):
        groupColumn = str(cls.uuid())
        sortColumn = str(cls.uuid())

        _x = asFunction(x, stringAsSingular=True)
        _y = asFunction(y, stringAsSingular=True)
        _group = asFunction(group, stringAsSingular=True)
        _sort = asFunction(sort, stringAsSingular=True)
        _lineOpts = asFunction(lineOpts, stringAsSingular=True)
        _pointOpts = asFunction(pointOpts, stringAsSingular=True)

        def groupHelper(row, *_):
            g = _group(row)
            g = tuple((g,)) if isinstance(g, str) else g
            g = [] if g is None else g
            return g

        ticksMeta = {
            'xs': [],
            'ys': [],
            'groups': [],
        }

        if ax:
            _ax = ax
            _fig = ax.figure
        else:
            if not fig:
                _fig = plt.figure()
            else:
                _fig = fig
            _ax = _fig.add_subplot(1, 1, 1)

        _df = df.copy()
        _df[groupColumn] = [groupHelper(row) for i, row in df.iterrows()]
        # print(_df[groupColumn].values)
        allGroups = set([group for groups in _df[groupColumn]
                        for group in groups])
        while len(allGroups) > 0:
            g = allGroups.pop()

            gdf = []
            for i, row in _df.iterrows():
                if g in row[groupColumn]:
                    gdf.append(row)
            gdf = pd.DataFrame(gdf, columns=_df.columns)
            # gdf = P4thPDF(_df.copy()).keepRows(
            #     lambda row: g in row[groupColumn]).state
            # gdf = gdf.reset_index()
            if not sort is None:
                gdf[sortColumn] = [_sort(row, g) for i, row in gdf.iterrows()]
                # print(gdf[sortColumn].values, gdf['fixtureDate'].values, g)
                gdf = gdf.sort_values(sortColumn)
            # print(gdf)

            xs = []
            ys = []
            for i, row in gdf.iterrows():
                xx = x(row, g)
                yy = y(row, g)
                ticksMeta['xs'].append(xx)
                ticksMeta['ys'].append(yy)
                ticksMeta['groups'].append(g)
                xs.append(xx)
                ys.append(yy)
                po = _pointOpts(row, g)
                po = {} if po is None else po
                _ax.plot(xx, yy, **po)
                # print(xx,yy, row[sortColumn])

                if text:
                    _text = asFunction(text, stringAsSingular=True)
                    ttext = _text(row, g)
                    Tools._plotText(_ax, xx, yy, ttext,
                                    filterByKey(po, ['color'])
                                    )

                if cross:
                    _cross = asFunction(cross, stringAsSingular=True)
                    Tools._plotCross(_ax, xx, yy, _cross(row, g))

                if ellipse:
                    _ellipse = asFunction(
                        ellipse, stringAsSingular=True)
                    Tools._plotEllipse(_ax, xx, yy, _ellipse(row, g))

                if box:
                    _box = asFunction(box, stringAsSingular=True)
                    Tools._plotBox(_ax, xx, yy, _box(row, g))

            lo = _lineOpts(g)
            lo = {} if lo is None else lo
            # print(lo, 'lineOpts')
            line, = _ax.plot(xs, ys, **lo)
            if lineLegend:
                _lineLegend = asFunction(
                    lineLegend, stringAsSingular=True)
                line.set_label(_lineLegend(g))

        if xTicks:
            _xTicks = asFunction(xTicks, stringAsSingular=True)
            ticks = Tools._setTicks(_ax.xaxis, _xTicks(
                ticksMeta['xs'], ticksMeta['groups'], _ax.xaxis))

        if yTicks:
            _yTicks = asFunction(yTicks, stringAsSingular=True)
            ticks = Tools._setTicks(_ax.yaxis, _yTicks(
                ticksMeta['ys'], ticksMeta['groups'], _ax.yaxis))

        if lineLegend:
            _ax.legend()

        if xLabel:
            _xLabel = asFunction(xLabel, stringAsSingular=True)
            _ax.set_xlabel(_xLabel())

        if yLabel:
            _yLabel = asFunction(yLabel, stringAsSingular=True)
            _ax.set_ylabel(_yLabel())
        return _ax, _fig
