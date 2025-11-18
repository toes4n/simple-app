# Use build platform for dependencies
FROM --platform=$BUILDPLATFORM python:3.11-slim AS build

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Final multi-platform stage
FROM python:3.11-slim

WORKDIR /app

COPY --from=build /app /app
COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

EXPOSE 5000

CMD ["python", "app.py"]
