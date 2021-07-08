import shutil
import glob
import tqdm

paths = glob.glob('/e/datasets/License_plates/recognition/*/*')
for p in tqdm.tqdm(paths, total=len(paths)):
    shutil.copy(p, '/e/datasets/License_plates/recognition_bigger')
