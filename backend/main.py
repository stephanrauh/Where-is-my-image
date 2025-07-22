from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from models import get_db, create_tables, Image
from image_scanner import scan_images_directory
import uvicorn
import os

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)