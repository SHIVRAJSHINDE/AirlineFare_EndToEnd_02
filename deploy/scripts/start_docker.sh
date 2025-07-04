#!/bin/bash

# Authenticate Docker to the AWS ECR registry - Authentication
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 905418096737.dkr.ecr.ap-south-1.amazonaws.com

# Pull the latest Docker image from your ECR repository - Pull Docker
docker pull 905418096737.dkr.ecr.ap-south-1.amazonaws.com/new_ecr:latest

# Stop and remove the old container (if any)
sudo docker stop new_ecr || true
sudo docker rm new_ecr || true

# Run the new Docker container
docker run -d -p 80:5000 -e DAGSHUB_PAT=c7739af80dc00d48cfbd465104124cf4ecd96802 --name new_ecr 905418096737.dkr.ecr.ap-south-1.amazonaws.com/new_ecr:latest


