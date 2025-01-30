# Use a lightweight Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Run Flask app
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
