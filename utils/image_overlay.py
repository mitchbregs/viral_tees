import argparse
import cv2
import datetime
import numpy as np
import os
from .constants import SRC_DIR
from pathlib import Path
from PIL import ImageFont, ImageDraw, Image


def resize_img(image):
    height, width = image.shape[:2]
    max_height = 100000
    max_width = 300

    # only shrink if img is bigger than required
    if max_height < height or max_width < width:
        # get scaling factor
        scaling_factor = max_height / float(height)
        if max_width/float(width) < scaling_factor:
            scaling_factor = max_width / float(width)
        # resize image
        image = cv2.resize(image, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)

    return image


def overlay_transparent(background, overlay, x, y):
    background_width, background_height = background.shape[:2]

    if x >= background_width or y >= background_height:
        return background

    h, w = overlay.shape[:2]

    if x + w > background_width:
        w = background_width - x
        overlay = overlay[:, :w]

    if y + h > background_height:
        h = background_height - y
        overlay = overlay[:h]

    if overlay.shape[2] < 4:
        overlay = np.concatenate(
            [
                overlay,
                np.ones((overlay.shape[0], overlay.shape[1], 1), dtype = overlay.dtype) * 255
            ],
            axis=2,
        )

    overlay_image = overlay[..., :3]
    mask = overlay[..., 3:] / 255.0

    background[y:y+h, x:x+w] = (1.0 - mask) * background[y:y+h, x:x+w] + mask * overlay_image

    return background


def get_coordinates(background, overlay):
    half, extra_half = background.shape[1]/2, overlay.shape[1]/2
    return int(half - extra_half), 175


def crop_image(y, x, image):
    h, w = image.shape[:2]
    return image[y:y + h, x:x + w]


def add_text(img, trend_name):
    today = str(datetime.datetime.today().strftime('%m-%d-%Y'))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    pil_img = Image.fromarray(img)
    draw = ImageDraw.Draw(pil_img)

    font = ImageFont.truetype('{}/static/LinLibertine_aS.ttf'.format(str(SRC_DIR)), 15)
    draw.text((250, 150),
              '{} trending on {}'.format(trend_name, today),
              font=font,
              fill=(153, 153, 153, 1))

    img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    return img


def run(args_dict):
    background = cv2.imread(args_dict['background'])
    overlay = cv2.imread(args_dict['image'])
    overlay = resize_img(overlay)

    if overlay.shape[0] > 180:
        overlay = crop_image(overlay.shape[0]-180, 0, overlay)

    x, y = get_coordinates(background, overlay)

    img = overlay_transparent(background, overlay, x, y)

    trend_name = args_dict['name']
    img = add_text(img, trend_name)

    return img


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Overlay cropped image on background t-shirt')
    parser.add_argument('-i', '--image', required=True,
        help='Path to overlay image on background t-shirt.')
    parser.add_argument('-n', '--name', required=True,
        help='Name of trend dicionary for text overlay.')
    parser.add_argument('-b', '--background', required=False,
        default='/home/git/viral_tees/static/background.jpg',
        help='Path to overlay image on t-shirt.')
    parser.add_argument('-o', '--output', required=True,
        help='Path to image output.')

    args_dict = vars(parser.parse_args())

    run(args_dict)


