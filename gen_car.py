import os
import os.path as osp
import glob
import cv2
import numpy as np
import time
import shutil
import random
from pathlib import Path
from tqdm import tqdm
from multiprocessing.pool import Pool, ThreadPool

label_map = {
    'white440x140': 0,
    'white440x220': 0,
    'black440x140': 1,
    'yellow440x140': 2,
    'yellow440x220': 2,
    'blue440x140': 3,
    'green480x140': 4,
}
blue_green = [3, 4]

# True: cause there are existed blue and green license plates, just save image and generate label.
# False: Generate white, black and yellow license plates, then save image and label.
blue_or_green = False

show_only = False

ccpd_dir = '/d/baidubase/CCPD2019/ccpd_base'
ccpd_paths = glob.glob(osp.join(ccpd_dir, '*'))
random.shuffle(ccpd_paths)

license_dir = '/d/projects/fake-chinese-license-plate/fakeclp0720'
license_paths = glob.glob(osp.join(license_dir, '*220', '*'))
# print(len(license_paths))

save_dir = '/e/datasets/License_plates/detection/all_color0730'
img_dir = osp.join(save_dir, 'images')
label_dir = osp.join(save_dir, 'labels')
os.makedirs(img_dir, exist_ok=True)
os.makedirs(label_dir, exist_ok=True)


def generate_one_car(args):
    i, license_path = args
    ccpd_path = ccpd_paths[i]
    ccpd_name = osp.basename(ccpd_path)
    img = cv2.imread(ccpd_path)
    img_ori = img.copy()
    img_h, img_w, _ = img.shape

    points = ccpd_name.split('-')[3]
    points = [int(p) for ps in points.split('_') for p in ps.split('&')]

    dst_pst = np.float32(np.split(np.array(points), 4))
    # for two line license plate(220)
    approx_license_h = dst_pst.max(0)[1] - dst_pst.min(0)[1]
    dst_pst[[0, 1], 1] += approx_license_h * 0.5

    x1 = int(dst_pst[:, 0].min())
    y1 = int(dst_pst[:, 1].min())
    x2 = int(dst_pst[:, 0].max())
    y2 = int(dst_pst[:, 1].max())
    # # rects = ccpd_name.split('-')[2]
    # x1, y1, x2, y2 = [int(p) for ps in rects.split('_') for p in ps.split('&')]
    # # for two line license plate
    # y2 = int(approx_license_h * 0.5) + y2

    wb, hb = x2 - x1, y2 - y1
    x, y = x1 + wb / 2, y1 + hb / 2

    if not blue_or_green:
        license = cv2.imread(license_path)
        license_color = str(Path(license_path).parent.name)
        license_name = str(Path(license_path).name)
        # remove suffix
        license_name = license_name[:license_name.rfind('.')]

        mask = np.ones_like(license, dtype=np.float32) * 255

        h, w, _ = license.shape
        origin_pst = np.float32([[w, h],
                                 [0, h], 
                                 [0, 0],
                                 [w, 0]])

        M = cv2.getPerspectiveTransform(origin_pst, dst_pst)
        new = cv2.warpPerspective(license, M, dsize=(img_w, img_h))
        new_mask = cv2.warpPerspective(mask, M, dsize=(img_w, img_h))
        # cv2.imshow('n', new)
        # cv2.imshow('nm', new_mask)

        img[new_mask.astype(bool)] = new[new_mask.astype(bool)]

    if show_only:
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 0), thickness=2)
        for i, p in enumerate(range(0, len(points), 2)):
            cv2.putText(img, f'{i}', (points[p], points[p + 1]), cv2.FONT_HERSHEY_SIMPLEX, 2, color=(0, 0, 255))
        cv2.namedWindow('x', cv2.WINDOW_NORMAL)
        stack_img = np.concatenate([new, img_ori, img], axis=1)
        cv2.imshow('x', stack_img)
        if cv2.waitKey(0) == ord('q'):
            exit()
    else:
        if blue_or_green:
            shutil.copy(ccpd_path, img_dir)
        else:
            cv2.imwrite(osp.join(img_dir, f'{license_color}_{license_name}_{i}.jpg'), img)

        dst_pst[:, 0] /= img_w
        dst_pst[:, 1] /= img_h
        points = dst_pst.reshape(-1)
        if blue_or_green:
            str_label = f"{blue_green[1]} {x / img_w} {y / img_h} {wb / img_w} {hb / img_h}"
            label_name = osp.basename(osp.splitext(ccpd_path)[0]) + '.txt'
        else:
            str_label = f"{label_map[license_color]} {x / img_w} {y / img_h} {wb / img_w} {hb / img_h}"
            label_name = f'{license_color}_{license_name}_{i}.txt'
        for p in points:
            str_label += f" {p}"
        str_label += '\n'
        with open(osp.join(label_dir, label_name), 'a') as f:
            f.write(str_label)


# for ccpd_path in ccpd_paths:

# single process
# for i, license_path in tqdm(enumerate(license_paths), total=len(license_paths)):
#     generate_one_car((i, license_path))

# multi process
with Pool() as p:
    pbar = tqdm(p.imap(generate_one_car, [(i, license_path) for i, license_path in enumerate(license_paths)]), total=len(license_paths))
    for _ in pbar:
        pass
