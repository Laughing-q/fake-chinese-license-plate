import glob
import cv2
import os.path as osp
from core.augment import random_perspective
from tqdm import tqdm
from pathlib import Path
import random

# img_paths = glob.glob('cut_out/*')
#
# for i, p in enumerate(tqdm(img_paths, total=len(img_paths))):
#     img = cv2.imread(p)
#     # img = cv2.resize(img, (160, 50))
#     # name = Path(p).name
#     # if random.random() > 0.5:
#     #     img = random_perspective(img)
#     # print(name)
#     # cv2.imwrite(osp.join("cut_final", f"{name}"), img)
#
#     cv2.imshow('p', img)
#     if cv2.waitKey(0) == ord('q'):
#         break

img_paths = glob.glob("/dataset/dataset/lpr/train/rect_img/*/*")
random.shuffle(img_paths)
# print(len(img_paths))
for i, p in enumerate(tqdm(img_paths[:10000], total=10000)):
    img = cv2.imread(p)
    # img = cv2.resize(img, (160, 50))
    name = Path(p).name
    name = name[:name.find('_')]
    length = len(name)
    # print(name, len(name))
    if length == 0:
        continue

    ratio = random.randrange(2, length - 2)
    # print(ratio)
    left_name = name[:ratio]
    right_name = name[ratio:]
    # print(left_name, right_name)
    h, w = img.shape[:2]
    nw = int(w * ratio / length)
    left_plate = img[:, :nw, :]
    right_plate = img[:, nw:, :]
    cv2.imwrite(osp.join("real_final", f"{left_name}_{i}.jpg"), left_plate)
    cv2.imwrite(osp.join("real_final", f"{right_name}_{i}.jpg"), right_plate)
