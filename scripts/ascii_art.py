import sys
import math
import numpy as np
from PIL import Image
from fontTools.ttLib import TTFont
from fontTools.pens.freetypePen import FreeTypePen

class AsciiArtGlyph:
    def __init__(self, font_path, box_size = 50):
        self.ttFont = TTFont(font_path)
        self.box_size = box_size

    def render_glyph(self, glyph_name, scale=1):
        glyph = self.ttFont.getGlyphSet()[glyph_name]
        width, ascender, descender = glyph.width, self.ttFont['OS/2'].sTypoAscender, self.ttFont['OS/2'].sTypoDescender
        height = ascender - descender
        im = self.draw_char_image_array(glyph, width, height)
        ceiled_shape = [math.ceil(v / self.box_size) * self.box_size for v in im.shape]
        # [0, 255] to [0, 1]
        background = np.ones(ceiled_shape, dtype=np.uint8) * scale
        for i in range(im.shape[0]):
            for j in range(im.shape[1]):
                # gray to black
                if im[i, j] < 255:
                    background[i, j] = 0
        return background

    def quantize_as_ascii_art(self, image:np.ndarray):
        canvas = []
        for i in range(image.shape[0] // self.box_size):
            row = ''
            for j in range(image.shape[1] // self.box_size):
                sub_image = image[self.box_size*i:self.box_size*(i+1), self.box_size*j:self.box_size*(j+1)]
                if np.sum(sub_image) < self.box_size*self.box_size/2:
                    row += '*'
                else:
                    row += '.'
            canvas.append(row)
        return '\n'.join(canvas)

    def draw_char_image_array(self, glyph, width=None, height=None):
        pen = FreeTypePen(None)
        glyph.draw(pen)
        im = pen.image(width=width, height=height)
        background = Image.new('RGB', im.size, (255, 255, 255))
        background.paste(im, mask=im.split()[-1])
        return np.asarray(background.convert('L'))

    def save_image_array(self, image:np.ndarray, filename):
        Image.fromarray(image, mode='L').save(filename)

def main():
    aa = AsciiArtGlyph(sys.argv[1])
    for glyph_name in ['A', 'B', 'C', 'a', 'b', 'c']:
        im = aa.render_glyph(glyph_name)
        print(aa.quantize_as_ascii_art(im))

if __name__ == '__main__':
    main()
