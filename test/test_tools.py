import unittest

from src.tools import Tools


class TestTools(unittest.TestCase):

    def testColorGetter(self):
        intens1 = 0.8
        intens2 = 0.4

        cg = Tools.createColorGetter()
        c1 = cg()
        c2 = cg()
        assert [0, 0, intens1] == c1
        assert [0, intens1, 0] == c2

        cg2 = Tools.createColorGetter()
        c1 = cg2()
        c2 = cg2()
        assert [0, 0, intens1] == c1
        assert [0, intens1, 0] == c2

        c_A = cg2('A')
        c_B = cg2('B')
        assert [0, intens2, intens2] == c_A
        assert [intens1, 0, 0] == c_B
        assert [0, intens2, intens2] == cg2('A')

    def testMarkerGetter(self):
        g = Tools.createMarkerGetter()
        m1 = g()
        m2 = g()
        assert 'o' == m1
        assert '+' == m2

        g2 = Tools.createMarkerGetter()
        m1 = g2()
        m2 = g2()
        assert 'o' == m1
        assert '+' == m2

        m_A = g2('A')
        m_B = g2('B')
        assert 'x' == m_A
        assert '.' == m_B
        assert m_A == g2('A')

        # assert 3 == 0


if __name__ == '__main__':
    unittest.main()
