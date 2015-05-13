from PIL import Image, ImageOps

CROP_TARGET = {
    'l': 0,
    'c': 0.5,
    'r': 1,
    't': 0,
    'm': 0.5,
    'b': 1,
}


def resize(img, size=(100, 100)):
    img.thumbnail(size, resample=Image.ANTIALIAS)
    return img


def scale_and_crop(img, size=(100, 100), crop=False, target=None):
    if crop is False:
        return resize(img, size)
    else:
        target = target if target else 'cm'
        if size[0] > img.size[0] or size[1] > img.size[1]:  # too big
            return img
        startx, starty = target
        trans_target = (CROP_TARGET[startx], CROP_TARGET[starty])
        return ImageOps.fit(img, size, Image.ANTIALIAS, 0, trans_target)


def fill(img, size, colour=(255, 255, 255, 0)):
    img = resize(img, size)
    # generating the thumbnail from given size
    img.thumbnail(size, Image.ANTIALIAS)
    offset_x = max((size[0] - img.size[0]) / 2, 0)
    offset_y = max((size[1] - img.size[1]) / 2, 0)
    offset_tuple = (offset_x, offset_y)  # pack x and y into a tuple
    # create the image object to be the final product
    canvas = Image.new(mode='RGBA', size=size, color=colour)
    #  paste the thumbnail into the full sized image
    canvas.paste(img, offset_tuple)
    return canvas
