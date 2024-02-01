FROM python:3.9-slim

# Set a working directory
WORKDIR /usr/src/app

# Install dependencies
# Copying the requirements file separately allows Docker to cache the installed
# dependencies between builds if the requirements file hasn't changed
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code
COPY . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Expose the port the app runs on
EXPOSE 80

# Create a non-root user and change ownership of the app files
RUN useradd appuser && chown -R appuser /usr/src/app
USER appuser

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
