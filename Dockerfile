# What This Step Does
# Defines:
#     Python environment
#     dependencies
#     runtime configuration
# This becomes the blueprint for all PulsePay containers.

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# WHAT THIS DOES:
# Instruction	    Purpose
# FROM	            Base Python image
# WORKDIR	        Container working directory
# COPY requirements	Copy dependencies
# RUN pip install	Install packages
# COPY . .	        Copy project files
# EXPOSE 8000	    Open FastAPI port   