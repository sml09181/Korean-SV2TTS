import os
import pandas as pd
import yaml
import numpy as np
from pathlib import Path
import parmap
import pandas as pd
import multiprocessing

from text.korean import normalize

# normalize korean translabel
def extract_noramlized_label(src_txt_path):
    src_txt_path = Path(src_txt_path)
    with open(src_txt_path, 'r') as f:
        text = f.read()

    dst_txt_folder = os.path.join(src_txt_path.parent.parent, "normalized")
    os.makedirs(dst_txt_folder, exist_ok=True)
    dst_txt_path = os.path.join(dst_txt_folder, src_txt_path.name)
    with open(dst_txt_path, 'w') as f:
        f.write(normalize(text))

if __name__ == "__main__":
    src_root = "/GENERATION/SV2TTS/synthesizer/translabel"
    src_path_list = [os.path.join(src_root, file) for file in os.listdir(src_root)]
    n_proc = multiprocessing.cpu_count()

    with multiprocessing.Pool(n_proc) as pool:
        parmap.map(
            extract_noramlized_label, 
            src_path_list, 
            pm_pbar=True, pm_processes=n_proc)

    def test_normalize(text):
        print(text)
        print(normalize(text))
        print("="*30)

    test_normalize("JTBC는 JTBCs를 DY는 A가 Absolute")
    test_normalize("오늘(13일) 3,600마리 강아지가")
    test_normalize("60.3%")
    test_normalize('"저돌"(猪突) 입니다.')
    test_normalize('비대위원장이 지난 1월 이런 말을 했습니다. “난 그냥 산돼지처럼 돌파하는 스타일이다”')
    test_normalize("지금은 -12.35%였고 종류는 5가지와 19가지, 그리고 55가지였다")
    test_normalize("JTBC는 TH와 K 양이 2017년 9월 12일 오후 12시에 24살이 된다")