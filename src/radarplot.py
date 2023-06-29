from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt
import math

from contrib.p4thpymisc.src.misc import asFunction
from contrib.p4thpymisc.src.misc import items

from .tools import Tools


class RadarPlot():

    @staticmethod
    def minMaxScaler(val, key, min, max, avg, med):
        # print(val, key, min, max, avg, med, float(val - min) / float(max - min))
        if max == min:
            return val

        return (float(val) - float(min)) / (float(max) - float(min))

    @staticmethod
    def insideOutScaler(val, key, min, max, avg, med):
        # print(val, key, min, max, avg, med, float(val - min) / float(max - min))
        # if max == min:
        #    return val
        return float(max) - float(val) + float(min)

    @classmethod
    def radarPlot(cls, df,
                  axes=OrderedDict(
                      {'Height': 'h', 'Width': 'w', 'Depth': 'd', }),
                  color=['b', 'r', 'g'],
                  # format=lambda v: str(v),
                  label=lambda i, row: str(i),
                  scaler=lambda val, col, min, max, avg, med: val,
                  title=None,
                  legend=None,
                  fig=None,
                  ax=None,
                  line=lambda i, row: {},
                  text=lambda val, axisLabel, axisKey, row: None,
                  minAxisFormater=lambda v, axisColumn: str(v),
                  maxAxisFormater=lambda v, axisColumn: str(v),
                  yTicks=None,
                  yMax=None,
                  subplotargs=(1, 1, 1),
                  subplotkwargs={'polar': True}
                  ):

        def scalerHelper(*_, **__):
            res = scaler(*_, **__)
            # print(res)
            if not isinstance(res, (list, tuple)):
                return (res, res)
            return res

        _fig = plt.figure() if fig is None else fig
        _fig.tight_layout()

        _color = asFunction(color, stringAsSingular=True)
        _line = asFunction(line, stringAsSingular=True)
        _label = asFunction(label, stringAsSingular=True)
        _legend = {
            'bbox_to_anchor': (1.0, 1.0),
            'loc': 'upper right',
        } if legend is None else legend

        # print(axes)
        _ax = _fig.add_subplot(
            *subplotargs, **subplotkwargs) if ax is None else ax

        thetas = np.linspace(0, 2 * np.pi, len(axes), endpoint=False).tolist()
        # delta

        Theta = thetas[1] - thetas[0]

        _ax.set_theta_zero_location('N')
        # Fake labels to get size correct....
        _ax.set_xticklabels(
            [' ' for label, column in items(axes)])
        # ax.set_xticklabels([])
        _ax.set_xticks(thetas)
        _ax.set_yticklabels([])

        scaleParams = {}
        i = 0
        mx = -float('inf')
        for axisLabel, axisColumn in items(axes):
            # print(df[axisColumn].min(), max(df[axisColumn]))

            theta = thetas[i]

            # print(i, axisColumn, theta)
            args = [
                df[axisColumn].min(),
                df[axisColumn].max(),
                df[axisColumn].mean(),
                df[axisColumn].median(),
            ]
            delta = (args[1] - args[0]) * 0.025
            scaleParams[axisColumn] = args

            minAxisLabel = minAxisFormater(
                args[0], axisColumn) if not minAxisFormater is None else ''
            if minAxisLabel:
                _ax.text(theta, scalerHelper(args[0] + delta, axisColumn, *args)[
                         0], rotation_mode='anchor', rotation=theta * 180 / np.pi, s=minAxisLabel)
            maxAxisLabel = maxAxisFormater(
                args[1], axisColumn) if not maxAxisFormater is None else ''
            if maxAxisLabel:
                _ax.text(theta, scalerHelper(args[1] - delta, axisColumn, *args)[
                         0], rotation_mode='anchor', rotation=theta * 180 / np.pi, s=maxAxisLabel)

            mx = max(mx, scalerHelper(args[1], axisColumn, *args)[1])
            i = i + 1

        _ax.set_ylim([0, mx])
        if yTicks:
            _yTicks = asFunction(yTicks, stringAsSingular=True)
            _ax.set_yticks(_yTicks(mx))

        i = 0
        for axisLabel, axisColumn in items(axes):
            theta = thetas[i]
            _ax.text(theta, 1.05 * (mx if yMax is None else yMax), ha='center',
                     va='baseline', rotation_mode='anchor', rotation=theta * 180 / np.pi, s=axisLabel)
            i = i + 1

        # print(scaleParams)

        thetas += [thetas[0]]
        globalMax = 0
        for i, row in df.iterrows():
            values = [
                scalerHelper(row[axis], axis, *scaleParams[axis])[0] for label, axis in items(axes)
            ]
            globalMax = max(globalMax, np.max(values))
            values += [values[0]]
            col = _color(i, row)
            lineKWs = {
                'color': col,
                'linewidth': 1,
                'label': label(i, row),
            }
            lineKWs.update(_line(i, row))
            _ax.plot(thetas, values, **lineKWs)
            _ax.fill(thetas, values, color=lineKWs['color'], alpha=0.1)

            if text:
                i = 0
                for axisLabel, axisColumn in items(axes):
                    _text = asFunction(text, stringAsSingular=True)
                    ttext = _text(row[axisColumn], axisLabel, axisColumn, row)
                    theta = thetas[i]
                    r = values[i] / mx

                    sign = 1.0 if r > 0.5 else -1
                    ha = 'center'
                    ha = 'right' if sign * math.sin(theta) < -0.5 else ha
                    ha = 'left' if sign * math.sin(theta) > 0.5 else ha

                    va = 'center'
                    va = 'top' if sign * math.cos(theta) > 0.5 else va
                    va = 'bottom' if sign * math.cos(theta) < -0.5 else va

                    defaults = {
                        'color': col,
                        'horizontalalignment': ha,
                        'verticalalignment': va,
                    }

                    Tools._plotText(
                        _ax, thetas[i], values[i], ttext, defaults)
                    i = i + 1

        if not yMax is None:
            ax.set_ylim((0, yMax))

        if not title is None:
            _title = asFunction(title, stringAsSingular=True)
            _title = _title()
            if isinstance(_title, str):
                _title = {
                    'label': _title,
                    'loc': 'left',
                }
            _ax.set_title(**_title)

        if _legend != False:
            _ax.legend(**_legend)
        return _fig
