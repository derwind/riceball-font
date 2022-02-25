from ufoLib2 import Font
from ufoLib2.objects import Contour, Point
from ufo2ft import compileTTF

class Riceball:
    info = {
        'familyName': 'Riceball',
        'styleName': 'Regular',
        'styleMapStyleName': 'regular',
        'versionMajor': 0,
        'versionMinor': 1,
        'unitsPerEm': 1000,
        'descender': -250,
        'xHeight': 300,
        'capHeight': 390,
        'ascender': 750,
        'postscriptFontName': 'Riceball-Regular',
        'openTypeOS2WidthClass': 5,
        'openTypeOS2WeightClass': 400,
    }

    glyph_order = ['space', 'A']

    def __init__(self):
        self.font = Font()
        self.fillings = {}

    def add_salts(self):
        for k, v in self.info.items():
            setattr(self.font.info, k, v)

    def form_shape(self):
        for glyph_name in self.glyph_order:
            self.font.newGlyph(glyph_name)
        self.font.glyphOrder = ['.notdef'] + self.glyph_order

    def put_fillings(self):
        glyph = self.font['space']
        glyph.width = 500
        glyph.unicodes = [0x20]

        glyph = self.font['A']
        glyph.width = 600
        glyph.unicodes = [ord('A')]
        contour = Contour()
        for x, y in [(0, 0), (300, 520), (600, 0)]:
            contour.insert(-1, Point(x, y))
        glyph.appendContour(contour)

    def wrap(self):
        ttFont = compileTTF(self.font)
        ttFont.save('Riceball-Regular.ttf')

def main():
    riceball = Riceball()
    riceball.add_salts()
    riceball.form_shape()
    riceball.put_fillings()
    riceball.wrap()

if __name__ == '__main__':
    main()
