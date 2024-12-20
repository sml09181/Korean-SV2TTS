![header](https://capsule-render.vercel.app/api?type=waving&height=250&color=gradient&text=Korean%20SV2TTS&descAlign=42&descAlignY=40&fontColor=FFFFFF)
<br>
*2024년 2학기 이화여자대학교 도전학기제 개인 프로젝트로 진행하였음.*
<br>
<br>
## Implementation of Korean [SV2TTS](https://arxiv.org/pdf/1806.04558)

>   Based on [CorentinJ/Real-Time-Voice-Cloning](https://github.com/CorentinJ/Real-Time-Voice-Cloning) and [esoyeon/KoreanTTS](https://github.com/esoyeon/KoreanTTS)
<br>





![image](https://github.com/user-attachments/assets/947ed1ed-3d5d-4dc6-997c-38bb43714fad)



- GPU: NVIDIA RTX A6000
- CUDA version: 10.1.243

You can use pretrained weights (Korean) for each component. The weights are located in `/weights` folder.
Highly recommend to create new anaconda environment and run `pip install -r requirements.txt`.
Before running the code, modify the paths to match your project directory.

## STEP1: Encoder
- Input: log mel-spectrogram (from raw speech data w/ arbitrary length)
- Output: speaker embedding w/ fixed dimension
- Action: Learn speaker embedding via speaker verification task

### Dataset

The dataset used is the subset of [AIHub 화자 인식용 음성 데이터](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=537)(AIHub Speaker Recognition Speech Data), with a total size of 98GB.

### Preprocessing
The 'command' type has been excluded from the dataset.
Speakers with fewer than 8 samples have been excluded.
As a result, the dataset contains preprocessed data from a total of 2,535 speakers.

First, the raw dataset has been reorganized into a speaker-specific folder structure. Each folder is named after an individual speaker and contains their respective audio samples.
```
$ python speaker_folder.py
```

Mainly, let's loads and preprocesses audio files (e.g., generating mel spectrograms) while filtering short or corrupted files.
```
$ python encoder_preprocess.py
```

### Training
Then train the encoder.
```
$ python encoder_train.py
```

## STEP2: Synthesizer
- Input: grapheme or phoneme sequence
- Output: log-mel spectrogram
- Action: Text-to-spectrogram for target speaker

### Dataset

The dataset used is the subset of [AIHub 다화자 음성합성 데이터](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=542)(AIHub Multi-Speaker Speech Synthesis Data).
The ZIP files are randomly selected and downloaded, with the total raw data size being 704GB based on 791 speakers.

### Preprocessing

Run code below to organize data into speaker-specific folders and extract Korean transcripts.
The extracted translabels are saved as `.txt` files from the raw label files.
```
$ korean_dataset.py
```

Run code below to normalize Korean translabels.
```
$ korean_normalize.py
```

Preprocessing steps:
- Remove leading and trailing spaces (using strip())
- Remove characters such as ⺀-⺙, ⺛-⻳, 〠-⿕, 々, and 〇
- Normalize using a Korean dictionary
- Normalize English text (convert to uppercase)
- Normalize quotation marks
- Normalize numbers

Final Dataset:
- Data used from 202 out of 791 speakers
- Total of 633,517 samples used

Then, preprocess audioaudio files from datasets, encodes them as mel spectrograms and writes them to the disk. 
Audio files are also saved, to be used by the vocoder for training.
```
$ python synthesizer_preprocess_audio.py
```

Creates embeddings for the synthesizer from the LibriSpeech utterances.

```
$ python synthesizer_preprocess_embeds.py
```

### Train

It was run with the `no_alignment` setting.

```
$ python synthesizer_train.py
```

## STEP3: Vocoder
- Input: log-mel spectrogram
- Output: time-domain waveform
- Action: Convert mel-spectrogram into waveform

### Preprocessing
This script generates ground truth-aligned mel-spectrograms (GTA mels) for vocoder training by synthesizing them with a pre-trained Tacotron model. It processes a dataset, removes padding from the generated mels, and saves the results along with metadata.
```
$ python vocoder_preprocess.py
```

### Train
Trains a WaveRNN vocoder model on mel-spectrograms to generate high-quality audio. 
```
$ python vocoder_train.py
```

## Run demo
Prepare reference audio files before running the code. Here, my voice is used as a reference voice.
```
$ python demo_cli.py
```

## Related Repository
+ [Ear-VoM](https://github.com/sml09181/Ear-VoM)
+ [Deepvoice-Detection-FL](https://github.com/sml09181/Deepvoice-Detection-FL)

## Reference
- [AIHub 화자 인식용 음성 데이터](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=537)(AIHub Speaker Recognition Speech Data)
- [AIHub 다화자 음성합성 데이터](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=542)(AIHub Multi-Speaker Speech Synthesis Data)
- [CorentinJ/Real-Time-Voice-Cloning](https://github.com/CorentinJ/Real-Time-Voice-Cloning)
- [esoyeon/KoreanTTS](https://github.com/esoyeon/KoreanTTS)
