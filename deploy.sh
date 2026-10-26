#!/bin/bash

set -e

# EC2 configuration
EC2_USER="ec2-user"
EC2_HOST="18.134.226.124"
KEY_PATH="/Users/nobellimbu/.ssh/nobellimbu-ec2-keypair.pem"

# App configuration
APP_DIR="/home/ec2-user/book_store"
IMAGE_NAME="book_store"
CONTAINER_NAME="book_store"

echo "Copying updated files to EC2..."

scp -i "$KEY_PATH" \
    app.py \
    database_connection.py \
    book_repository.py \
    "$EC2_USER@$EC2_HOST:$APP_DIR/"

echo "Connecting to EC2 and redeploying..."

ssh -i "$KEY_PATH" "$EC2_USER@$EC2_HOST" << 'EOF'

set -e

cd /home/ec2-user/book_store

echo "Building new Docker image..."
docker build -t book_store:latest .

echo "Stopping old container..."
docker stop book_store || true

echo "Removing old container..."
docker rm book_store || true

echo "Starting new container..."
docker run -d \
    --name book_store \
    -p 5000:5000 \
    -e DATABASE_NAME=book_store \
    --restart unless-stopped \
    book_store:latest

echo "Checking running containers..."
docker ps

EOF

echo "Deployment completed!"