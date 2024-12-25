from PIL import Image


def get_image(image_path: str = '/Users/mehmet.selim.onat/PycharmProjects/bausteine/src/pics/image.png') -> Image:
    """Get the image from the path"""
    return Image.open(image_path)


def pixelate_image(image: Image, width: int, height: int) -> Image:
    """Pixelate the image"""
    # TODO: keep the aspect ratio
    img_res = image.resize((width, height))
    if img_res.mode == 'RGBA':
        img_res = img_res.convert('RGB')

    # save the resized img to a file
    # img_res.save('/Users/mehmet.selim.onat/PycharmProjects/bausteine/src/pics/resized.jpg')
    return img_res


if __name__ == '__main__':
    img = get_image('/Users/mehmet.selim.onat/PycharmProjects/bausteine/src/pics/IMG_1161.JPG')
    pixelate_image(img, 30, 30)
    print("Pixelated image saved as 'resized.png'")
