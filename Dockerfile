# Dockerfile
FROM python:3.11-slim

# Create a folder in the the container

WORKDIR /app

# Copy the folders in the the container
COPY create_db.py .
COPY schema.sql .

COPY . .

# Launch container
# CMD ["python", "hello_world.py"]
CMD ["python", "create_db.py"]
CMD ["python", "fill_data.py"]
