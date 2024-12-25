from PIL import Image
from src.utils.color_space import get_color_rank

HEADER = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="50" height="50" xmlns="http://www.w3.org/2000/svg">
# add a border around the image
<rect x="0.5" y="0.5" width="49" height="49" fill="none" stroke="white" stroke-width="1"/>
"""


def get_contrast_color(r, g, b):
    # Calculate the luminance of the background color
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255

    # Return black or white text color based on luminance
    return (0, 0, 0) if luminance > 0.5 else (255, 255, 255)


def img_to_circles(img_file: str, color_space: list = None):
    # read the image
    img = Image.open(img_file)

    # for each pixel, create a circle with the color of the pixel using svg
    width, height = img.size
    circles = []
    for i in range(width):
        for j in range(height):
            color = img.getpixel((i, j))
            rank = get_color_rank(color, color_space) if color_space else ''
            r, g, b = color[:3]
            circle = (f'<circle cx="{i + 1.5}" cy="{j + 1.5}" r="0.5" fill="rgb({r},{g},{b})" stroke="gray" '
                      f'stroke-width="0.02"/>')
            # add a square with a very thiny gray border
            square = f'<rect x="{i+1}" y="{j+1}" width="1" height="1" fill="none" stroke="gray" stroke-width="0.01" />'
            # create a circle
            content = rank
            text_color = get_contrast_color(*color[:3])
            r, g, b = text_color
            text = (f'<text x="{i + 1.5}" y="{j + 1.5}" font-size="0.35" fill="rgb({r},{g},{b})" text-anchor="middle" '
                    f'dominant-baseline="middle">{content}</text>')

            circles.append(circle)
            circles.append(square)
            circles.append(text)

    # create the svg
    svg = f'{HEADER}' + '\n'.join(circles) + '</svg>'

    # replace fileextension in img_file to svg
    img_file = img_file.rsplit('.', 1)[0]
    img_file += '.svg'

    # save the svg file
    with open(img_file, 'w') as f:
        f.write(svg)
