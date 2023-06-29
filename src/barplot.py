import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from contrib.p4thpymisc.src.misc import asFunction


class BarPlot():

    @classmethod
    def barPlot(cls, df, catValMap, group=None, groupColor=None, xLabel=None, yLabel=None,
                color=None,
                fig=None,
                ax=None):
        _color = (lambda *_, **__: None) if color is None else asFunction(
            color, stringAsSingular=True)
        _group = (lambda row, *_, **__: None) if group is None else asFunction(
            group, stringAsSingular=True)
        _groupColor = (lambda row, *_, **__: None) if groupColor is None else asFunction(
            groupColor, stringAsSingular=True)
        if ax:
            _ax = ax
            _fig = ax.figure
        else:
            if not fig:
                _fig = plt.figure()
            else:
                _fig = fig
            _ax = _fig.add_subplot(1, 1, 1)

        width = 1.0 / (1.0+len(catValMap))
        dx = 0.0
        legend = {
            'handles': [],
        }
        xAxes = {
            'ticks': [],
            'labels': [],
            'colors': [],
        }
        yMin = None
        yMax = None
        for category, column in catValMap.items():
            print(category, column)
            for r, row in df.iterrows():
                yMax = row[column] if yMax is None or row[column] > yMax else yMax
                yMin = row[column] if yMin is None or row[column] < yMin else yMin

        yMin = yMin - 0.1 * (yMax-yMin)
        for category, column in catValMap.items():
            col = _color(category, column) if len(catValMap) > 1 else None
            legend['handles'].append(Patch(color=col, label=category))
            for r, row in df.iterrows():
                x = 1.0*r + dx
                if (x == 1.0*r):
                    xAxes['ticks'].append(x)
                    xAxes['labels'].append(' ' + _group(row))
                    xAxes['colors'].append(_groupColor(row))

                _ax.bar(x, row[column]-yMin, bottom=yMin,
                        color=_groupColor(row) if col is None else col, width=width)
            dx = dx + width

        _ax.axes.xaxis.set_ticks([])
        _ax.axes.set_xlabel(xLabel)
        _ax.axes.set_ylabel(yLabel)
        if len(catValMap) > 1:
            _ax.legend(**legend)
        else:
            _ax.plot([], [], lw=0, marker='', label=list(catValMap.keys())[0])
            _ax.legend(handlelength=0.0, handletextpad=0)
        for i, x in enumerate(xAxes['ticks']):
            _ax.text(x, yMin - 0.0 * (yMax - yMin),
                     s=xAxes['labels'][i], color=xAxes['colors'][i], ha='center', va='top', rotation=-90)
        return _ax, _fig
