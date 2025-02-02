FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY ./app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . /app/

# Expose port
EXPOSE 8002

# Start the app with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
