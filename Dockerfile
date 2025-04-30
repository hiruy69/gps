# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the script
COPY rabbit_mq_publisher.py .
COPY requirments.txt .
RUN pip install --no-cache-dir -r requirments.txt
COPY gps.py .

# Expose the TCP listening port
EXPOSE 5151

# Run the listener script
CMD ["python", "gps.py"]
