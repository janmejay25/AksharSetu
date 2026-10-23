import pandas as pd
from pathlib import Path
import shutil
import unicodedata

# ==========================================
# PROJECT CONFIGURATION
# ==========================================

PROJECT_ROOT = Path(
    r"D:\code material 2.0\akshar-setu-v2"
)

DATASET_DIR = (
    PROJECT_ROOT
    / "data"
    / "lines"
    / "OCR-Bench1000-Gujarati"
)

IMAGE_DIR = DATASET_DIR / "images"

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "tesseract"
)

# CSV splits
splits = {
    "train": DATASET_DIR / "train.csv",
    "validation": DATASET_DIR / "validation.csv",
    "test": DATASET_DIR / "test.csv"
}


# ==========================================
# RESOLVE IMAGE PATH
# ==========================================

def find_image(image_value):

    image_value = str(image_value).strip()

    # Convert Windows path separators
    image_value = image_value.replace("\\", "/")

    original_path = Path(image_value)

    candidates = [

        # Original path interpreted from project root
        PROJECT_ROOT / original_path,

        # Path interpreted from CSV dataset directory
        DATASET_DIR / original_path,

        # Filename directly inside images folder
        IMAGE_DIR / original_path.name

    ]

    for candidate in candidates:

        candidate = candidate.resolve()

        if candidate.exists():
            return candidate

    return None


# ==========================================
# PROCESS DATASET
# ==========================================

for split_name, csv_path in splits.items():

    print(f"\nProcessing: {split_name}")

    if not csv_path.exists():

        print(f"CSV not found: {csv_path}")
        continue

    df = pd.read_csv(csv_path)

    output_split = OUTPUT_DIR / split_name

    output_split.mkdir(
        parents=True,
        exist_ok=True
    )

    success = 0
    missing = 0

    for index, row in df.iterrows():

        image_path = find_image(row["image"])

        if image_path is None:

            print(
                f"Missing image at row {index}: "
                f"{row['image']}"
            )

            missing += 1
            continue

        # Normalize Gujarati text
        text = unicodedata.normalize(
            "NFC",
            str(row["text"])
        )

        # Use split + index as unique filename
        new_name = f"{split_name}_{index:06d}"

        destination_image = (
            output_split
            / f"{new_name}{image_path.suffix}"
        )

        destination_text = (
            output_split
            / f"{new_name}.gt.txt"
        )

        # Copy image
        shutil.copy2(
            image_path,
            destination_image
        )

        # Write Gujarati ground truth
        destination_text.write_text(
            text,
            encoding="utf-8"
        )

        success += 1

    print(f"Successful: {success}")
    print(f"Missing: {missing}")

print("\nConversion completed!")