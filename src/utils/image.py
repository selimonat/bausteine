from PIL import Image


def get_image(image_path: str = '/Users/mehmet.selim.onat/PycharmProjects/bausteine/src/pics/image.png') -> Image:
    """Get the image from the path"""
    return Image.open(image_path)


def pixelate_image(image: Image, width: int, height: int) -> Image:
    """Pixelate the image"""
    # extract from image a central square portion
    w, h = image.size
    # take the smallest dimension
    size = min(w, h)
    # take the central square
    left = (w - size) / 2
    top = (h - size) / 2
    right = (w + size) / 2
    bottom = (h + size) / 2
    image = image.crop((left, top, right, bottom))
    #
    img_res = image.resize((width, height))
    if img_res.mode == 'RGBA':
        img_res = img_res.convert('RGB')

    # save the resized img to a file
    # img_res.save('/Users/mehmet.selim.onat/PycharmProjects/bausteine/src/pics/resized.jpg')
    return img_res


if __name__ == '__main__':
    img = get_image('/src/pics/reserve/IMG_1161.JPG')
    pixelate_image(img, 30, 30)
    print("Pixelated image saved as 'resized.png'")
