import numpy as np
import io
import base64
from sklearn.linear_model import LinearRegression
from matplotlib.patches import Ellipse
from matplotlib.patches import Rectangle


class Tools():

    colorIndex = 0
    colors = [[0, 0, 0.8], [0, 0.8, 0], [0, 0.4, 0.4], [0.8, 0, 0], [0.4, 0, 0.4], [
        0, 0, 0.5], [0, 0.5, 0], [0, 0.25, 0.25], [0.5, 0, 0], [0.25, 0, 0.25], [0.25, 0.25, 0], ]

    @staticmethod
    def createColorGetter():

        def helper(key=None):
            nonlocal i
            nonlocal cache

            if key in cache and not key is None:
                return cache[key]

            cache[key] = Tools.colors[i % len(Tools.colors)]
            i = i + 1
            return cache[key]

        i = 0
        cache = {}

        return helper

    markerIndex = 0
    markers = ["o", "+", "x", ".", "v", "^", "<", ">", "1", "2", "3", "4", "8", "s", "p",
               "P", "*", "h", "H", "X", "D", "d", "|", "_", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, ]

    @staticmethod
    def createMarkerGetter():

        def helper(key=None):
            nonlocal i
            nonlocal cache

            if key in cache and not key is None:
                return cache[key]

            cache[key] = Tools.markers[i % len(Tools.markers)]
            i = i + 1
            return cache[key]

        i = 0
        cache = {}

        return helper

    linestylesIndex = 0
    linestyles = ['solid', 'dashed', 'dotted', 'dashdot']

    @staticmethod
    def createLinestyleGetter():

        def helper(key=None):
            nonlocal i
            nonlocal cache

            if key in cache and not key is None:
                return cache[key]

            cache[key] = Tools.linestyles[i % len(Tools.linestyles)]
            i = i + 1
            return cache[key]

        i = 0
        cache = {}

        return helper

    @staticmethod
    def plotAsBase64(plt, bbox_inches=None):
        bbytes = io.BytesIO()

        # plt.savefig(bbytes, dpi=Tools.plot2ImageDPI, format='png', bbox_inches='tight')
        plt.savefig(bbytes, dpi=Tools.plot2ImageDPI,
                    format='png', bbox_inches=bbox_inches)
        bbytes.seek(0)
        return base64.b64encode(bbytes.read()).decode('ascii')

    @staticmethod
    def base64AsImgSrc(base64Img, imageFormat='png'):
        return 'data:image/{};base64,{}'.format(imageFormat, base64Img)

    @staticmethod
    def _setTicks(axis, ticks):
        ticks = [
            t for t in ticks if ('label' in t and t['label']) or ('tick' in t and (t['tick'] or t['tick'] != 0))
        ]
        ticks.sort(key=lambda item: item['tick'])
        axis.set_ticks([
            t['tick'] if 'tick' in t else None for t in ticks
        ], minor=False)
        axis.set_ticklabels([
            t['label'] if t['label'] else '' for t in ticks
        ], minor=False)
        yMin = np.min([t['tick'] for t in ticks])
        yMax = np.max([t['tick'] for t in ticks])

    @staticmethod
    def _setLimits(ax, rectangle={'bottom': None, 'top': None, 'left': None, 'right': None}):
        ax.set_ylim(**{
            'top': rectangle['top'] if 'top' in rectangle else None,
            'bottom': rectangle['bottom'] if 'bottom' in rectangle else None,
        })

        ax.set_xlim(**{
            'left': rectangle['left'] if 'left' in rectangle else None,
            'right': rectangle['right'] if 'right' in rectangle else None,
        })

    @staticmethod
    def _plotRay(ax, x, y, ray):
        if not ray:
            return

        xTo = ray['x']
        yTo = ray['y']
        if 'arrow' in ray:
            kwArgs = {
                'length_includes_head': True
            }
            kwArgs.update(ray['arrow'] if 'arrow' in ray else {})
            reverse = kwArgs.pop('reverse', False)
            # print(kwArgs)
            if reverse:
                ax.arrow(xTo, yTo, x-xTo, y-yTo, **kwArgs)
            else:
                ax.arrow(x, y, xTo-x, yTo-y, **kwArgs)

        if 'line' in ray:
            ax.plot((x, xTo), (y, yTo), **ray['line'] if 'line' in ray else {})

        if 'point' in ray:
            ax.plot((xTo, xTo), (yTo, yTo), **
                    ray['point'] if 'point' in ray else {'linewidth': 0})

    @staticmethod
    def _plotText(ax, x, y, ttext, pointSpec={}):
        if ttext:
            if isinstance(ttext, str):
                _txt = ttext
                ttext = {}
            else:
                _txt = ttext.pop('txt')

            if 'xytext' in ttext:
                _xytext = ttext.pop('xytext')

            _text0 = dict(pointSpec)
            _text0.update(ttext)
            ttext = _text0
            ax.annotate(_txt, (x, y), **ttext)

    @staticmethod
    def _plotEllipse(ax, x, y, ellipse):
        return Tools._plotPatch(ax, Ellipse, x, y, ellipse, center=False)

    @staticmethod
    def _plotBox(ax, x, y, ellipse):
        return Tools._plotPatch(ax, Rectangle, x, y, ellipse, center=True)

    @staticmethod
    def _plotPatch(ax, Patch, x, y, ellipse, center=False):
        if ellipse:

            ellipse0 = {
                'xy': (x, y),
                'width': 0,
                'height': 0,
                'fill': False,
                'edgecolor': None,
                'facecolor': None,
                'linewidth': 0,
            }

            if 'width' in ellipse or 'height' in ellipse:
                _ellipse = {}
                _ellipse.update(ellipse0)
                _ellipse.update(ellipse)
                _ellipse.pop('left', None)
                _ellipse.pop('right', None)
                _ellipse.pop('top', None)
                _ellipse.pop('bottom', None)
                if center:
                    x = _ellipse['xy'][0] - 0.5 * _ellipse['width']
                    y = _ellipse['xy'][1] - 0.5 * _ellipse['height']
                    _ellipse['xy'] = (x, y)
                _ellipse = Patch(**_ellipse)
                ax.add_patch(_ellipse)

            if 'left' in ellipse or 'right' in ellipse or 'top' in ellipse or 'bottom' in ellipse:
                _ellipse = {}
                _ellipse.update(ellipse0)
                _ellipse.update(ellipse)
                _ellipse.pop('width', None)
                _ellipse.pop('height', None)
                _ellipse['width'] = ellipse['right'] - ellipse['left']
                _ellipse['height'] = ellipse['top'] - ellipse['bottom']
                _ellipse['xy'] = (
                    0.5 * (ellipse['right'] + ellipse['left']),
                    0.5 * (ellipse['top'] + ellipse['bottom']),
                )
                del _ellipse['left']
                del _ellipse['right']
                del _ellipse['bottom']
                del _ellipse['top']
                if center:
                    x = _ellipse['xy'][0] - 0.5 * _ellipse['width']
                    y = _ellipse['xy'][1] - 0.5 * _ellipse['height']
                    _ellipse['xy'] = (x, y)
                _ellipse = Patch(**_ellipse)
                ax.add_patch(_ellipse)

    @staticmethod
    def _plotCross(ax, x, y, cross):
        if cross is None:
            return

        _cross0 = {
            'width': 0,
            'height': 0,
            'color': None,
            'linewidth': 0,
            'linestyle': '-',
        }

        if 'width' in cross or 'height' in cross:

            _cross = {}
            _cross.update(_cross0)
            _cross.update(cross)
            _cw = _cross.pop('width')
            _ch = _cross.pop('height')
            _cross.pop('left', None)
            _cross.pop('right', None)
            _cross.pop('top', None)
            _cross.pop('bottom', None)

            # print(cross)
            ax.plot((x - 0.5 * _cw, x+0.5 * _cw), (y, y), **_cross)
            ax.plot((x, x), (y - 0.5 * _ch,  y + 0.5 * _ch), **_cross)

        if 'left' in cross or 'right' in cross or 'top' in cross or 'bottom' in cross:
            _cross = {}
            _cross.update(_cross0)
            _cross.update(cross)
            left = cross['left'] if 'left' in cross else x
            right = cross['right'] if 'right' in cross else x
            bottom = cross['bottom'] if 'bottom' in cross else y
            top = cross['top'] if 'top' in cross else y
            _cross.pop('left', None)
            _cross.pop('right', None)
            _cross.pop('bottom', None)
            _cross.pop('top', None)
            _cross.pop('width', None)
            _cross.pop('height', None)
            if 'left' in cross or 'right' in cross:
                ax.plot((left, right), (y, y), **_cross)
            if 'bottom' in cross or 'top' in cross:
                ax.plot((x, x), (bottom,  top), **_cross)

    @staticmethod
    def _plotOLS(ax, ols, xys):

        if ols is None:
            return

        _olss = ols if isinstance(ols, (list, tuple)) else [ols]

        for _ols in _olss:
            _ols['showFit'] = _ols['showFit'] if 'showFit' in _ols else False
            showFit = _ols.pop('showFit')
            xys = _ols.pop('xys', xys)
            xys = np.reshape(np.array(xys), (-1, 2))
            lr = LinearRegression()
            # print(xys[:,0], xys[:,1])
            lr.fit(np.reshape(xys[:, 0], (-1, 1)), xys[:, 1])
            r2 = lr.score(np.reshape(xys[:, 0], (-1, 1)), xys[:, 1])
            X = np.array([np.min(xys[:, 0]), np.max(xys[:, 0])])
            X = np.reshape(X, (2, 1))
            yExp = lr.predict(X)
            # print(yExp)
            ax.plot(X[:, 0], yExp, **_ols)

            if showFit != False:
                ax.text(x=X[-1, 0], y=yExp[-1], s='$R^2=' + str(round(100.0 * r2)) + '$',
                        ha='right',
                        va='bottom' if lr.coef_[0] >= 0 else 'top',
                        fontsize='small',
                        color=_ols['color'] if 'color' in _ols else None)
