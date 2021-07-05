#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   main.py
@License :   (C)Copyright 2020

@Modify Time        @Author    @Version    @Desciption
----------------    -------    --------    -----------
2020-07-01 14:02    yuyang     1.0         None
'''
# THIS FILE IS PART OF fakeCLP PROJECT

from core.template import Blue440x140, Yellow440x140, Green480x140, Yellow440x220, Black440x140, White440x140, White440x220
from core.augment import *
from core.utils import *

import os
import shutil
import tqdm

num = 5000

color = {
    'yellow440x220': Yellow440x220,
    'yellow440x140': Yellow440x140,
    'white440x140': White440x140,
    'white440x220': White440x220,
    'black440x140': Black440x140,
    'blue440x140': Blue440x140,
    'green480x140': Green480x140,
}

dir_path = 'fakeclp'
if os.path.isdir(dir_path):
    shutil.rmtree(dir_path)

for name in color.keys():
    os.makedirs(os.path.join(dir_path, name), exist_ok=True)


for key, value in color.items():
    kwargs = {}
    kwargs['width'] = 1100
    kwargs['height'] = 500 if '220' in key else 300
    for _ in tqdm.tqdm(range(num)):
        code, plate = value()()

        background = Background(**kwargs)()

        plate = random_distort(plate)
        img = plate

        # background = random_distort(background)
        # background = random_rotate(background)
        #
        # img = putPatchOn(plate, background)
        #
        # h, w = img.shape[:2]
        # img = randon_crop_and_zoom(img, (w, h))
        # img = random_perspective(img)
        img = random_blur(img)
        img = random_add_smu(img)

        # cv2.imshow('img', img)
        # cv2.waitKey()

        cv_imwrite(os.path.join(os.path.join(dir_path, f'{key}'), '{}.jpg'.format(code)), 
                   img)



# for _ in tqdm.tqdm(range(50)):
#     # code, plate = Blue440x140()()
#     code, plate = White440x140()()
#
#     background = Background(width=1100, height=300)()
#
#     plate = random_distort(plate)
#
#     background = random_distort(background)
#     background = random_rotate(background)
#
#     img = putPatchOn(plate, background)
#
#     h, w = img.shape[:2]
#     img = randon_crop_and_zoom(img, (w, h))
#     img = random_perspective(img)
#     img = random_blur(img)
#     img = random_add_smu(img)
#
#     # cv2.imshow('img', img)
#     # cv2.waitKey()
#
#     cv_imwrite(os.path.join(os.path.join(dir_path, 'blue440x140'), '{}.jpg'.format(code)), img)
#
# for _ in tqdm.tqdm(range(500)):
#     code, plate = Yellow440x140()()
#
#     background = Background(width=1100, height=300)()
#
#     plate = random_distort(plate)
#
#     background = random_distort(background)
#     background = random_rotate(background)
#
#     img = putPatchOn(plate, background)
#
#     h, w = img.shape[:2]
#     img = randon_crop_and_zoom(img, (w, h))
#     img = random_perspective(img)
#     img = random_blur(img)
#     img = random_add_smu(img)
#
#     # cv2.imshow('img', img)
#     # cv2.waitKey()
#
#     cv_imwrite(os.path.join(os.path.join(dir_path, 'yellow440x140'), '{}.jpg'.format(code)), img)
#
# for _ in tqdm.tqdm(range(500)):
#     code, plate = Green480x140()()
#
#     background = Background(width=1100, height=300)()
#
#     plate = random_distort(plate)
#
#     background = random_distort(background)
#     background = random_rotate(background)
#
#     img = putPatchOn(plate, background)
#
#     h, w = img.shape[:2]
#     img = randon_crop_and_zoom(img, (w, h))
#     img = random_perspective(img)
#     img = random_blur(img)
#     img = random_add_smu(img)
#
#     # cv2.imshow('img', img)
#     # cv2.waitKey()
#
#     cv_imwrite(os.path.join(os.path.join(dir_path, 'green480x140'), '{}.jpg'.format(code)), img)
#
#
