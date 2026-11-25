"""Preserve the salon's original URLs when moving the site to a new domain or host."""
from pathlib import Path

UPLOADS = 'wgc1/wp-content/uploads/2023/07/'
ORIGIN = 'https://grace-2012.com/' + UPLOADS
FILES = ('rogo.jpg', 'IMG_9091-1.jpg', 'IMG_9091-2.jpg', 'shinsotusaiyou.jpg', 'tyuuto2.jpg', 'part2.jpg')


def source(filename, dist, relative_path):
    if filename not in FILES:
        raise ValueError(f'Unknown original image {filename}')
    key = UPLOADS + filename
    return relative_path(key) if (Path(dist) / key).is_file() else ORIGIN + filename
