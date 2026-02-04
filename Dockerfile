# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# COPY only requirements first
COPY requirements.txt requirements.txt

# Install dependancies
RUN pip install -r requirements.txt

# Copy rest of the code
COPY . .

# Run your app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]