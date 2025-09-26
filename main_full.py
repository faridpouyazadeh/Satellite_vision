import os
import sys
import requests
from PIL import Image, ImageFilter
from bs4 import BeautifulSoup
import re
import numpy as np
import time
from download_pics_Rdy import Download
from increase_resolution_Rdy import Resolution
from Model_Rdy import Model
from Model_InsSeg_Rdy import Model_InsSeg


def display_text(text_content):
    """Display text character by character with delay"""
    for char in text_content:
        print(char, end='', flush=True)
        time.sleep(0.05)
    print()


def get_coordinate_input(coord_type):
    """Get coordinate input with proper validation"""
    print(f"Enter {coord_type}:")
    
    while True:
        try:
            sign_input = input("Write Positive OR Negative:(p/n) ").lower().strip()
            
            if not (sign_input.startswith("p") or sign_input.startswith("n")):
                raise ValueError("Invalid input. Enter 'p' for positive or 'n' for negative")
            
            degree = int(input("Degree: "))
            minute = int(input("Minute: "))
            seconds = float(input("Seconds: "))
            
            sign = "-" if sign_input.startswith("n") else ""
            return sign, degree, minute, seconds
            
        except ValueError as e:
            print(f"Error: {e}. Please try again.")


def convert_dms_to_decimal(sign, degree, minute, seconds):
    """Convert DMS coordinates to decimal degrees"""
    decimal = degree + (minute / 60) + (seconds / 3600)
    return float(f"{sign}{decimal}")


def calculate_bounding_box(longitude, latitude):
    """Calculate bounding box for satellite image"""
    offset_x = 0.000396296382
    offset_y = 0.000357551447
    
    point1_x = longitude - offset_x
    point1_y = latitude - offset_y
    point2_x = longitude + offset_x
    point2_y = latitude + offset_y
    
    return point1_x, point1_y, point2_x, point2_y


def create_satellite_url(long_sign, point1_x, lati_sign, point1_y, point2_x, point2_y):
    """Create URL for satellite image request"""
    return f"https://picsfromspace.com/satellite?pos={long_sign}{point1_x}%2C{lati_sign}{point1_y}%2C{long_sign}{point2_x}%2C{lati_sign}{point2_y}&basemap=Google%2520Hybrid"


def process_satellite_data(url, item):
    """Download and process satellite images"""
    try:
        download_step = Download()
        csv_path = download_step.req_and_get(url, item)
        
        if not csv_path:
            raise RuntimeError("Failed to download satellite data")
        
        resolution_step = Resolution()
        resolution_step.imgs_to_image(csv_path)
        result = resolution_step.combined_img()
        
        if result != "saved all in one":
            raise RuntimeError("Failed to combine images")
            
        return "input_images/image.png"
        
    except Exception as e:
        raise RuntimeError(f"Satellite data processing failed: {e}")


def parse_custom_classes(input_text):
    """Parse custom classes from user input"""
    for delimiter in [',', ' ', ', ', ' ,']:
        if delimiter in input_text:
            return [cls.strip() for cls in input_text.split(delimiter) if cls.strip()]
    return [input_text.strip()]


def handle_object_detection(order, img_path, model):
    """Handle object detection operations"""
    try:
        if order == "train":
            yaml_file = input("Input path of yaml_file for <Train>: ").strip()
            result = model.train(yaml_file)
            
        elif order == "predict":
            print("Processing satellite image for prediction...")
            result = model.predict(img_path)
            
        elif order == "validation":
            yaml_file = input("Input path of yaml_file for <Validation>: ").strip()
            result = model.validation(yaml_file)
            
        elif order == "track-on-video":
            vid_path = input("Input path of Video for <Tracking>: ").strip()
            result = model.track(vid_path)
            
        elif order == "define-custom-classes":
            classes_input = input("Write classes (e.g., person car or person,car): ").lower().strip()
            class_list = parse_custom_classes(classes_input)
            
            result = model.define_custom_classes(img_path, class_list)
            if result == "Done":
                save_choice = input("Save this model? (y/n): ").strip().lower()
                if save_choice.startswith('y'):
                    save_result = model.save_define_model(class_list)
                    if save_result != "Done":
                        raise RuntimeError("Model saving failed")
        
        if result != "Done":
            raise RuntimeError(f"Operation failed: {order}")
            
        print("Operation completed successfully")
        
    except Exception as e:
        print(f"Object detection operation failed: {e}")


def handle_instance_segmentation(order, img_path, model):
    """Handle instance segmentation operations"""
    try:
        if order == "train":
            yaml_file = input("Input path of yaml_file for <Train>: ").strip()
            result = model.train(yaml_file)
            
        elif order == "predict":
            result = model.predict(img_path)
            
        elif order == "define-custom-classes":
            classes_input = input("Write classes (e.g., person car or person,car): ").lower().strip()
            class_list = parse_custom_classes(classes_input)
            result = model.define_custom_classes(class_list)
        
        if result != "Done":
            raise RuntimeError(f"Operation failed: {order}")
            
        print("Operation completed successfully")
        
    except Exception as e:
        print(f"Instance segmentation operation failed: {e}")


def run_model_operations(img_path):
    """Handle model operations menu"""
    work_options = ["train", "predict", "validation", "track-on-video", "define-custom-classes", "exit"]
    task_options = ["objects-detection", "instance-segmentation", "exit"]
    
    # Initialize models
    od_model = Model()
    seg_model = Model_InsSeg()
    
    while True:
        try:
            print("\nChoose operation:")
            print("[ Train | Predict | Validation | Track-on-Video | Define-Custom-Classes | Exit ]")
            order = input("--> ").lower().strip()
            
            if order not in work_options:
                print("Invalid option. Please try again.")
                continue
                
            if order == "exit":
                return True
                
            print("\nChoose task:")
            print("[ Objects-Detection | Instance-Segmentation | Exit ]")
            task = input("--> ").lower().strip()
            
            if task not in task_options:
                print("Invalid task. Please try again.")
                continue
                
            if task == "exit":
                return True
                
            if task == "objects-detection":
                handle_object_detection(order, img_path, od_model)
            elif task == "instance-segmentation":
                handle_instance_segmentation(order, img_path, seg_model)
                
        except KeyboardInterrupt:
            print("\nOperation cancelled by user")
            return True
        except Exception as e:
            print(f"Error: {e}")
            continue


def main():
    """Main function - satellite vision application"""
    try:
        print("Welcome to Satellite Vision!")
        item = input("What object do you want to find? ").lower().strip()
        
        # Get coordinates
        display_text("Enter coordinates in DMS format:")
        display_text("Longitude range: [-180 : +180], Latitude range: [-90 : +90]")
        
        long_sign, long_deg, long_min, long_sec = get_coordinate_input("Longitude")
        lati_sign, lati_deg, lati_min, lati_sec = get_coordinate_input("Latitude")
        
        # Convert to decimal degrees
        longitude = convert_dms_to_decimal(long_sign, long_deg, long_min, long_sec)
        latitude = convert_dms_to_decimal(lati_sign, lati_deg, lati_min, lati_sec)
        
        # Calculate bounding box and create URL
        point1_x, point1_y, point2_x, point2_y = calculate_bounding_box(longitude, latitude)
        url = create_satellite_url(long_sign, point1_x, lati_sign, point1_y, point2_x, point2_y)
        
        # Process satellite data
        print("Processing satellite data...")
        img_path = process_satellite_data(url, item)
        
        # Run model operations
        print("Image ready for analysis!")
        run_model_operations(img_path)
        
        print("Thank you for using Satellite Vision!")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"Application error: {e}")
        return False
    
    return True


if __name__ == "__main__":
    main()