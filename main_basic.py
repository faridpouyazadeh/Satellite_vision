#!/usr/bin/env python3
import os
import sys
import time
from pathlib import Path

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from download_pics_Rdy import Download
    from increase_resolution_Rdy import Resolution
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all required files are in the same directory")
    sys.exit(1)


def display_text(text_content):
    for char in text_content:
        print(char, end='', flush=True)
        time.sleep(0.02)
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
            
            # Validate ranges
            if coord_type.lower() == "longitude" and not (-180 <= degree <= 180):
                raise ValueError("Longitude degree must be between -180 and 180")
            elif coord_type.lower() == "latitude" and not (-90 <= degree <= 90):
                raise ValueError("Latitude degree must be between -90 and 90")
            
            if not (0 <= minute <= 59):
                raise ValueError("Minutes must be between 0 and 59")
            if not (0 <= seconds < 60):
                raise ValueError("Seconds must be between 0 and 59.999")
            
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
        print("Downloading satellite images...")
        download_step = Download()
        csv_path = download_step.req_and_get(url, item)
        
        if not csv_path:
            raise RuntimeError("Failed to download satellite data")
        
        print("Processing and combining images...")
        resolution_step = Resolution()
        resolution_step.imgs_to_image(csv_path)
        result = resolution_step.combined_img()
        
        if result != "saved all in one":
            raise RuntimeError("Failed to combine images")
            
        return "input_images/image.png"
        
    except Exception as e:
        raise RuntimeError(f"Satellite data processing failed: {e}")


def main():
    try:
        print("=" * 50)
        print("Welcome to Satellite Vision!")
        print("=" * 50)
        
        item = input("What object/location do you want to find? ").lower().strip()
        if not item:
            print("Error: Please provide a valid search term")
            return False
        
        # Get coordinates
        display_text("Enter coordinates in DMS (Degrees, Minutes, Seconds) format:")
        display_text("Longitude range: [-180 : +180], Latitude range: [-90 : +90]")
        
        long_sign, long_deg, long_min, long_sec = get_coordinate_input("Longitude")
        lati_sign, lati_deg, lati_min, lati_sec = get_coordinate_input("Latitude")
        
        # Convert to decimal degrees
        longitude = convert_dms_to_decimal(long_sign, long_deg, long_min, long_sec)
        latitude = convert_dms_to_decimal(lati_sign, lati_deg, lati_min, lati_sec)
        
        print(f"Coordinates: {latitude}, {longitude}")
        
        # Calculate bounding box and create URL
        point1_x, point1_y, point2_x, point2_y = calculate_bounding_box(longitude, latitude)
        url = create_satellite_url(long_sign, point1_x, lati_sign, point1_y, point2_x, point2_y)
        
        # Process satellite data
        print("Processing satellite data...")
        img_path = process_satellite_data(url, item)
        
        print(f"Success! Satellite image saved to: {img_path}")
        print("You can now use the advanced features in main_full.py for AI analysis")
        
        return True
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return False
    except Exception as e:
        print(f"Application error: {e}")
        return False


if __name__ == "__main__":
    success = main()
    if success:
        print("\nProcess completed successfully!")
    else:
        print("\nProcess failed. Please check the error messages above.")