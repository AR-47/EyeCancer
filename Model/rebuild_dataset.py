#!/usr/bin/env python3
r"""
rebuild_dataset.py
Adapted for your project layout on Windows:
C:\data\raw\odir5k\...
        \uwf_tumor\...

- Samples 2000 non-cancer images
- Augments the ~272 cancer images up to 2000
- Writes processed/ and split/ inside C:\data
- Safe: does not modify raw/
"""

from pathlib import Path
import random
import shutil
import os
from tqdm import tqdm
import cv2
import numpy as np
from PIL import Image
import albumentations as A

# --------- USER EDITABLE (already set for C:\data) -------------
PROJECT_ROOT = Path("C:\\Users\\adith\\Downloads\\EyeCancer\\data")
RAW_DIR = PROJECT_ROOT / "raw"

PROCESSED_DIR = PROJECT_ROOT / "processed"
SPLIT_DIR = PROJECT_ROOT / "split"

UWF_DIR = RAW_DIR / "uwf_tumor"
ODIR_DIR = RAW_DIR / "odir5k"

TARGET_NON_CANCER = 2000
TARGET_CANCER = 2000
TRAIN_RATIO = 0.80
RANDOM_SEED = 42
# ---------------------------------------------------------------

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

def ensure_dirs():
    (PROCESSED_DIR / "cancer").mkdir(parents=True, exist_ok=True)
    (PROCESSED_DIR / "non_cancer").mkdir(parents=True, exist_ok=True)
    (SPLIT_DIR / "train" / "cancer").mkdir(parents=True, exist_ok=True)
    (SPLIT_DIR / "train" / "non_cancer").mkdir(parents=True, exist_ok=True)
    (SPLIT_DIR / "val" / "cancer").mkdir(parents=True, exist_ok=True)
    (SPLIT_DIR / "val" / "non_cancer").mkdir(parents=True, exist_ok=True)

def list_images(folder: Path):
    exts = {".png", ".jpg", ".jpeg", ".tiff", ".bmp"}
    files = []
    if not folder.exists():
        return files
    for p in folder.rglob("*"):
        if p.suffix.lower() in exts and p.is_file():
            files.append(p)
    return files

def gather_cancer_sources():
    cancer_paths = []
    if not UWF_DIR.exists():
        print("Warning: uwf_tumor folder not found at:", UWF_DIR)
        return cancer_paths
    for sub in UWF_DIR.iterdir():
        if sub.is_dir() and sub.name.lower() != "normal":
            cancer_paths.extend(list_images(sub))
    return sorted(cancer_paths)

def gather_non_cancer_sources():
    nonc = []
    normal1 = UWF_DIR / "Normal"
    if normal1.exists():
        nonc.extend(list_images(normal1))

    # read likely ODIR folders
    if (ODIR_DIR / "ODIR-5K").exists():
        base = ODIR_DIR / "ODIR-5K"
        for p in base.rglob("*"):
            if p.is_dir():
                pstr = str(p).lower()
                if ("normal" in pstr) or ("training" in pstr) or ("testing" in pstr) or ("preprocessed" in pstr):
                    nonc.extend(list_images(p))
    else:
        nonc.extend(list_images(ODIR_DIR))

    nonc = sorted(list(set(nonc)))
    return nonc

# Augmentation pipeline — edit to remove medically-inadmissible transforms if needed
augmentations = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.RandomRotate90(p=0.2),
    A.Rotate(limit=12, p=0.5),
    A.OneOf([
        A.RandomBrightnessContrast(brightness_limit=0.18, contrast_limit=0.18, p=0.6),
        A.CLAHE(p=0.3),
    ], p=0.6),
    A.RandomResizedCrop(height=512, width=512, scale=(0.92, 1.0), p=0.35),
    A.GaussNoise(var_limit=(10.0, 40.0), p=0.25),
    A.ShiftScaleRotate(shift_limit=0.04, scale_limit=0.04, rotate_limit=8, p=0.35),
])

def load_image_cv2(path):
    img = cv2.imread(str(path))
    if img is None:
        raise RuntimeError(f"Failed to read image: {path}")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def save_image_pil(arr, path):
    img = Image.fromarray(arr.astype(np.uint8))
    img.save(path)

def copy_all_cancer_to_processed(cancer_paths):
    for src in tqdm(cancer_paths, desc="Copying cancer -> processed/cancer"):
        dst = PROCESSED_DIR / "cancer" / (src.stem + src.suffix)
        if dst.exists():
            dst = PROCESSED_DIR / "cancer" / (f"{src.parent.name}_{src.stem}{src.suffix}")
        shutil.copy2(src, dst)

def copy_sample_non_cancer(all_non_cancer_paths):
    n_available = len(all_non_cancer_paths)
    if n_available < TARGET_NON_CANCER:
        raise ValueError(f"Not enough non-cancer images found ({n_available}) to sample {TARGET_NON_CANCER}.")
    sampled = random.sample(all_non_cancer_paths, TARGET_NON_CANCER)
    for src in tqdm(sampled, desc="Copying non-cancer -> processed/non_cancer"):
        dst = PROCESSED_DIR / "non_cancer" / (src.stem + src.suffix)
        if dst.exists():
            dst = PROCESSED_DIR / "non_cancer" / (f"{src.parent.name}_{src.stem}{src.suffix}")
        shutil.copy2(src, dst)
    return sampled

def augment_cancer_to_target():
    proc_cancer_files = list_images(PROCESSED_DIR / "cancer")
    current = len(proc_cancer_files)
    if current == 0:
        raise ValueError("No cancer images found in processed/cancer — aborting augmentation.")
    idx = 0
    pbar = tqdm(total=max(0, TARGET_CANCER - current), desc="Augmenting cancer images")
    while current < TARGET_CANCER:
        src = proc_cancer_files[idx % len(proc_cancer_files)]
        try:
            img = load_image_cv2(src)
        except RuntimeError:
            idx += 1
            continue
        transformed = augmentations(image=img)
        aug_img = transformed["image"]
        out_name = f"{src.stem}_aug_{current+1}{src.suffix}"
        out_path = PROCESSED_DIR / "cancer" / out_name
        save_image_pil(aug_img, out_path)
        current += 1
        idx += 1
        pbar.update(1)
    pbar.close()

def build_splits():
    cancer_files = list_images(PROCESSED_DIR / "cancer")
    nonc_files = list_images(PROCESSED_DIR / "non_cancer")
    random.shuffle(cancer_files)
    random.shuffle(nonc_files)

    def split_and_copy(file_list, label):
        n = len(file_list)
        n_train = int(n * TRAIN_RATIO)
        train_files = file_list[:n_train]
        val_files = file_list[n_train:]
        dest_train = SPLIT_DIR / "train" / label
        dest_val = SPLIT_DIR / "val" / label
        for src in tqdm(train_files, desc=f"Copy train/{label}"):
            dst = dest_train / src.name
            shutil.copy2(src, dst)
        for src in tqdm(val_files, desc=f"Copy val/{label}"):
            dst = dest_val / src.name
            shutil.copy2(src, dst)
        return len(train_files), len(val_files)

    t_c, v_c = split_and_copy(cancer_files, "cancer")
    t_n, v_n = split_and_copy(nonc_files, "non_cancer")
    print(f"Split completed. cancer train/val: {t_c}/{v_c}, non_cancer train/val: {t_n}/{v_n}")

def main():
    ensure_dirs()
    print("Gathering source image lists...")
    cancer_srcs = gather_cancer_sources()
    nonc_srcs = gather_non_cancer_sources()
    print(f"Found {len(cancer_srcs)} cancer-source images and {len(nonc_srcs)} non-cancer-source images.")

    copy_all_cancer_to_processed(cancer_srcs)
    copy_sample_non_cancer(nonc_srcs)
    print(f"Currently processed cancer images: {len(list_images(PROCESSED_DIR / 'cancer'))}")
    print(f"Augmenting cancer images to reach {TARGET_CANCER} total...")
    augment_cancer_to_target()

    final_c = len(list_images(PROCESSED_DIR / "cancer"))
    final_n = len(list_images(PROCESSED_DIR / "non_cancer"))
    print(f"Final processed counts -> cancer: {final_c}, non_cancer: {final_n}")

    print("Creating train/val splits in 'split/' (80% train / 20% val)...")
    build_splits()
    print("Done. Processed data is in:", PROCESSED_DIR)
    print("Train/val split in:", SPLIT_DIR)

if __name__ == "__main__":
    main()
