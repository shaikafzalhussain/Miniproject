# Build image for the Flask app
FROM python:3.9-slim

WORKDIR /app

# Copy and install dependencies
COPY app/requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install gunicorn

# Copy app source code
COPY app/ .

EXPOSE 5000

ENV FLASK_ENV=production

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--workers", "2"]
