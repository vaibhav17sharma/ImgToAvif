FROM python:3.11-slim

# Install dependencies
RUN pip install pillow pillow-avif-plugin

# Set working directory
WORKDIR /images

# Copy conversion script
COPY convert.py /convert.py

# Default command
CMD ["python", "/convert.py"]
