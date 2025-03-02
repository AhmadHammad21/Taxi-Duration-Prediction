FROM python:3.9-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project
COPY . .

# Expose the port
EXPOSE 8000

# Run the API
CMD ["uvicorn", "deployment.api.app:app", "--host", "0.0.0.0", "--port", "8000"]