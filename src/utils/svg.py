from PIL import Image
from src.utils.color_space import get_color_rank
import os

HEADER = """<svg width="50" height="51" xmlns="http://www.w3.org/2000/svg">
<style>
    .toggle-target {
      opacity: 1;
    }
    .toggle-element:hover ~ .toggle-target {
      opacity: 0.3;
    }
    .toggle-element-1:hover ~ .toggle-target-1,
    .toggle-element-2:hover ~ .toggle-target-2,
    .toggle-element-3:hover ~ .toggle-target-3,
    .toggle-element-4:hover ~ .toggle-target-4,
    .toggle-element-5:hover ~ .toggle-target-5,
    .toggle-element-6:hover ~ .toggle-target-6,
    .toggle-element-7:hover ~ .toggle-target-7,
    .toggle-element-8:hover ~ .toggle-target-8,
    .toggle-element-9:hover ~ .toggle-target-9,
    .toggle-element-10:hover ~ .toggle-target-10,
    .toggle-element-11:hover ~ .toggle-target-11,
    .toggle-element-12:hover ~ .toggle-target-12,
    .toggle-element-13:hover ~ .toggle-target-13,
    .toggle-element-14:hover ~ .toggle-target-14,
    .toggle-element-15:hover ~ .toggle-target-15,
    .toggle-element-16:hover ~ .toggle-target-16 {
      opacity: 1;
    }
</style>
<!-- add a border around the image -->
<rect x="0.5" y="0.5" width="49" height="49" fill="black" stroke="white" stroke-width="1"/>
<!-- add a gray horizontal line at the bottom -->
<line x1="0" y1="50.5" x2="50" y2="50.5" stroke="gray" stroke-width="1"/>
"""


def get_contrast_color(r, g, b):
    # Calculate the luminance of the background color
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255

    # Return black or white text color based on luminance
    return (0, 0, 0) if luminance > 0.5 else (255, 255, 255)


def img_to_circles(img_file: str, color_space: list = None):
    # read the image
    img = Image.open(img_file)
    circles = []
    # add color space circles at the bottom, these are toggle elements
    if color_space:
        for idx, color in enumerate(color_space):
            r, g, b = color[:3]
            rank = get_color_rank(color, color_space)
            text_color = get_contrast_color(*color[:3])
            tr, tg, tb = text_color

            circle = (
                f'<circle class="toggle-element toggle-element-{rank}" cx="{idx+1.5}" cy="50.5" r="{0.5}" '
                f'fill="rgb'
                f'({r}'
                f',{g}'
                f',{b})" stroke="gray" '
                f'stroke-width="0.02"/>')
            text = (f'<text class="toggle-element toggle-element-{rank}" x="{idx + 1.5}" y="50.5" font-size="0.35" '
                    f'fill="rgb({tr},{tb},{tg})" text-anchor="middle" '
                    f'dominant-baseline="middle">{idx + 1}</text>')
            circles.append(circle)
            circles.append(text)

    # for each pixel, create a circle with the color of the pixel using svg
    # these circles are target elements
    width, height = img.size

    for i in range(width):
        # add the number of the column on top of the column as a bold text
        axis_text = (f'<text x="{i + 1.5}" y="0.5" font-size="0.35" fill="black" text-anchor="middle" '
                        f'dominant-baseline="middle" font-weight="bold">{i + 1}</text>')
        circles.append(axis_text)
        # do the same with the bottom of the column
        axis_text_bottom = (f'<text x="{i + 1.5}" y="{height + 1.5}" font-size="0.35" fill="black" text-anchor="middle" '
                        f'dominant-baseline="middle" font-weight="bold">{i + 1}</text>')
        circles.append(axis_text_bottom)

        for j in range(height):
            color = img.getpixel((i, j))
            rank = get_color_rank(color, color_space) if color_space else ''
            r, g, b = color[:3]
            circle = (f'<circle class="toggle-target toggle-target-{rank}" cx="{i + 1.5}" cy="{j + 1.5}" r="0.5" '
                      f'fill="rgb({r},{g}'
                      f',{b})" stroke="gray" '
                      f'stroke-width="0.02"/>')
            # add a square with a very thiny gray border
            square = f'<rect x="{i+1}" y="{j+1}" width="1" height="1" fill="none" stroke="gray" stroke-width="0.01" />'
            # create a circle
            content = rank
            text_color = get_contrast_color(*color[:3])
            r, g, b = text_color
            text = (f'<text class="toggle-target toggle-target-{rank}" x="{i + 1.5}" y="{j + 1.5}" font-size="0.35" '
                    f'fill="rgb({r},{g}'
                    f',{b})" text-anchor="middle" '
                    f'dominant-baseline="middle">{content}</text>')

            circles.append(circle)
            circles.append(square)
            circles.append(text)

            # add the index of the row on the left of the row
            if i == 0:
                axis_text = (f'<text x="0.5" y="{j + 1.5}" font-size="0.35" fill="black" text-anchor="middle" '
                             f'dominant-baseline="middle" font-weight="bold">{j + 1}</text>')
                circles.append(axis_text)
                # also add it to the right of the image
                axis_text_right = (f'<text x="{width + 1.5}" y="{j + 1.5}" font-size="0.35" fill="black" text-anchor="middle" '
                                   f'dominant-baseline="middle" font-weight="bold">{j + 1}</text>')
                circles.append(axis_text_right)





    # create the svg
    svg = f'{HEADER}' + '\n'.join(circles) + '</svg>'

    # replace fileextension in img_file to svg
    img_file = img_file.rsplit('.', 1)[0]
    img_file += '.svg'

    # save the svg file
    with open(img_file, 'w') as f:
        f.write(svg)

    # make the svg file writable
    os.chmod(img_file, 0o777)
