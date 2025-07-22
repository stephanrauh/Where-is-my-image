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

app.mount("/static", StaticFiles(directory="../vanilla"), name="static")

@app.get("/")
async def read_root():
    return FileResponse("../vanilla/index.html")

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