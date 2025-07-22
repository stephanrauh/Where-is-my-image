# Photo Browser Application

A simple photo browsing application with tagging, search, and metadata management capabilities.

## Prerequisites

Before running this application, make sure you have the following installed:

- **Docker**: Required for running PostgreSQL database and containerized deployment
  - Download from: https://www.docker.com/get-started
  - Verify installation: `docker --version`
- **Docker Compose**: Usually included with Docker Desktop
  - Verify installation: `docker compose --version`
- **Git**: For cloning the repository
  - Download from: https://git-scm.com/downloads
  - Verify installation: `git --version`

### For Local Development (Optional)
- **Python 3.11+**: Required only if using local development mode
  - Download from: https://www.python.org/downloads/
  - Verify installation: `python --version` or `python3 --version`

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/stephanrauh/Where-is-my-image.git
cd Where-is-my-image
```

### 2. Add Your Images

Place your photos in the `images/` folder:
```bash
# Copy your photos to the images directory
cp /path/to/your/photos/* images/
```

### 3. Run the Application

**Quick Start (Recommended):**
- **Linux/macOS**: `./start.sh`
- **Windows**: `start.bat`

**For Local Development:**
- **Linux/macOS**: `./start-local.sh` 
- **Windows**: `start-local.bat`

Then open http://localhost:8000 in your browser!

## Architecture

- **Frontend**: Vanilla JavaScript with Tailwind CSS (`vanilla/` folder)
- **Backend**: FastAPI Python server (`backend/` folder)
- **Database**: PostgreSQL running in Docker container. The database is stored in the folder `database` in the repository.
- **Images**: Stored in `images/` folder

## Features

- Browse photos with metadata display
- Scan image directories to discover new photos
- Store image metadata (dimensions, file size, format, EXIF data)
- Simple web interface showing database stats and image gallery

## Quick Start

### Option 1: Full Docker Setup (Recommended)

1. Place your images in the `images/` folder
2. Run the startup script:
   - **Linux/macOS**: `./start.sh`
   - **Windows**: `start.bat`
3. Open http://localhost:8000 in your browser
4. Click "Scan for New Images" to populate the database
5. Click "Load Images" to view your photo collection

### Option 2: Local Development

For local development (Python app runs locally, database in Docker):

1. Place your images in the `images/` folder
2. Run the local startup script:
   - **Linux/macOS**: `./start-local.sh`
   - **Windows**: `start-local.bat`
3. Open http://localhost:8000 in your browser
4. Click "Scan for New Images" to populate the database
5. Click "Load Images" to view your photo collection

To stop the local database:
- **Linux/macOS**: `./stop-local.sh`
- **Windows**: `stop-local.bat`

### Manual Setup

Alternatively, you can start manually:
```bash
docker compose up --build
```

## API Endpoints

- `GET /` - Serves the frontend application
- `GET /api/images/count` - Returns count of images in database
- `POST /api/images/scan` - Scans images folder and adds new images to database
- `GET /api/images` - Returns all images with metadata

## Database Schema

The `images` table stores:
- Basic file info (filename, path, size)
- Image dimensions and format
- Creation/modification dates
- EXIF metadata (JSON)
- Tags and location data (for future features)