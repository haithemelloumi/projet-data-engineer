FROM python:3.11-slim

# Create a folder in the container
WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir pandas

# Copy necessary files
COPY . .

# Command to run when container starts
CMD ["sh", "-c", "python create_db.py && python insert_data.py"]