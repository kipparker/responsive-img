import itertools
import re

from PIL import Image, ImageOps

CROP_TARGET = {
    'l':0,
    'c':0.5,
    'r':1,
    't':0,
    'm':0.5,
    'b':1,
}

from . import utils

def resize(img, size=(100,100)):
    img.thumbnail(size, resample=Image.ANTIALIAS)
    return img

def scale_and_crop(img, size=(100,100), crop=False, target=None):
    if crop == False:
        return resize(img, size)
    else:
        target =  target if target else 'cm'
        if size[0] > img.size[0] or size[1] > img.size[1]:#too big
            return img
        startx, starty = target
        trans_target = (CROP_TARGET[startx], CROP_TARGET[starty])
        return ImageOps.fit(img, size, Image.ANTIALIAS, 0, trans_target)

def fill(img, size, colour=(255,255,255,0)):
    img = resize(img, size)
    img.thumbnail(size, Image.ANTIALIAS) #generating the thumbnail from given size
    offset_x = max((size[0] - img.size[0]) / 2, 0)
    offset_y = max((size[1] - img.size[1]) / 2, 0)
    offset_tuple = (offset_x, offset_y) #pack x and y into a tuple
    canvas = Image.new(mode='RGBA', size=size, color=colour) #create the image object to be the final product
    canvas.paste(img, offset_tuple) #paste the thumbnail into the full sized image
    return canvas

def colorspace(img, bw=False, replace_alpha=False, **kwargs):
    """
    Convert images to the correct color space.

    A passive option (i.e. always processed) of this method is that all images
    (unless grayscale) are converted to RGB colorspace.

    This processor should be listed before :func:`scale_and_crop` so palette is
    changed before the image is resized.

    bw
        Make the thumbnail grayscale (not really just black & white).

    replace_alpha
        Replace any transparency layer with a solid color. For example,
        ``replace_alpha='#fff'`` would replace the transparency layer with
        white.

    """
    if img.mode == 'I':
        # PIL (and pillow) have can't convert 16 bit grayscale images to lower
        # modes, so manually convert them to an 8 bit grayscale.
        img = img.point(list(_points_table()), 'L')

    is_transparent = utils.is_transparent(img)
    is_grayscale = img.mode in ('L', 'LA')
    new_mode = img.mode
    if is_grayscale or bw:
        new_mode = 'L'
    else:
        new_mode = 'RGB'

    if is_transparent:
        if replace_alpha:
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            base = Image.new('RGBA', img.size, replace_alpha)
            base.paste(img, mask=img)
            img = base
        else:
            new_mode = new_mode + 'A'

    if img.mode != new_mode:
        img = img.convert(new_mode)

    return img
