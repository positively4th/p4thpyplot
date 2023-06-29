import numpy as np
import matplotlib.pyplot as plt

from contrib.p4thpymisc.src.misc import asFunction
from contrib.p4thpymisc.src.misc import filterByKey

from .tools import Tools


class ScatterPlot():

    @classmethod
    def plot(cls,
             df,
             xLabel: lambda: None,
             yLabel: lambda: None,
             x=lambda row, i: None,
             y=lambda row, i: None,
             color=lambda row, i: 'black',
             xTicks=None,
             yTicks=None,
             limits=None if True else lambda xs, ys, ax: {
                 'left': np.min(xs),
                 'right': np.max(xs),
                 'top': np.max(ys),
                 'bottom': np.min(ys),
             },
             markerSize=lambda row, i: None,
             marker=lambda row, i: '.',
             text=lambda row, i: None,
             ellipse=lambda row, i: None,
             box=lambda row, i: None,
             cross=lambda row, i: None,
             ols=lambda *_, **__: None,
             rays=lambda row, i: [],
             verticalMean=None,
             horizontalMean=None,
             verticalMedian=None,
             horizontalMedian=None,
             ax=None
             ):
        if not ax:
            _fig = plt.figure()
            _ax = _fig.add_subplot(1, 1, 1)
        else:
            _ax = ax
            _fig = ax.figure

        _xLabel = asFunction(xLabel)
        _yLabel = asFunction(yLabel)

        _x = asFunction(x)
        _y = asFunction(y)
        _color = asFunction(color)
        _marker = asFunction(marker)
        _markerSize = asFunction(markerSize)
        _ellipse = asFunction(ellipse)
        _cross = asFunction(cross)
        _rays = asFunction(rays)

        xys = []
        xs = []
        ys = []

        xxLabel = _xLabel()
        if xxLabel:
            _ax.set_xlabel(xxLabel)

        yyLabel = _yLabel()
        if yyLabel:
            _ax.set_ylabel(yyLabel)

        for i, row in df.iterrows():
            xx = _x(row, i)
            yy = _y(row, i)
            pointSpec = {
                'color': _color(row, i),
                'marker': _marker(row, i),
                'markersize': _markerSize(row, i),
            }

            if text:
                _text = asFunction(text)
                ttext = _text(row, i)
                Tools._plotText(_ax, xx, yy, ttext,
                                filterByKey(pointSpec, ['color']))

            if ellipse:
                eellipse = _ellipse(row, i)
                Tools._plotEllipse(_ax, xx, yy, eellipse)

            if box:
                _box = asFunction(box)
                Tools._plotBox(_ax, xx, yy, _box(row, i))

            for ray in _rays(row, i):
                Tools._plotRay(_ax, xx, yy, ray)

            ccross = _cross(row, i)
            if ccross:
                Tools._plotCross(_ax, xx, yy, ccross)

            _ax.plot([xx], [yy], **pointSpec)
            xys.append([xx, yy])
            xs.append(xx)
            ys.append(yy)

        xMin = min(xs)
        xMax = max(xs)
        yMin = min(ys)
        yMax = max(ys)

        if verticalMedian:
            xMedian = np.median(xs)
            _ax.plot((xMedian, xMedian), (yMin, yMax), **verticalMedian)

        if horizontalMedian:
            yMedian = np.median(ys)
            _ax.plot((xMin, xMax), (yMedian, yMedian), **horizontalMedian)

        if verticalMean:
            xMean = np.mean(xs)
            _ax.plot((xMean, xMean), (yMin, yMax), **verticalMean)

        if horizontalMean:
            yMean = np.mean(ys)
            _ax.plot((xMin, xMax), (yMean, yMean), **horizontalMean)

        if ols:
            _ols = asFunction(ols)
            ools = _ols(
                *list(zip(  # Transpose
                    *[(row, i, _x(row, i), _y(row, i)) for i, row in df.iterrows()]
                ))
            )
            Tools._plotOLS(_ax, ools, xys)

        if limits:
            _limits = asFunction(limits)
            Tools._setLimits(_ax, _limits(xs, ys, _ax))

        if xTicks:
            _xTicks = asFunction(xTicks)
            ticks = Tools._setTicks(_ax.xaxis, _xTicks(xs, _ax.xaxis))

        if yTicks:
            _yTicks = asFunction(yTicks)
            ticks = Tools._setTicks(_ax.yaxis, _yTicks(ys, _ax.yaxis))

        return _ax, _fig
