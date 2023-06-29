import numpy as np
import matplotlib.pyplot as plt
import math

from .tools import Tools


class FractionPlot():

    @classmethod
    def fractionPlots(cls, df, specs,
                      colorGetter=None,
                      markerGetter=None,
                      labelGetter=None,
                      fig=None,
                      ax=None):

        _colorGetter = (lambda row, i: Tools.colors[i % len(
            Tools.colors)]) if colorGetter is None else colorGetter
        _markerGetter = (lambda row, i: Tools.markers[i % len(
            Tools.markers)]) if markerGetter is None else markerGetter
        _labelGetter = (lambda row, i: str(
            i)) if labelGetter is None else labelGetter

        luMap = {
            'right': -1,
            'center': 0,
            'left': 1,
            'top': -1,
            'bottom': 1,
        }

        lMapInv = {val: key for key,
                   val in luMap.items() if key not in ('top', 'bottom')}
        uMapInv = {val: key for key,
                   val in luMap.items() if key not in ('left', 'right')}

        def alignment(ha='center', va='center'):

            Tlu = np.matmul(pieT, [
                [luMap[ha], 0],
                [0, luMap[va]],
                [0, 0]
            ])
            Tv = np.matmul(pieT, [
                [1, 0],
                [0, 1],
                [0, 0]
            ])
            rot = 90 * abs(Tv[1, 0]) * -np.sign(Tv[0, 1])
            res = {'ha': lMapInv[round(
                Tlu[0, 0]+Tlu[0, 1])], 'va': uMapInv[round(Tlu[1, 0]+Tlu[1, 1])], 'rotation': rot}
            return res

        def plotScatter(xColumn, yColumn, T, xMax, shareMean, ha, va):
            xy0 = df[[xColumn, yColumn]].copy()
            xy0['zero'] = 1
            xy0 = xy0.to_numpy().transpose()
            xy = np.matmul(T, xy0)

            p = [0.5 * (xMax + xMin), shareMean * 0.5 * (xMax + xMin), 1]
            p = np.matmul(T, p)
            for i, row in df.iterrows():
                # if abs(xy[0,i]) < 0.00001:
                #    continue
                color = _colorGetter(row, i)
                marker = _markerGetter(row, i)
                label = _labelGetter(row, xColumn, yColumn, i)

                # xRef = [0.5 * xMax, 0.5 * xMax, 1]
                # xRef = np.matmul(T, xRef)

                # yRef = [shareMean * xy0[0,i], shareMean * xy0[0,i], 1]
                # yRef = np.matmul(T, yRef)

                if ha is None:
                    _ha = 'right' if xy[0, i] > p[0] else 'left'
                else:
                    _ha = ha
                if va is None:
                    _va = 'top' if xy[1, i] > p[1] else 'bottom'
                else:
                    _va = va

                _ax.plot(xy[0, i], xy[1, i], linewidth=0,
                         marker=marker, color=color)
                _ax.text(xy[0, i], xy[1, i], label,
                         color=color, ha=_ha, va=_va)

        if ax:
            _ax = ax
            _fig = ax.figure
        else:
            if not fig:
                _fig = plt.figure()
            else:
                _fig = fig
            _ax = _fig.add_subplot(1, 1, 1)

        for i, spec in enumerate(specs):
            areaSpec = cls.fractionPlotSpecs[spec['area']]
            assert areaSpec, 'Invalid area spec {}'.format(spec['area'])
            shareMax = np.max(df[spec['yColumn']] / df[spec['xColumn']])
            shareMin = np.min(df[spec['yColumn']] / df[spec['xColumn']])
            xMin = df[spec['xColumn']].min()
            xMax = df[spec['xColumn']].max()
            xMin = 0.80 * xMin

            xBase = math.ceil(-(math.log10(0.5 * (xMin+xMax))) - 1)
            xBase = int(max(xBase, 0))

            yMax = np.max([shareMax * xMin, shareMax * xMax])
            yMin = np.min([shareMin * xMin, shareMin * xMax])

            transT =\
                [
                    [1, 0, -xMin],
                    [0, 1, -yMin],
                    [0, 0, 1]
                ]

            _df = df[[spec['xColumn'], spec['yColumn']]]
            _df[spec['xColumn']] = _df[spec['xColumn']] - xMin
            _df[spec['yColumn']] = _df[spec['yColumn']] - yMin
            _xMin = _df[spec['xColumn']].min()
            _xMax = _df[spec['xColumn']].max()
            _shareMax = np.max(_df[spec['yColumn']] / _df[spec['xColumn']])
            _shareMin = np.min(_df[spec['yColumn']] / _df[spec['xColumn']])
            _yMax = np.max([_shareMax * _xMin, _shareMax * _xMax])
            _yMin = np.min([_shareMin * _xMin, _shareMin * _xMax])

            locT = transT

            minBase = [1, _shareMin, 0]
            minBase = minBase / \
                np.linalg.norm(minBase) * \
                np.linalg.norm([_xMax, _shareMin * (_xMax)])
            maxBase = np.subtract([(_xMax), (_yMax), 0],
                                  [minBase[0],  minBase[1], 0])

            f = [minBase, maxBase, [0, 0, 1]]
            f = np.transpose(f)
            locT = np.matmul(
                np.linalg.inv(f), locT)
            locTInv = np.linalg.inv(locT)

            pieT = areaSpec['T']
            T = np.matmul(np.array(pieT), locT)

            plotScatter(spec['xColumn'], spec['yColumn'], T,
                        xMax, 0.5 * (shareMin + shareMax),
                        areaSpec['haMarkerLabel'], areaSpec['vaMarkerLabel'])

            dShare = (shareMax - shareMin) / 4.0
            share = shareMin + dShare
            while share <= shareMax + 0.5 * dShare:

                zz0 = (0, 0, 1)
                zz1 = (1, 1, 1)
                zz0 = np.matmul(locTInv, zz0)
                zz1 = np.matmul(locTInv, zz1)

                kk = (zz1[1] - zz0[1]) / (zz1[0] - zz0[0])

                _share = max(min(shareMax, share), shareMin)

                x = (kk * zz0[0] - zz0[1]) / (kk - _share)
                x = max(x, xMin)
                vecCent = np.matmul(T, [x, x * _share, 1])
                vecPeri = np.matmul(T, [xMax, _share * xMax, 1])

                a = alignment(ha='left', va='center')
                _ax.plot([vecCent[0], vecPeri[0]], [vecCent[1], vecPeri[1]],
                         linewidth=0.125, marker='', color='grey')
                _ax.text(vecPeri[0], vecPeri[1], '{}%'.format(int(round(_share*100))), {
                    'alpha': 0.5,
                    'color': 'grey',
                    **a,
                })

                share = share + dShare

            _ = 0.5 * (np.min(df[spec['xColumn']]) + xMax)
            p = np.matmul(T, [_, shareMin * _, 1, ])
            _ax.text(p[0], p[1], spec['label'], {
                'alpha': 1,
                'fontsize': 'small',
                **alignment(ha='center', va='bottom'),
            })

            pq0 = np.matmul(pieT, [
                [0, 1],
                [0, 0],
                [1, 1],
            ])
            _ax.plot(pq0[0, :], pq0[1, :], linewidth=0.1,
                     marker='', color='black', alpha=1)
            pq45 = np.matmul(pieT, [
                [0, 1],
                [0, 1],
                [1, 1],
            ])
            _ax.plot(pq45[0, :], pq45[1, :], linewidth=0.1,
                     marker='', color='black', alpha=1)

            _ = np.min(df[spec['xColumn']])
            pq = np.matmul(T, [
                _,
                shareMin * _,
                1
            ])
            a = alignment(ha='left', va='bottom')
            _ax.text(pq[0], pq[1], s=round(_, xBase),
                     color='black', alpha=0.5, **a)
            _ax.plot(pq[0], pq[1], lw=0, marker='+',
                     markersize=0.5, color='black', alpha=0.5)

            a = alignment(ha='right', va='bottom')
            _ = xMax
            pq = np.matmul(T, [
                _,
                shareMin * _,
                1
            ])
            _ax.text(pq[0], pq[1], s=round(_, xBase),
                     color='black', alpha=0.5, **a)
            _ax.plot(pq[0], pq[1], lw=0, marker='+',
                     markersize=0.5, color='black', alpha=0.5)

            _ax.axis('off')
            # break

        return _ax, _fig

    fractionPlotSpecs = {

        '1': {
            'T': [  # 0-45
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]
            ],
            'haMarkerLabel': 'left',
            'vaMarkerLabel': None,
        },

        '2': {
            'T': [  # 45-90
                [0, 1, 0],
                [1, 0, 0],
                [0, 0, 1]
            ],
            'haMarkerLabel': None,
            'vaMarkerLabel': 'bottom',
        },

        '3': {
            'T': [  # 90-135
                [0, -1, 0],
                [1, 0, 0],
                [0, 0, 1]
            ],
            'haMarkerLabel': None,
            'vaMarkerLabel': 'bottom',
        },

        '4': {
            'T': [  # 135-180
                [-1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]
            ],
            'haMarkerLabel': 'right',
            'vaMarkerLabel': None,
        },

        '5': {
            'T': [  # 180-225
                [-1, 0, 0],
                [0, -1, 0],
                [0, 0, 1]
            ],
            'haMarkerLabel': 'right',
            'vaMarkerLabel': None,
        },

        '6': {
            'T': [  # 225-270
                [0, -1, 0],
                [-1, 0, 0],
                [0, 0, 1]
            ],
            'ha100': 'center',
            'va100': 'bottom',
            'ha50': 'center',
            'va50': 'bottom',
            'haMarkerLabel': None,
            'vaMarkerLabel': 'top',
        },

        '7': {
            'T': [  # 270-315
                [0, 1, 0],
                [-1, 0, 0],
                [0, 0, 1]
            ],
            'haMarkerLabel': None,
            'vaMarkerLabel': 'top',
        },

        '8': {
            'T': [  # 270-315
                [1, 0, 0],
                [0, -1, 0],
                [0, 0, 1]
            ],
            'haMarkerLabel': 'left',
            'vaMarkerLabel': None,
        },

    }
