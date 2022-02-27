import sys
import math
from fontTools.ttLib import TTFont
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

    default_glyph_order = ['space', 'A']

    def __init__(self, ttFont=None, glyph_order=None):
        self.font = Font()
        self.ttFont = ttFont
        self.fillings = {}
        self.glyph_order = glyph_order or self.default_glyph_order

    def add_salts(self):
        for k, v in self.info.items():
            setattr(self.font.info, k, v)

    def form_shape(self):
        for glyph_name in self.glyph_order:
            self.font.newGlyph(glyph_name)
        self.font.glyphOrder = ['.notdef'] + self.glyph_order

    def put_fillings(self):
        if self.ttFont is None:
            self.construct_sample_glyphs()
        else:
            for glyph_name in self.glyph_order:
                self.construct_glyph(glyph_name)

    def wrap(self):
        ttFont = compileTTF(self.font)
        ttFont.save('Riceball-Regular.ttf')

    def construct_sample_glyphs(self):
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

    def construct_glyph(self, glyph_name):
        from ascii_art import AsciiArtGlyph

        if glyph_name == 'space':
            glyph = self.font['space']
            glyph.width = 500
            glyph.unicodes = [0x20]
        else:
            glyph = self.font[glyph_name]
            glyph.width = self.ttFont.getGlyphSet()[glyph_name].width
            glyph.unicodes = [ord(glyph_name)]

            box_width = 50
            box_height = 50

            aag = AsciiArtGlyph(self.ttFont, (box_width, box_height))
            image = aag.render_glyph(glyph_name)
            vertical_box_num = image.shape[0] // box_height
            aa = aag.quantize_as_ascii_art(image)

            for h in range(len(aa)):
                for w in range(len(aa[h])):
                    if aa[h][w] == '*':
                        offset_x = box_width * w
                        offset_y = box_height * (vertical_box_num - h - 1)
                        contour = self.create_riceball_contour(box_width, offset_x, offset_y)
                        glyph.appendContour(contour)

    def create_riceball_contour(self, box_width, offset_x=0, offset_y=0):
        contour = Contour()
        for x, y in [(offset_x, offset_y), (int(math.ceil(box_width/2))+offset_x, int(math.ceil(box_width*math.sqrt(3)/2))+offset_y), (box_width+offset_x, offset_y)]:
            contour.insert(-1, Point(x, y))
        return contour

def main():
    ttFont = TTFont(sys.argv[1])
    glyph_order = ['space'] + [chr(v) for v in list(range(ord('A'), ord('Z')+1)) + list(range(ord('a'), ord('z')+1))]
    riceball = Riceball(ttFont, glyph_order)
    riceball.add_salts()
    riceball.form_shape()
    riceball.put_fillings()
    riceball.wrap()

if __name__ == '__main__':
    main()
