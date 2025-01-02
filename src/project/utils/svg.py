from PIL import Image
from src.project.utils.color_space import get_color_rank
import os

RR = 1  # radius of the circles on the colorpalette
R = .5  # radius of the circles on the image
CANVAS_INNER_WIDTH = 48
CANVAS_INNER_HEIGHT = 48
BORDER_THICKNESS = R * 2
PALETTE_HEIGHT = R * 2 * 2  # height of the gray color palette
CANVAS_WIDTH = CANVAS_INNER_WIDTH + BORDER_THICKNESS * 2
CANVAS_HEIGHT = CANVAS_INNER_HEIGHT + BORDER_THICKNESS * 2 + PALETTE_HEIGHT
PALETTE_WIDTH = CANVAS_WIDTH
MULTIPLIER = M = 10


def base_doc():
    # sets the canvas size
    return f"""<svg width="{CANVAS_WIDTH * M}" height="{CANVAS_HEIGHT * M}" xmlns="http://www.w3.org/2000/svg">
    </svg>
    """


def add_style(doc: str) -> str:
    style_element = """<style>
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
    """
    # replace the RRR with the style
    return doc.replace('</svg>', style_element + '\n</svg>')


def add_script(doc: str) -> str:
    script = """
  <script type="text/javascript">
    function toggleVisibility(targetId) {
      var target = document.getElementById(targetId);
      if (target.style.display === 'none') {
        target.style.display = 'block';
      } else {
        target.style.display = 'none';
      }
    }

    function toggleVisibilityByClass(targetClass) {
      var targets = document.getElementsByClassName(targetClass);
      for (var i = 0; i &lt; targets.length; i++) {
        if (targets[i].style.opacity === '0.2') {
          targets[i].style.opacity = '1';
        } else {
          targets[i].style.opacity = '0.2';
        }
      }
    }
    
    function setVisibilityByClassOn(targetClass) {
  var targets = document.getElementsByClassName(targetClass);
  for (var i = 0; i &lt; targets.length; i++) {
    targets[i].style.opacity = '1';
  }
}

function setVisibilityByClassOff(targetClass) {
  var targets = document.getElementsByClassName(targetClass);
  for (var i = 0; i &lt; targets.length; i++) {
    targets[i].style.opacity = '0.2';
  }
}
  </script>
    """
    # replace the RRR with the style
    return doc.replace('</svg>', script + '\n</svg>')


def add_border(doc: str) -> str:
    border = f'<rect x="{BORDER_THICKNESS / 2 * 10}" y="{BORDER_THICKNESS / 2 * 10}" width="{(CANVAS_INNER_WIDTH + BORDER_THICKNESS) * 10}" height="{(CANVAS_INNER_HEIGHT + BORDER_THICKNESS) * 10}" fill="black" stroke="white" stroke-width="{BORDER_THICKNESS * 10}"/>'
    # replace </svg> with the border
    doc = doc.replace('</svg>', border + '\n</svg>')
    return doc


def add_square_tiles(doc: str, n: int) -> str:
    # adds n tiles in both directions
    # Check if INNER CANVAS is divisible by n
    if CANVAS_INNER_WIDTH % n != 0 or CANVAS_INNER_HEIGHT % n != 0:
        raise ValueError('Canvas is not divisible by n')
    TILE_BORDER_WIDTH = 2
    # Calculate the size of the tiles
    tile_width = CANVAS_INNER_WIDTH / n
    tile_height = CANVAS_INNER_HEIGHT / n

    # Add the tiles
    for i in range(n):
        for j in range(n):
            x = i * tile_width
            y = j * tile_height
            square = f'<rect x="{(x + BORDER_THICKNESS) * M}" y="{(y + BORDER_THICKNESS) * M}" width="{tile_width * 10}" height="{tile_height * 10}" fill="none" stroke="red" stroke-width="{TILE_BORDER_WIDTH}" opacity="0.5"/>'
            doc = doc.replace('</svg>', square + '\n</svg>')
    return doc


def get_contrast_color(r, g, b):
    # Calculate the luminance of the background color
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255

    # Return black or white text color based on luminance
    return (0, 0, 0) if luminance > 0.5 else (255, 255, 255)


def add_horizontal_scale(doc: str) -> str:
    # Add the horizontal scale
    for i in range(CANVAS_INNER_WIDTH):
        # add the number of the column on top of the column as a bold text
        axis_text = (f'<text x="{(i + 1 + R) * M}" y="{R * M}" font-size="{0.35 * M}" fill="black" '
                     f'text-anchor="middle" '
                     f'dominant-baseline="middle" font-weight="bold">{i + 1}-{CANVAS_INNER_WIDTH - i}</text>')
        doc = doc.replace('</svg>', axis_text + '\n</svg>')
        # do the same with the bottom of the column
        axis_text_bottom = (
            f'<text x="{(i + 1 + R) * M}" y="{(CANVAS_INNER_HEIGHT + 1 + R) * M}" font-size="{0.35 * M}" '
            f'fill="black" '
            f'text-anchor="middle" '
            f'dominant-baseline="middle" font-weight="bold">{i + 1}-{CANVAS_INNER_HEIGHT - i}</text>')
        doc = doc.replace('</svg>', axis_text_bottom + '\n</svg>')
    return doc


def add_vertical_scale(doc: str) -> str:
    # Add the vertical scale
    for i in range(CANVAS_INNER_HEIGHT):
        # add the number of the row on the left of the row
        axis_text = (f'<text x="{0.5 * M}" y="{(i + 1.5) * M}" font-size="{0.35 * M}" fill="black" '
                     f'text-anchor="middle" '
                     f'dominant-baseline="middle" font-weight="bold">{i + 1}-{CANVAS_INNER_HEIGHT - i}</text>')
        doc = doc.replace('</svg>', axis_text + '\n</svg>')
        # also add it to the right of the image
        axis_text_right = (
            f'<text x="{(CANVAS_INNER_WIDTH + 1.5) * M}" y="{(i + 1.5) * M}" font-size="{0.35 * M}" fill="black" text-anchor="middle" '
            f'dominant-baseline="middle" font-weight="bold">{i + 1}-{CANVAS_INNER_HEIGHT - i}</text>')
        doc = doc.replace('</svg>', axis_text_right + '\n</svg>')
    return doc


def add_color_palette_background(doc: str) -> str:
    # add the color palette background
    palette = f'<rect x="{0}" y="{(CANVAS_HEIGHT - PALETTE_HEIGHT) * M}" width="{CANVAS_WIDTH * M}" height="{PALETTE_HEIGHT * M}" fill="gray" stroke="grau" stroke-width="{0}"/>'
    doc = doc.replace('</svg>', palette + '\n</svg>')
    return doc


def add_color_palette(doc: str, color_space: list) -> str:
    # add color space circles at the bottom, these are toggle elements, at hover they will toggle target elements.
    # add the color palette
    for idx, color in enumerate(color_space):
        r, g, b = color[:3]
        rank = get_color_rank(color, color_space)
        text_color = get_contrast_color(*color[:3])
        tr, tg, tb = text_color
        argument = f"'toggle-target-{rank}'"
        circle = (
            f'<circle class="toggle-element toggle-element-{rank}" cx="{(idx * RR * 2 + 1 + RR) * M}" cy="'
            f'{(CANVAS_HEIGHT - PALETTE_HEIGHT + RR) * M}" r="'
            f'{RR * M}" '
            f'fill="rgb'
            f'({r}'
            f',{g}'
            f',{b})" stroke="gray" '
            f'stroke-width="0.02" '
            f'onclick="toggleVisibilityByClass({argument})" '
            f'/>')
        text = (
            f'<text class="toggle-element toggle-element-{rank}" x="{(idx * RR * 2 + 1 + RR) * M}" y="'
            f'{(CANVAS_HEIGHT - PALETTE_HEIGHT + RR) * M}" '
            f'font-size="{0.35 * M}" '
            f'fill="rgb({tr},{tb},{tg})" text-anchor="middle" '
            f'dominant-baseline="middle">{idx + 1}</text>')
        doc = doc.replace('</svg>', circle + '\n</svg>')
        doc = doc.replace('</svg>', text + '\n</svg>')
    return doc


def add_circles(doc: str, img: Image, color_space: list) -> str:
    # for each pixel, create a circle with the color of the pixel using svg
    # these circles are target elements
    width, height = img.size

    for i in range(width):
        for j in range(height):
            color = img.getpixel((i, j))
            rank = get_color_rank(color, color_space) if color_space else ''
            r, g, b = color[:3]
            circle = (f'<circle class="toggle-target toggle-target-{rank}" cx="{(i + 1.5) * 10}" cy="'
                      f'{(j + 1.5) * M}" r="{R * M}" '
                      f'fill="rgb({r},{g}'
                      f',{b})" stroke="gray" '
                      f'stroke-width="0.02" opacity="0.2"/>')
            # add a square with a very thiny gray border
            square = f'<rect x="{i + 1}" y="{j + 1}" width="1" height="1" fill="none" stroke="gray" stroke-width="0.01" />'
            # create a circle
            content = rank
            text_color = get_contrast_color(*color[:3])
            r, g, b = text_color
            text = (f'<text class="toggle-target toggle-target-{rank}" x="{(i + 1 + R) * M}" y="{(j + 1 + R) * M}" '
                    f'font-size="{0.35 * M}" '
                    f'fill="rgb({r},{g}'
                    f',{b})" text-anchor="middle" '
                    f'dominant-baseline="middle" opacity="0.2">{content}</text>')
            doc = doc.replace('</svg>', circle + '\n</svg>')
            doc = doc.replace('</svg>', square + '\n</svg>')
            doc = doc.replace('</svg>', text + '\n</svg>')
    return doc


def add_on_off_buttons(doc: str) -> str:
    # create on and off buttons next to the color palette so that the user can toggle the visibility of the circles
    on_button = f'<rect x="{(CANVAS_WIDTH - 4.5) * M}" y="{(CANVAS_HEIGHT - PALETTE_HEIGHT + 0.5) * M}" width="{2 * M}" height="{1 * M}" fill="green" stroke="gray" stroke-width="0.02" onclick="setVisibilityByClassOn(\'toggle-target\')"/>'
    on_text = f'<text x="{(CANVAS_WIDTH - 4.0) * M}" y="{(CANVAS_HEIGHT - PALETTE_HEIGHT + 1.0) * M}" font-size="{0.35 * M}" fill="black" text-anchor="middle" dominant-baseline="middle">ON</text>'

    off_button = f'<rect x="{(CANVAS_WIDTH - 2.5) * M}" y="{(CANVAS_HEIGHT - PALETTE_HEIGHT + 0.5) * M}" width="{2 * M}" height="{1 * M}" fill="red" stroke="gray" stroke-width="0.02" onclick="setVisibilityByClassOff(\'toggle-target\')"/>'
    off_text = f'<text x="{(CANVAS_WIDTH - 2.0) * M}" y="{(CANVAS_HEIGHT - PALETTE_HEIGHT + 1.0) * M}" font-size="{0.35 * M}" fill="black" text-anchor="middle" dominant-baseline="middle">OFF</text>'

    doc = doc.replace('</svg>', on_button + '\n' + on_text + '\n' + off_button + '\n' + off_text + '\n</svg>')
    return doc


def add_grid_lines(doc: str) -> str:
    # add grid lines
    for i in range(CANVAS_INNER_WIDTH):
        # add vertical lines
        line = f'<line x1="{(i + 1 + R) * M}" y1="{(1 + R) * M}" x2="{(i + 1 + R) * M}" y2="{(CANVAS_INNER_HEIGHT + R) * M}" stroke="gray" stroke-width="0.01"/>'
        doc = doc.replace('</svg>', line + '\n</svg>')
    for i in range(CANVAS_INNER_HEIGHT):
        # add horizontal lines
        line = f'<line x1="{(1 + R) * M}" y1="{(i + 1 + R) * M}" x2="{(CANVAS_INNER_WIDTH + R) * M}" y2="{(i + 1 + R) * M}" stroke="gray" stroke-width="0.01"/>'
        doc = doc.replace('</svg>', line + '\n</svg>')
    return doc


def img_to_circles(img_file: str, color_space: list = None):
    # read the image
    img = Image.open(img_file)
    circles = base_doc()
    # circles = add_style(circles)
    circles = add_script(circles)
    circles = add_border(circles)
    circles = add_horizontal_scale(circles)
    circles = add_vertical_scale(circles)
    circles = add_grid_lines(circles)
    circles = add_color_palette_background(circles)
    circles = add_color_palette(circles, color_space)
    circles = add_circles(circles, img, color_space)
    circles = add_square_tiles(circles, 3)
    circles = add_on_off_buttons(circles)

    # create the svg
    svg = circles
    # replace fileextension in img_file to svg
    img_file = img_file.rsplit('.', 1)[0]
    img_file += '.svg'

    # save the svg file
    print(f"Saving the svg file to {img_file}")
    with open(img_file, 'w') as f:
        f.write(svg)

    # make the svg file writable
    os.chmod(img_file, 0o777)
    return img_file
