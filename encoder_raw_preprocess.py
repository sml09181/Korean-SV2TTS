import os
import shutil
from tqdm import tqdm

SRC_ROOT = "/GENERATION/enc003"
DST_ROOT = "/GENERATION/enc003_spkr"

cnt = 0
for folder in tqdm(os.listdir(SRC_ROOT)):
    folder_path = os.path.join(SRC_ROOT, folder, "data")
    for sub_folder in tqdm(os.listdir(folder_path)):
        sub_folder_path = os.path.join(folder_path, sub_folder)
        if sub_folder_path.endswith('.zip'): continue
        for sub_folder_ in os.listdir(sub_folder_path):
            sub_folder_path_ = os.path.join(sub_folder_path, sub_folder_)
            for date_folder in os.listdir(sub_folder_path_):
                date_folder_path = os.path.join(sub_folder_path_, date_folder)
                for speaker_id in os.listdir(date_folder_path):
                    src_folder_path = os.path.join(date_folder_path, speaker_id)
                    dst_folder = os.path.join(DST_ROOT, speaker_id)
                    if not os.path.exists(dst_folder): os.makedirs(dst_folder)
                    for filename in os.listdir(src_folder_path):
                        src_file = os.path.join(src_folder_path, filename)
                        if os.path.isfile(src_file):
                            dst_file = os.path.join(dst_folder, filename)
                            shutil.copy(src_file, dst_file)  # 파일 복사
                            cnt += 1
                            print(f"Copied: {filename}")
print(f"{cnt} file copied")