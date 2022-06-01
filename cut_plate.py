import cv2
import glob
import os.path as osp
from pathlib import Path
from tqdm import tqdm
import random

# double
img_paths = glob.glob("fakeclp0720/*220/*")
for i, p in enumerate(tqdm(img_paths, total=len(img_paths))):
    img = cv2.imread(p)
    name = Path(p).name
    name = name[:name.find('_')]
    up_name = name[:2]
    down_name = name[2:]

    h, w = img.shape[:2]
    nh = int(h / 2.5)
    up_plate = img[0:nh, :, :]
    up_plate = cv2.resize(up_plate, (160, 50))
    down_plate = img[nh:, :, :]
    down_plate = cv2.resize(down_plate, (160, 50))
    cv2.imwrite(osp.join("cut_out", f"{up_name}_{i}.jpg"), up_plate)
    cv2.imwrite(osp.join("cut_out", f"{down_name}_{i}.jpg"), down_plate)
    # if cv2.waitKey(0) == ord('q'):
        # break

# single

# img_paths = glob.glob("fakeclp0720/*140/*")
# for i, p in enumerate(tqdm(img_paths, total=len(img_paths))):
#     img = cv2.imread(p)
#     img = cv2.resize(img, (160, 50))
#     name = Path(p).name
#     name = name[:name.find('_')]
#     length = len(name)
#     # print(len(name))
#
#     ratio = random.randrange(2, length - 2)
#     # print(ratio)
#     left_name = name[:ratio]
#     right_name = name[ratio:]
#     # print(left_name, right_name)
#     h, w = img.shape[:2]
#     nw = int(w * ratio / length)
#     left_plate = img[:, :nw, :]
#     right_plate = img[:, nw:, :]
#     cv2.imwrite(osp.join("cut_out", f"{left_name}_{i}.jpg"), left_plate)
#     cv2.imwrite(osp.join("cut_out", f"{right_name}_{i}.jpg"), right_plate)

    # cv2.imshow('p', left_plate)
    # cv2.imshow('p1', right_plate)
    # if cv2.waitKey(0) == ord('q'):
    #     break
