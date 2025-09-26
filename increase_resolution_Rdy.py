import csv
import numpy as np
import os
from PIL import Image, UnidentifiedImageError


class Resolution:
    def __init__(self):
        self.image_rows = []
        self.output_dir = "input_images"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _validate_path(self, file_path):
        """Validate file path to prevent path traversal"""
        if not file_path or '..' in file_path:
            return False
        return os.path.exists(file_path)
    
    def _load_csv_data(self, csv_path):
        """Load and validate CSV data"""
        if not self._validate_path(csv_path):
            raise ValueError("Invalid CSV path")
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                return list(reader)
        except (IOError, csv.Error) as e:
            raise RuntimeError(f"Failed to read CSV: {e}")
    
    def _load_image_safely(self, image_path):
        """Load image with proper error handling"""
        try:
            if not self._validate_path(image_path):
                return None
            
            with Image.open(image_path) as img:
                return np.array(img.convert('RGB'))
        except (UnidentifiedImageError, IOError, OSError):
            return None
    
    def _organize_images_by_grid(self, data):
        """Organize images into a grid structure"""
        if not data:
            return []
        
        # Extract coordinates and find bounds
        x_coords = [int(row['x']) for row in data if row.get('x', '').isdigit()]
        y_coords = [int(row['y']) for row in data if row.get('y', '').isdigit()]
        
        if not x_coords or not y_coords:
            return []
        
        min_x, max_x = min(x_coords), max(x_coords)
        min_y, max_y = min(y_coords), max(y_coords)
        
        # Create grid structure
        grid = {}
        for row in data:
            try:
                x = int(row['x'])
                y = int(row['y'])
                path = row['path_file']
                
                if x not in grid:
                    grid[x] = {}
                grid[x][y] = path
            except (ValueError, KeyError):
                continue
        
        # Convert to ordered list of rows
        image_rows = []
        for x in range(min_x, max_x + 1):
            if x in grid:
                row_images = []
                for y in range(min_y, max_y + 1):
                    if y in grid[x]:
                        img_array = self._load_image_safely(grid[x][y])
                        if img_array is not None:
                            row_images.append(img_array)
                
                if row_images:
                    image_rows.append(row_images)
        
        return image_rows
    
    def imgs_to_image(self, csv_path):
        """Process CSV and organize images into grid structure"""
        try:
            data = self._load_csv_data(csv_path)
            self.image_rows = self._organize_images_by_grid(data)
            
            if not self.image_rows:
                raise RuntimeError("No valid images found to process")
                
        except Exception as e:
            raise RuntimeError(f"Image processing failed: {e}")
    
    def combined_img(self):
        """Combine images into single output image"""
        try:
            if not self.image_rows:
                raise RuntimeError("No image data available. Call imgs_to_image first.")
            
            # Combine each row horizontally
            combined_rows = []
            for row_images in self.image_rows:
                if row_images:
                    try:
                        combined_row = np.hstack(row_images)
                        combined_rows.append(combined_row)
                    except ValueError as e:
                        print(f"Warning: Skipping row due to size mismatch: {e}")
                        continue
            
            if not combined_rows:
                raise RuntimeError("No rows could be combined")
            
            # Combine all rows vertically
            final_image = np.vstack(combined_rows)
            
            # Save the combined image
            output_path = os.path.join(self.output_dir, "image.png")
            pil_image = Image.fromarray(final_image.astype('uint8'))
            pil_image.save(output_path)
            
            return "saved all in one"
            
        except Exception as e:
            raise RuntimeError(f"Image combination failed: {e}")