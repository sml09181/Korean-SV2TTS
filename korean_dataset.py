# For organize AIHub TTS dataset(https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=542)
import os
import json
import shutil
from tqdm import tqdm

def organize_speaker_folders(src_root, dst_root):
    for zip_folder in tqdm(os.listdir(src_root)[44:]): # per zip file # ex. TS2
        zip_folder_path = os.path.join(src_root, zip_folder)
        if not os.path.isdir(zip_folder_path) or not zip_folder_path.endswith("_2"): continue
        for root, dirs, files in os.walk(zip_folder_path, topdown=False):
            if len(dirs) > 1 and len(files) == 0: 
                src_folder = os.path.join(zip_folder_path, root) # ex. 0313_G1A2E7_PTH
                for speaker_folder in os.listdir(src_folder):
                    src_path = os.path.join(src_folder, speaker_folder)
                    dst_path = os.path.join(dst_root, speaker_folder)
                    shutil.copytree(src_path, dst_path)
    print("[INFO] Organized:", dst_root)

def extract_translabel(src_data_root, src_label_root):
    for speaker in tqdm(os.listdir(src_label_root)):
        speaker_folder = os.path.join(src_label_root, speaker)
        for json_file in os.listdir(speaker_folder):
            filename = os.path.splitext(json_file)[0]
            json_path = os.path.join(speaker_folder, json_file)
            wav_path = os.path.join(src_data_root, speaker, f"{filename}.wav")
            #print(wav_path)
            if os.path.isfile(wav_path):
                # open label json file
                # ex. /6030_G1A1E7_KJW/6030_G1A1E7_KJW_000001.json
                # {"기본정보": {"Language": "KOR", "Version": "N/A", "ApplicationCategory": "N/A", "NumberOfSpeaker": "6030", "NumberOfUtterance": "N/A", "DataCategory": "ReadSpeech", "RecordingDate": "N/A", "FillingDate": "N/A", "RevisionHistory": "N/A", "Distributor": "MediaZen"}, "음성정보": {"SamplingRate": "48000", "NumberOfBit": "16", "ByteOrder": "N/A", "EncodingLaw": "SignedIntegerPCM", "NumberOfChannel": "1", "SignalToNoiseRatio": "N/A"}, "전사정보": {"OrgLabelText": "몇 리터로 드릴까요?", "TransLabelText": "몇 리터로 드릴까요?", "RefinedLabelText": "", "ModifyLabelText": "0", "TextCategory": "AI답변"}, "화자정보": {"SpeakerName": "KJW", "Gender": "Male", "Age": "10~19", "Region": "Seoul", "Dialect": "NotProvidied", "Emotion": "Neutrality", "Sensitivity": "Neutrality"}, "환경정보": {"RecordingEnviron": "RecordingBooth", "NoiseEnviron": "Soundproof", "RecordingDevice": "RecordingMIC"}, "파일정보": {"FileCategory": "Audio", "FileName": "6030_G1A1E7_KJW_000001.wav", "DirectoryPath": "/6030_G1A1E7_KJW", "HeaderSize": "N/A", "FileLength": 1.88, "FileFormat": "WAV", "NumberOfRepeat": "1", "TimeInterval": "N/A", "Distance": "N/A"}, "기타정보": {"QualityStatus": "Good", "SpeechStart": 0.3, "SpeechEnd": 1.58}}
                with open(json_path, 'r') as f:
                    data = json.load(f)
                    text = data['전사정보']['TransLabelText']
                
                # write raw text(TransLabelText)
                txt_folder = os.path.join(os.path.dirname(src_data_root), "translabel")
                os.makedirs(txt_folder, exist_ok=True)
                txt_path = os.path.join(txt_folder, f"{filename}.txt")
                #print(txt_path)
                with open(txt_path, 'w') as f:
                    f.write(text)
    print("[INFO] TransLabelText extracted")

if __name__ == '__main__':
    data_root = "/GENERATION/SV2TTS/synthesizer/data"
    label_root = "/GENERATION/SV2TTS/synthesizer/label"

    organize_speaker_folders(os.path.join(src_root, "train", "data"), os.path.join(dst_root, "data"))
    organize_speaker_folders(os.path.join(src_root, "train", "label"), os.path.join(dst_root, "label"))
    organize_speaker_folders(os.path.join(src_root, "valid", "data"), os.path.join(dst_root, "data"))
    organize_speaker_folders(os.path.join(src_root, "valid", "label"), os.path.join(dst_root, "label"))

    extract_translabel(data_root, label_root)
