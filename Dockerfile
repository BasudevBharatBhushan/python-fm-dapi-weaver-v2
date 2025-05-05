# Use a lightweight Python base image
FROM python:3.9-slim

# Set the project directory 
WORKDIR /python-fm-api

# Copy the requirements file 
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire  code
COPY . .

# Expose the port 
EXPOSE 8000


# run the application 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]



