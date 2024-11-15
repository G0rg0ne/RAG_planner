# Use an NVIDIA CUDA base image with Python 3.10
FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

# Install Python 3.10 and necessary Python utilities
RUN apt-get update -qy && \
    apt-get install -y software-properties-common wget && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.10 python3.10-distutils && \
    ln -s /usr/bin/python3.10 /usr/bin/python

# Manually install pip and upgrade to the latest version
RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
    rm get-pip.py && \
    python -m pip install --upgrade pip

# Set the working directory
WORKDIR /workdir

# Install additional system dependencies
RUN apt-get update -qy && \
    apt-get install -y apt-utils gosu make

# Copy requirements.txt and install dependencies with --ignore-installed flag
COPY requirements.txt /workdir/requirements.txt
RUN python -m pip install --ignore-installed --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . /workdir


# Expose the application port
EXPOSE 8501
