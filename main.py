#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    :   main.py
@License :   (C)Copyright 2020

@Modify Time        @Author    @Version    @Desciption
----------------    -------    --------    -----------
2020-07-01 14:02    yuyang     1.0         None
"""
# THIS FILE IS PART OF fakeCLP PROJECT

from core.template import (
    Blue440x140,
    Yellow440x140,
    Green480x140,
    Yellow440x220,
    Black440x140,
    White440x140,
    White440x220,
)
from core.augment import *
from core.utils import *

import os
import shutil
import time
import tqdm
from PIL import Image
from multiprocessing.pool import Pool, ThreadPool

num = 3000
recognition = False

resize = False


color = {
    "yellow440x220": Yellow440x220,
    "yellow440x140": Yellow440x140,
    "white440x140": White440x140,
    "white440x220": White440x220,
    "black440x140": Black440x140,
    "blue440x140": Blue440x140,
    "green480x140": Green480x140,
}

dir_path = "fakeclp0720"
# if os.path.isdir(dir_path):
#     shutil.rmtree(dir_path)

for name in color.keys():
    os.makedirs(os.path.join(dir_path, name), exist_ok=True)

hue = 18 if recognition else 4


def generate_one(args):
    key, value = args
    code, plate = value()()

    plate = random_distort(
        plate, hue=hue
    )  # this augment may change the color, only for car recognition, not for car detection which classify colors
    img = plate

    # background = Background(**kwargs)()
    # # print(background.shape)
    #
    # background = random_distort(background)
    # background = random_rotate(background)
    #
    # img = putPatchOn(plate, background)

    # h, w = img.shape[:2]
    # img = randon_crop_and_zoom(img, (w, h))
    # img = random_perspective(img)
    if not recognition:
        img = random_blur(img, sigma=30)
        img = random_add_smu(img)
    # print(img.shape)

    if resize:
        img = cv2.resize(img, (94, 24))
        # cv2.imshow('img', cv2.resize(img, (94, 24)))
    # cv2.imshow('img', img)
    # if cv2.waitKey(0) == ord('q'):
    #     break

    # img = Image.fromarray(img)
    # img.save(os.path.join(os.path.join(dir_path, f'{key}'), '{}_{}.jpg'.format(code, key)))
    cv_imwrite(
        os.path.join(os.path.join(dir_path, f"{key}"), "{}_{}.jpg".format(code, key)),
        img,
    )


for key, value in color.items():
    kwargs = {}
    kwargs["width"] = 980
    kwargs["height"] = 500 if "220" in key else 300
    with Pool() as p:
        pbar = tqdm.tqdm(
            p.imap(generate_one, [(key, value) for _ in range(num)]), total=num
        )
        for i in pbar:
            pass

    # for _ in tqdm.tqdm(range(num)):
    #     t1 = time.time()
    #     code, plate = value()()
    #
    #
    #     plate = random_distort(plate, hue=4)  # this augment may change the color, only for car recognition, not for car detection which classify colors
    #     img = plate
    #
    #     # background = Background(**kwargs)()
    #     # print(background.shape)
    #
    #     # background = random_distort(background)
    #     # background = random_rotate(background)
    #
    #     # img = putPatchOn(plate, background)
    #
    #     # h, w = img.shape[:2]
    #     # img = randon_crop_and_zoom(img, (w, h))
    #     # img = random_perspective(img)
    #     img = random_blur(img, sigma=30)
    #     img = random_add_smu(img)
    #     # print(img.shape)
    #
    #     if resize:
    #         img = cv2.resize(img, (94, 24))
    #         # cv2.imshow('img', cv2.resize(img, (94, 24)))
    #     # cv2.imshow('img', img)
    #     # if cv2.waitKey(0) == ord('q'):
    #     #     break
    #
    #     t2 = time.time()
    #     # img = Image.fromarray(img)
    #     # img.save(os.path.join(os.path.join(dir_path, f'{key}'), '{}_{}.jpg'.format(code, key)))
    #     cv_imwrite(os.path.join(os.path.join(dir_path, f'{key}'), '{}_{}.jpg'.format(code, key)),
    #                img)
    #     t3 = time.time()
    #     # print('save time:', t3 - t2)
    #     # print('generate time:', t2 - t1)


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
