# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# -------------------------------------------------------------------
# IMPORTANT: Install system libraries for Image Processing (OpenCV)
# Without these, YOLO will crash inside Docker
# -------------------------------------------------------------------
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*


# Copy requirements and install
COPY requirements.txt .
# Install dependencies (using CPU versions for torch to save space/time)
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Copy the project code
COPY . .

# Expose port 8000 for Django
EXPOSE 8000

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]