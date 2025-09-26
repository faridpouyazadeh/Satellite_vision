# Satellite Vision 🛰️

A comprehensive Python application for satellite image analysis using AI-powered object detection and instance segmentation.

## 🌟 Features

- **Satellite Image Download**: Automatically download satellite images from specified coordinates
- **Image Processing**: Combine multiple satellite tiles into high-resolution images
- **AI Object Detection**: Detect objects in satellite images using YOLO models
- **Instance Segmentation**: Perform pixel-level segmentation of objects
- **Custom Classes**: Define and train custom object classes
- **Video Tracking**: Track objects in video sequences
- **Batch Processing**: Process multiple images efficiently

## 📋 Requirements

- Python 3.8 or higher
- Internet connection for downloading satellite images and models
- At least 4GB RAM recommended
- GPU support optional but recommended for faster AI processing

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone or download the project
cd satellite_vison

# Install dependencies
pip install -r requirements.txt

# Run setup script (downloads models and creates directories)
python setup.py
```

### 2. Basic Usage

```bash
# For basic satellite image processing
python main_fixed.py

# For full AI analysis features
python main_complete_fixed.py
```

### 3. Example Usage

1. **Download Satellite Images**:
   - Enter the object/location you want to find
   - Provide coordinates in DMS format (Degrees, Minutes, Seconds)
   - The system will download and process satellite images

2. **AI Analysis** (main_complete_fixed.py):
   - Choose from object detection or instance segmentation
   - Train custom models or use pre-trained ones
   - Perform predictions on satellite images

## 📁 Project Structure

```
satellite_vison/
├── download_pics_fixed.py      # Satellite image downloader
├── increase_resolution_fixed.py # Image processing and combination
├── Model_fixed.py              # Object detection model
├── Model_InsSeg_fixed.py       # Instance segmentation model
├── main_fixed.py               # Simple entry point
├── main_complete_fixed.py      # Full-featured application
├── setup.py                    # Environment setup script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── download/                   # Downloaded images storage
├── input_images/               # Processed images
└── structure_folder/           # Models and outputs
    ├── models_folder/          # Trained models
    ├── CSV_folder/             # Analysis results
    ├── video_tracked/          # Video tracking outputs
    └── annonations/            # Annotation files
```

## 🔧 Configuration

### Coordinate Input Format

The application uses DMS (Degrees, Minutes, Seconds) format:
- **Longitude**: -180° to +180° (East/West)
- **Latitude**: -90° to +90° (North/South)

Example:
```
Longitude: 40° 45' 30.5" N
Latitude: 73° 59' 12.8" W
```

### Supported Operations

1. **Train**: Train models on custom datasets
2. **Predict**: Analyze satellite images
3. **Validation**: Validate model performance
4. **Track-on-Video**: Track objects in video sequences
5. **Define-Custom-Classes**: Create custom object detection classes

## 🛡️ Security Features

- **URL Validation**: Prevents SSRF attacks
- **Path Sanitization**: Prevents path traversal vulnerabilities
- **Input Validation**: Validates all user inputs
- **Safe File Handling**: Secure file operations
- **Error Handling**: Comprehensive error management

## 📊 Model Information

### Object Detection (Model_fixed.py)
- **Base Model**: YOLOv8n (Nano)
- **Input Size**: 640x640 pixels
- **Features**: Real-time object detection
- **Custom Classes**: Supported

### Instance Segmentation (Model_InsSeg_fixed.py)
- **Base Model**: YOLOv8n-seg
- **Input Size**: 640x640 pixels
- **Features**: Pixel-level segmentation
- **Output**: Masks and bounding boxes

## 🔍 Usage Examples

### Basic Satellite Image Download
```python
from download_pics_fixed import Download

downloader = Download()
csv_path = downloader.req_and_get(url, "buildings")
```

### Image Processing
```python
from increase_resolution_fixed import Resolution

processor = Resolution()
processor.imgs_to_image("path/to/data.csv")
result = processor.combined_img()
```

### Object Detection
```python
from Model_fixed import Model

model = Model()
result = model.predict("input_images/image.png")
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**:
   ```bash
   pip install -r requirements.txt
   python setup.py
   ```

2. **Model Download Failures**:
   - Check internet connection
   - Run `python setup.py` again
   - Manually download models from GitHub releases

3. **Memory Issues**:
   - Reduce image resolution
   - Process images in smaller batches
   - Close other applications

4. **Coordinate Errors**:
   - Verify coordinate format (DMS)
   - Check longitude/latitude ranges
   - Ensure positive/negative indicators are correct

### Error Messages

- **"Invalid or unsafe URL"**: Check coordinate input and internet connection
- **"Failed to download satellite data"**: Verify coordinates and try again
- **"No valid images found"**: Check if images were downloaded successfully

## 📈 Performance Tips

1. **GPU Acceleration**: Install CUDA for faster AI processing
2. **Batch Processing**: Process multiple images together
3. **Model Optimization**: Use appropriate model sizes for your hardware
4. **Memory Management**: Monitor RAM usage during processing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is provided as-is for educational and research purposes.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review error messages carefully
3. Ensure all dependencies are installed
4. Verify input formats and file paths

## 🔄 Version History

- **v1.0**: Initial release with basic functionality
- **v1.1**: Added security improvements and error handling
- **v1.2**: Enhanced AI model support and custom classes
- **v1.3**: Added setup script and improved documentation

---

**Note**: This application requires internet access to download satellite images and may be subject to rate limits from image providers. Please use responsibly and in accordance with the terms of service of satellite image providers.