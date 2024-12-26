import numpy as np
from src.utils.image import pixelate_image, get_image
from src.utils.color_space import get_color_resources, get_color_space, get_closest_color
from src.utils.config import WIDTH, HEIGHT
from src.utils.svg import img_to_circles


def image_to_circles(img_file='/Users/mehmet.selim.onat/PycharmProjects/bausteine/src/pics/IMG_1154.JPG',
                     no_limit=False):
    """
    Convert the image to circles where the color of the circle is the closest color in the color space.
    Saves two artefacts: the image with the closest color and an SVG file with the circles to the result folder.
    """
    print(f"Processing {img_file}")
    # extract the path, filename, and extension
    path, filename = img_file.rsplit('/', 1)
    # results path
    path_results = f"{path}/results/"
    filename, ext = filename.rsplit('.', 1)
    filename_matched = f"{filename}color_matched.png"
    path_matched = f"{path_results}{filename_matched}"

    # get the color space
    color_space = get_color_space()

    # get the color resources
    color_resources = get_color_resources(color_space)
    if no_limit:
        color_resources['n'] = np.Inf

    # get the image and pixelate it
    img = get_image(img_file)
    img = pixelate_image(img, WIDTH, HEIGHT)
    img = img.convert('RGBA')

    # zip x and y coordinates
    x = np.tile(np.arange(WIDTH), HEIGHT)
    y = np.repeat(np.arange(HEIGHT), WIDTH)
    coordinates = list(zip(x, y))
    # randomize the coordinates
    np.random.shuffle(coordinates)
    # run across the coordinates
    # # Matching: for each pixel get the color and match it to the closest color in the color space
    for i, j in coordinates:
        # color of the pixel
        color = img.getpixel((i, j))

        # drop rows where the count is 0
        color_resources = color_resources[color_resources['n'] != 0]
        # check if color_resources is empty

        # convert each index entry of color_resources to a tuple using eval
        current_color_space = [eval(index) for index in color_resources.index]

        # get the closest color in the color space
        c_color = get_closest_color(color, current_color_space, p_second_closest=0)

        # decrease the count of the closest color in the color resources
        if str(c_color) in color_resources.index:
            color_resources.loc[str(c_color)] -= 1

        # add the alpha channel to the color
        # c_color = (*c_color)
        # print position and actual color
        print(f"Position: ({i}, {j}) --> Actual Color: {color}, Closest Color {c_color}")
        # replace the color with the closest color in the color space
        img.putpixel((i, j), c_color)

    # save the image
    img.save(path_matched)

    # save an SVG file with the circles where the color is the closest color in the color space
    img_to_circles(path_matched, color_space)


def convert_all(folder='/Users/mehmet.selim.onat/PycharmProjects/bausteine/src/pics'):
    def list_files(folder):
        import os
        files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        # exclude hidden files
        files = [f for f in files if not f.startswith('.')]
        return files

    # list files in the folder that are images
    files = list_files(folder)

    for file in files:
        print(f"Processing {file}")
        image_to_circles(f"{folder}/{file}")


if __name__ == '__main__':
    convert_all()
