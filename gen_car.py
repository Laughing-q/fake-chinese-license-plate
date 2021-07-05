import os
import os.path as osp
import glob
import cv2
import numpy as np
import time
import random
from pathlib import Path
from tqdm import tqdm

label_map = {
    'white440x140': 0,
    'white440x220': 0,
    'black440x140': 1,
    'yellow440x140': 2,
    'yellow440x220': 2,
}

ccpd_dir = '/d/baidubase/CCPD2019/ccpd_base'
ccpd_paths = glob.glob(osp.join(ccpd_dir, '*'))
random.shuffle(ccpd_paths)

license_dir = '/d/projects/fake-chinese-license-plate/fakeclp'
license_paths = glob.glob(osp.join(license_dir, '*220*', '*'))

save_dir = '/e/datasets/License_plates/new_220'
img_dir = osp.join(save_dir, 'images')
label_dir = osp.join(save_dir, 'labels')
os.makedirs(img_dir, exist_ok=True)
os.makedirs(label_dir, exist_ok=True)

# for ccpd_path in ccpd_paths:
for i, license_path in tqdm(enumerate(license_paths), total=len(license_paths)):
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

    ccpd_path = ccpd_paths[i]
    ccpd_name = osp.basename(ccpd_path)
    img = cv2.imread(ccpd_path)
    img_h, img_w, _ = img.shape

    points = ccpd_name.split('-')[3]
    points = [int(p) for ps in points.split('_') for p in ps.split('&')]

    dst_pst = np.float32(np.split(np.array(points), 4))
    # for two line license plate
    # approx_license_h = dst_pst.max(0)[1] - dst_pst.min(0)[1]
    # dst_pst[[0, 1], 1] += approx_license_h * 0.5

    M = cv2.getPerspectiveTransform(origin_pst, dst_pst)

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

    new = cv2.warpPerspective(license, M, dsize=(img_w, img_h))
    new_mask = cv2.warpPerspective(mask, M, dsize=(img_w, img_h))
    # cv2.imshow('n', new)
    # cv2.imshow('nm', new_mask)

    img[new_mask.astype(bool)] = new[new_mask.astype(bool)]

    # cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 0), thickness=2)
    # for i, p in enumerate(range(0, len(points), 2)):
    #     cv2.putText(img, f'{i}', (points[p], points[p + 1]), cv2.FONT_HERSHEY_SIMPLEX, 2, color=(0, 0, 255))
    cv2.imwrite(osp.join(img_dir, f'{license_color}_{license_name}_{i}.jpg'), img)
    dst_pst[:, 0] /= img_w
    dst_pst[:, 1] /= img_h
    points = dst_pst.reshape(-1)
    str_label = f"{label_map[license_color]} {x / img_w} {y / img_h} {wb / img_w} {hb / img_h}"
    for p in points:
        str_label += f" {p}"
    str_label += '\n'
    with open(osp.join(label_dir, f'{license_color}_{license_name}_{i}.txt'), 'a') as f:
        f.write(str_label)
    # cv2.imshow('p', img)
    # cv2.waitKey(0)
