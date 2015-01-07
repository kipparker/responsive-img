from PIL import Image, ImageOps, ImageDraw, ImageChops
from resizr import processors
from unittest import TestCase
from resizr.utils import is_transparent

def create_image(mode='RGB', size=(800, 600)):
    image = Image.new(mode, size, (255, 255, 255))
    draw = ImageDraw.Draw(image)
    x_bit, y_bit = size[0] // 10, size[1] // 10
    draw.rectangle((x_bit, y_bit * 2, x_bit * 7, y_bit * 3), 'red')
    draw.rectangle((x_bit * 2, y_bit, x_bit * 3, y_bit * 8), 'red')
    return image


class CropTest(TestCase):
    def assertImagesEqual(self, im1, im2, msg=None):
        if im1.size != im2.size or (
                ImageChops.difference(im1, im2).getbbox() is not None):
            raise self.failureException(
                msg or 'The two images were not identical')

    def test_crop(self):
        image = create_image()

        cropped = processors.scale_and_crop(image, (100, 100), crop=True)
        self.assertEqual(cropped.size, (100, 100))

        not_cropped = processors.scale_and_crop(image, (1000, 1000), crop=True)
        self.assertEqual(not_cropped.size, (800, 600))

        resize = processors.scale_and_crop(image, (100, 100))
        self.assertEqual(resize.size, (100, 75))

    def test_fill(self):
        image = create_image()
        filled = processors.fill(image, (100, 100), colour=(1,2,3,0))
        self.assertEqual(filled.size, (100, 100))
        self.assertEqual(is_transparent(filled), True)
