from ember.features import PEFeatureExtractor
import os
import json
import argparse
import datetime

def read_sample(path):
    with open(path, "rb") as sample:
        bytez = sample.read()
    return bytez

def get_raw_features(extractor, bytez):
    return extractor.raw_features(bytez)

def get_features(samples_dir, jsonl_path, label):
    appeared = datetime.datetime.now().strftime("%Y-%m")
    with open(jsonl_path, "w") as jsonl:
        extractor = PEFeatureExtractor()
        for path in os.listdir(samples_dir):
            bytez = read_sample(samples_dir + "/" + path)
            features = get_raw_features(extractor, bytez)
            features.update({"appeared": appeared, "label": label})
            fjson = json.dumps(features)
            jsonl.write(fjson + "\n")

parser = argparse.ArgumentParser()
parser.add_argument('--samples-dir', action="store", required=True, help="path to directory of samples")
parser.add_argument('--output-path', action="store", required=True, help="path to output jsonl file")
parser.add_argument('--label', type=int, action="store", choices=[0,1], required=True, help="0 for benign, 1 for malware")

if __name__ == "__main__":
    args = parser.parse_args()
    get_features(args.samples_dir, args.output_path, args.label)
