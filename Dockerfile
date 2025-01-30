# Use an official lightweight Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Google Cloud Run uses
EXPOSE 8080

# Command to run the Flask app using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
