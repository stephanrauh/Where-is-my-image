import os
import json
from datetime import datetime
from PIL import Image as PILImage
from PIL.ExifTags import TAGS
from sqlalchemy.orm import Session
from models import Image

# Register HEIF opener for HEIC files
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    print("HEIC/HEIF support enabled")
except ImportError:
    print("Warning: pillow-heif not installed, HEIC files won't be supported")

def extract_exif_data(image_path):
    try:
        image = PILImage.open(image_path)
        exif_data = {}
        
        if hasattr(image, '_getexif') and image._getexif() is not None:
            exif = image._getexif()
            for tag_id, value in exif.items():
                tag = TAGS.get(tag_id, tag_id)
                exif_data[tag] = str(value)
        
        return json.dumps(exif_data) if exif_data else None
    except Exception as e:
        print(f"Error extracting EXIF from {image_path}: {e}")
        return None

def scan_images_directory(images_path=None, db: Session = None):
    if images_path is None:
        # Default path depends on whether we're running in Docker or locally
        if os.path.exists("/app/images"):
            images_path = "/app/images"
        else:
            images_path = "../images"
    if not os.path.exists(images_path):
        print(f"Images directory {images_path} does not exist")
        return []
    
    supported_formats = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.heic'}
    new_images = []
    
    for root, dirs, files in os.walk(images_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in supported_formats):
                filepath = os.path.join(root, file)
                relative_path = os.path.relpath(filepath, images_path)
                
                if db:
                    existing = db.query(Image).filter(Image.filepath == relative_path).first()
                    if existing:
                        continue
                
                try:
                    stat = os.stat(filepath)
                    
                    # Try to open and get image dimensions
                    try:
                        with PILImage.open(filepath) as img:
                            width, height = img.size
                            format_name = img.format or 'Unknown'
                    except Exception as img_error:
                        print(f"Cannot open image {filepath}: {img_error}")
                        # For unsupported formats, still record basic file info
                        width, height = None, None
                        format_name = os.path.splitext(file)[1].upper().lstrip('.')
                    
                    exif_data = extract_exif_data(filepath)
                    
                    image_record = {
                        'filename': file,
                        'filepath': relative_path,
                        'file_size': stat.st_size,
                        'width': width,
                        'height': height,
                        'format': format_name,
                        'created_at': datetime.fromtimestamp(stat.st_ctime),
                        'modified_at': datetime.fromtimestamp(stat.st_mtime),
                        'exif_data': exif_data
                    }
                    
                    if db:
                        db_image = Image(**image_record)
                        db.add(db_image)
                        db.commit()
                        db.refresh(db_image)
                    
                    new_images.append(image_record)
                    print(f"Processed: {file} ({format_name}) - {width}x{height}" if width else f"Processed: {file} ({format_name}) - dimensions unavailable")
                    
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")
                    continue
    
    return new_images