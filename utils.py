from pygame.transform import scale as pg_scale
from pygame import image as pg_image

def scale_img(img_path, d_width=None, d_height=None):
    img = pg_image.load(img_path)
    raw_width, raw_height = img.get_size()
    if d_width is None and d_height is None:
        return img
    elif d_width is None and d_height is not None:
        scale_factor = d_height / raw_height
        d_width = int(raw_width * scale_factor)
        return pg_scale(img, (d_width, d_height))
    elif d_height is None and d_width is not None:
        scale_factor = d_width / raw_width
        d_height = int(raw_height * scale_factor)
        return pg_scale(img, (d_width, d_height))
    if d_width is not None and d_height is not None:
        scale_img(img_path, d_width)