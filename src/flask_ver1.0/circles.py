import numpy as np
from svgwrite.container import SVG
from svgwrite.shapes import Circle
from PIL import Image, ImageColor

r = 10
target_image_width = tiw = 48  # circles per row
target_image_height = tih = None  # circles per column

lego_colors = [
    'Black',
    'darkblue',
    'deepskyblue',
    'PowderBlue',
    'White',
    'Plum',
    'Red',
    'darkorange',
    'Orange',
    'Gold',
    'lemonchiffon',
    'wheat',
    'peru',
    'SaddleBrown',
    'limegreen',
    'Greenyellow'
    ]


def css_to_rgb(css):
    """convert css color to rgb"""
    c = list()
    for css in lego_colors:
        rgb = ImageColor.getcolor(css, "RGB")
        for _ in rgb:
            c.append(_)
    return c


def color_extractor(img):
    # open image
    img = Image.open(img)
    # get image size
    w, h = img.size
    print(f"Got image to height {h} and width {w}")
    # find the height of the image based on the target_image_width
    tih = int(h * (tiw / w))
    # resize image to target_image_width
    print(f"Resizing image to height {tih} and width {tiw}")
    img = img.resize((tih, tiw))
    img.save('./static/image_small.png')
    # convert image to hsv
    # img = img.convert('HSV')
    # run across all pixels and zip the x and y coordinates with the pixel values
    pixels = [(x * 2 * r, y * 2 * r, c_2_rgb(img.getpixel((y, x)))) for x in range(tiw) for y in range(tih)]
    return pixels


def c_2_hsl(color):
    """convert RGB colors to hsl format"""
    return f'hsl({int(color[0])}, {int(color[1])}%, {int(color[2] / 255 * 100)}%)'


def c_2_rgb(color):
    """convert RGB colors to hsl format"""
    return f'rgb({int(color[0])}, {int(color[1])}, {int(color[2])})'


# create a function that generates an array of svg circles based on a list of colors
def circle_array(values):
    # test the size of colors to be equal to the size of the lattice_x * lattice_y
    _ = [Circle((x, y), r, fill=c) for y, x, c in values]
    print(f"Created {len(_)} circles")
    return _


def svg_circles(img):
    v = color_extractor(img)
    # create the svg
    svg_width = tiw * 2 * r
    svg_height = len(v) / tiw * 2 * r
    print(f"SVG size: hxw {svg_height}x{svg_width}x")
    svg = SVG(size=(svg_width, svg_height))
    # add the circles to the svg
    for c in circle_array(v):
        svg.add(c)
    # return the svg
    return svg


def apply_palette(path_img):

    # Make a CGA palette and push it into image
    cga_colors = [
        182, 79, 73,
        181, 204, 214
    ]
    cga_colors = css_to_rgb(lego_colors)
    # Create new palette image
    palette_size = int(len(cga_colors) / 3)
    cga = Image.new('P', (palette_size, 1))
    cga.putpalette(cga_colors)
    # Open image
    img = Image.open(path_img)
    print(f"Image size: {img.size}")
    print(f"Image mode: {img.mode}")
    if img.mode == 'RGBA':
        print(f"Converting image mode to RGB")
        img = img.convert('RGB')
    img = img.resize((48, 48))
    # Quantize to our lovely CGA palette, without dithering
    res = img.quantize(colors=len(cga_colors), palette=cga, dither=Image.Dither.NONE)
    # Quantize to 5 colors, without dithering
    # res = img.quantize(colors=10, dither=Image.Dither.NONE)
    res.save('./static/image_palette_applied.png')
    cga.putdata(range(palette_size))
    cga.save('./static/palette.png')
    return 'image_palette.png'


if __name__ == '__main__':
    apply_palette("static/image_02.png")
    # s = svg_circles("./static/image.png")
    # print(s.tostring())
