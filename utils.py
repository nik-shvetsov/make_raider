from pygame.transform import scale as pg_scale
from pygame import image as pg_image

def scale_img(img_path, d_width):
    img = pg_image.load(img_path)
    raw_width, raw_height = img.get_size()
    scale_factor = d_width / raw_width
    d_height = int(raw_height * scale_factor)
    return pg_scale(img, (d_width, d_height))