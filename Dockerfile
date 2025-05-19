FROM python:3.9-slim

WORKDIR /app

# Don't use requirements.txt initially - install packages directly
RUN pip install --no-cache-dir flask==2.0.1 werkzeug==2.0.1

# Copy your application code
COPY . .

# Expose the port
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
