#!/bin/bash
echo "Starting AVIF Converter with Docker..."
docker-compose up --build -d
echo "AVIF Converter is running at http://localhost:8080"
echo "Press Ctrl+C to stop"
docker-compose logs -f