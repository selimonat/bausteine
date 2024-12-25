from PIL import Image

HEADER = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="48" height="48" xmlns="http://www.w3.org/2000/svg">
"""


def img_to_circles(img_file: str):
    # read the image
    img = Image.open(img_file)

    # for each pixel, create a circle with the color of the pixel using svg
    width, height = img.size
    circles = []
    for i in range(width):
        for j in range(height):
            color = img.getpixel((i, j))
            r, g, b = color[:3]
            circle = f'<circle cx="{i}" cy="{j}" r="0.5" fill="rgb({r},{g},{b})" />'  # create a circle
            # create a circle with the coordinate (i, j) and the color of the pixel written in the circle
            text = f'<text x="{i}" y="{j}" font-size="0.25" fill="black">{i}-{j}</text>'

            circles.append(circle)
            circles.append(text)

    # create the svg
    svg = f'{HEADER}' + '\n'.join(circles) + '</svg>'

    # replace fileextension in img_file to svg
    img_file = img_file.rsplit('.', 1)[0]
    img_file += '.svg'

    # save the svg file
    with open(img_file, 'w') as f:
        f.write(svg)
