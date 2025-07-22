FROM python:3.13-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY vanilla/ ./vanilla/
COPY images/ ./images/

EXPOSE 8000

CMD ["python", "backend/main.py"]