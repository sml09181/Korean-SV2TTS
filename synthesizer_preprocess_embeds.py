from synthesizer.preprocess import create_embeddings
from utils.argutils import print_args
from pathlib import Path
import argparse
import os


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Creates embeddings for the synthesizer from the LibriSpeech utterances.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--synthesizer_root", type=Path, default="/GENERATION/SV2TTS/synthesizer/preprocessed", help=\
        "Path to the synthesizer training data that contains the audios and the train.txt file. "
        "If you let everything as default, it should be <datasets_root>/SV2TTS/synthesizer/.")
    parser.add_argument("-e", "--encoder_model_fpath", type=Path, default="/GENERATION/result/saved_models/su/encoder/encoder_1565000.pt",
                        help=\
        "Path your trained encoder model.")
    parser.add_argument("-n", "--n_processes", type=int, default=5, help= \
        "Number of parallel processes. An encoder is created for each, so you may need to lower "
        "this value on GPUs with low memory. Set it to 1 if CUDA is unhappy.")
    args = parser.parse_args()

    # Preprocess the dataset
    os.environ["CUDA_VISIBLE_DEVICES"] = "4"
    print_args(args, parser)
    create_embeddings(**vars(args))
