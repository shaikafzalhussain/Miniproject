# Use official lightweight Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy dependency file first (for Docker layer caching)
COPY app/requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY app/ .

# Expose the Flask/Gunicorn port
EXPOSE 5000

# Set environment variables
ENV FLASK_ENV=production \
    PYTHONUNBUFFERED=1

# Start the Flask app using Gunicorn WSGI server
# Ensure your app.py file has: app = Flask(__name__)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--workers", "2"]
