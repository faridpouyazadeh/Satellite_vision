#!/usr/bin/env python3
import os
import sys
import urllib.request
from pathlib import Path


def create_directories():
    """Create necessary directories"""
    directories = [
        "structure_folder",
        "structure_folder/models_folder",
        "structure_folder/CSV_folder", 
        "structure_folder/video_tracked",
        "structure_folder/annonations",
        "download",
        "input_images"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")


def download_models():
    models = {
        "structure_folder/Model.pt": "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8x-worldv2.pt",
        "structure_folder/Model_InsSeg.pt": "https://github.com/ultralytics/assets/releases/download/v8.3.0/yoloe-v8l-seg.pt"
    }
    
    for model_path, url in models.items():
        if not os.path.exists(model_path):
            try:
                print(f"Downloading {model_path}...")
                urllib.request.urlretrieve(url, model_path)
                print(f"Successfully downloaded {model_path}")
            except Exception as e:
                print(f"Failed to download {model_path}: {e}")
                print("You can manually download the models from:")
                print(f"  {url}")
        else:
            print(f"Model already exists: {model_path}")


def install_requirements():
    try:
        import subprocess
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Requirements installed successfully!")
    except Exception as e:
        print(f"Failed to install requirements: {e}")
        print("Please manually run: pip install -r requirements.txt")


def main():
    print("=" * 50)
    print("Satellite Vision Setup")
    print("=" * 50)
    
    print("\n1. Creating directories...")
    create_directories()
    
    print("\n2. Installing requirements...")
    install_requirements()
    
    print("\n3. Downloading model files...")
    download_models()
    
    print("\n" + "=" * 50)
    print("Setup completed!")
    print("You can now run:")
    print("  python main_basic.py          - For basic satellite image processing")
    print("  python main_full.py           - For full AI analysis features")
    print("=" * 50)


if __name__ == "__main__":
    main()