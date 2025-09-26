import requests
from bs4 import BeautifulSoup
import re
import csv
import os
from urllib.parse import urlparse
from PIL import Image, UnidentifiedImageError


class Download:
    def __init__(self):
        self.allowed_domains = ['picsfromspace.com', 'mt.google.com']
        self.base_dir = 'download'
    
    def _validate_url(self, url):
        """Validate URL to prevent SSRF attacks"""
        try:
            parsed = urlparse(url)
            if not parsed.scheme in ['http', 'https']:
                return False
            if not any(domain in parsed.netloc for domain in self.allowed_domains):
                return False
            return True
        except Exception:
            return False
    
    def _sanitize_filename(self, filename):
        """Sanitize filename to prevent path traversal"""
        # Remove path separators and dangerous characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = filename.replace('..', '_')
        return filename[:50]  # Limit length
    
    def _create_safe_path(self, subject, filename):
        """Create safe file path within allowed directory"""
        safe_subject = self._sanitize_filename(subject)
        safe_filename = self._sanitize_filename(filename)
        
        # Ensure directory exists
        dir_path = os.path.join(self.base_dir, safe_subject, 'pics_satellite')
        os.makedirs(dir_path, exist_ok=True)
        
        return os.path.join(dir_path, safe_filename)
    
    def _download_image(self, img_url, file_path):
        """Safely download and process image"""
        try:
            if not self._validate_url(img_url):
                return False
                
            response = requests.get(img_url, timeout=10, stream=True)
            response.raise_for_status()
            
            # Write image data
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Process image
            return self._resize_image(file_path)
            
        except (requests.RequestException, IOError) as e:
            print(f"Download failed: {e}")
            return False
    
    def _resize_image(self, file_path):
        """Resize image with error handling"""
        try:
            with Image.open(file_path) as image:
                target_size = 640
                width, height = image.size
                
                if width > height:
                    new_width = target_size
                    new_height = int((target_size / width) * height)
                else:
                    new_height = target_size
                    new_width = int((target_size / height) * width)
                
                resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                resized_image.save(file_path)
                return True
                
        except (UnidentifiedImageError, IOError, OSError) as e:
            print(f"Image processing failed: {e}")
            if os.path.exists(file_path):
                os.remove(file_path)
            return False
    
    def _extract_coordinates(self, url):
        """Extract coordinates from URL"""
        pattern = r'\d+'
        coordinates = re.findall(pattern, url)
        return coordinates[0] if len(coordinates) > 0 else "0", coordinates[1] if len(coordinates) > 1 else "0"
    
    def _save_to_csv(self, pictures_info, subject):
        """Save picture information to CSV"""
        try:
            safe_subject = self._sanitize_filename(subject)
            csv_dir = os.path.join(self.base_dir, safe_subject)
            os.makedirs(csv_dir, exist_ok=True)
            
            csv_path = os.path.join(csv_dir, f"information_of_{safe_subject}.csv")
            
            fields = ["id", "subject", "path_file", "url_pic", "x", "y"]
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fields)
                writer.writeheader()
                writer.writerows(pictures_info)
            
            return csv_path
            
        except IOError as e:
            print(f"CSV save failed: {e}")
            return ""
    
    def req_and_get(self, create_url, item):
        """Main method to download satellite images"""
        if not create_url or not self._validate_url(create_url):
            raise ValueError("Invalid or unsafe URL provided")
        
        safe_item = self._sanitize_filename(item)
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        
        try:
            # Get webpage content
            response = requests.get(create_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            img_tags = soup.find_all('img')
            
            pictures_info = []
            downloaded_count = 0
            
            for img_tag in img_tags:
                try:
                    img_src = img_tag.get('src', '')
                    if not img_src.startswith("https://mt.google.com/vt/lyrs=y"):
                        continue
                    
                    # Create safe filename
                    filename = f"{safe_item}-{downloaded_count}.png"
                    file_path = self._create_safe_path(safe_item, filename)
                    
                    # Download and process image
                    if self._download_image(img_src, file_path):
                        x_coord, y_coord = self._extract_coordinates(img_src)
                        
                        pic_info = {
                            "id": str(downloaded_count),
                            "subject": safe_item,
                            "path_file": file_path,
                            "url_pic": img_src,
                            "x": x_coord,
                            "y": y_coord
                        }
                        pictures_info.append(pic_info)
                        downloaded_count += 1
                        
                except Exception as e:
                    print(f"Error processing image {downloaded_count}: {e}")
                    continue
            
            if not pictures_info:
                return ""
            
            # Save to CSV
            return self._save_to_csv(pictures_info, safe_item)
            
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return ""
        except Exception as e:
            print(f"Unexpected error: {e}")
            return ""