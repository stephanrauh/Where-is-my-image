from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from models import get_db, create_tables, Image
from image_scanner import scan_images_directory
import uvicorn
import os
import io
from PIL import Image as PILImage

# Register HEIF opener for HEIC files
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass

app = FastAPI()

create_tables()

# Determine paths based on environment (Docker vs local)
if os.path.exists("vanilla"):
    # Running from project root (Docker)
    static_dir = "vanilla"
    html_file = "vanilla/index.html"
else:
    # Running from backend directory (local development)
    static_dir = "../vanilla"
    html_file = "../vanilla/index.html"

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def read_root():
    return FileResponse(html_file)

@app.get("/api/images/count")
async def get_image_count(db: Session = Depends(get_db)):
    count = db.query(Image).count()
    return {"count": count}

@app.post("/api/images/scan")
async def scan_images(db: Session = Depends(get_db)):
    new_images = scan_images_directory(db=db)
    return {"scanned": len(new_images), "new_images": new_images}

@app.get("/api/images")
async def get_images(db: Session = Depends(get_db)):
    images = db.query(Image).all()
    return {"images": [
        {
            "id": img.id,
            "filename": img.filename,
            "filepath": img.filepath,
            "width": img.width,
            "height": img.height,
            "format": img.format,
            "file_size": img.file_size,
            "created_at": img.created_at.isoformat() if img.created_at else None,
            "modified_at": img.modified_at.isoformat() if img.modified_at else None
        }
        for img in images
    ]}

@app.get("/api/images/{image_id}/thumbnail")
async def get_thumbnail(image_id: int, db: Session = Depends(get_db)):
    image = db.query(Image).filter(Image.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    # Determine images path based on environment
    if os.path.exists("/app/images"):
        images_base = "/app/images"
    else:
        images_base = "../images"
    
    image_path = os.path.join(images_base, image.filepath)
    
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image file not found")
    
    try:
        # Create thumbnail
        with PILImage.open(image_path) as img:
            # Convert to RGB if necessary (for PNG with transparency, etc.)
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Create thumbnail (200x200 max, maintaining aspect ratio)
            img.thumbnail((200, 200), PILImage.Resampling.LANCZOS)
            
            # Save to bytes
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='JPEG', quality=85)
            img_bytes.seek(0)
            
            return StreamingResponse(
                io.BytesIO(img_bytes.read()),
                media_type="image/jpeg"
            )
    except Exception as e:
        print(f"Error creating thumbnail for {image_path}: {e}")
        raise HTTPException(status_code=500, detail="Could not create thumbnail")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)