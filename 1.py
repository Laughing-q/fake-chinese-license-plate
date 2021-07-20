import shutil
import glob
import tqdm
import os
import os.path as osp
from multiprocessing.pool import ThreadPool, Pool

source_dir = '/d/projects/fake-chinese-license-plate/fakeclp0709'
target_dir = '/d/projects/fake-chinese-license-plate/test'

os.makedirs(target_dir, exist_ok=True)

paths = glob.glob(osp.join(source_dir, '**', '*.jpg'), recursive=True)
print(len(paths))
# for p in paths:
#     if not p.endswith('.jpg'):
#         print(p)

# for p in tqdm.tqdm(paths, total=len(paths)):
#     shutil.copy(p, target_dir)


pbar = tqdm.tqdm(ThreadPool().imap(lambda x: shutil.copy(*x), [(p, target_dir) for p in paths]), total=len(paths))
for _ in pbar:
    pass
    pbar.desc = 'copy images'
pbar.close()
