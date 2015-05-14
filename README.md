## Introduction

responsive-img allows an image to be resized, cropped, or have a background fill
added by adding optional parameters to the basename of an image file.

Django handles resizing, but issues a redirect once the image is created,
avoiding the problems of serving images from the Django app.


## Installation

Install the package with:

    `pip install -e git+git@github.com:kipparker/responsive-img.git@master#egg=reponsive-img`

Import the resize url generator into your root urls.py file

    from responsive.media_urls import responsive_urls

And the following line **after** all other url rules

    urlpatterns += responsive_urls()

And in settings.py

    DEV_RESIZE_SERVER = False | True

Set to True if using the Django dev server to serve media files

## Server configuration

Responsive relies on an upstream server that will serve files if they exist,
falling back to the responsive app on a 404.

### Sample Nginx config

See the conf/ folder for sample configurations

## Resizing options

>  http://media-server.com/media/image-200x300.jpg

Will create a thumbnail preserving aspect ratio, with a maximum width of 200
pixels and a maximum height of 300 pixels

>  http://media-server.com/media/image-200x300-crop.jpg

Exactly 200x300, cropped as necessary, with crop point at centre and middle.

>  http://media-server.com/media/image-200x300-crop=lm.jpg

As for crop, but with a custom crop point. Accepted values are:

For the first character:

- l = Left
- c = Center
- r = Right

For the second character

- t = Top
- m = Middle
- b = Bottom

>  http://media-server.com/media/image-200x300-fill=255,124,123,1.jpg

Resize the image proportionally, and pastes it onto a canvas 200x300 pixels,
with a background rgba(255,124,123,1).

Will also accept three numbers for a RGB colour.

Only PNG images will respect the alpha channel argument.

## Admin widget

AdminImageWidget in widgets.py adds a Responsive generated thumbnail to an admin
ImageField.

Import the widget

    from responsive.widgets import AdminImageWidget

And override it for ImageFields:

    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget}
    }


## Template tags

The thumb tag will generate the correct url.

You will need to add 'responsive' to your installed apps to use it.

    {% thumb url '200x200' 'crop=cm' %}
