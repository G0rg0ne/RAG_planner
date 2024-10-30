# Use an NVIDIA CUDA base image with Python 3.10
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04

# Install Python 3.10 and necessary Python utilities
RUN apt-get update -qy && \
    apt-get install -y software-properties-common wget && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.10 python3.10-distutils && \
    ln -s /usr/bin/python3.10 /usr/bin/python

# Manually install pip and Poetry
RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
    rm get-pip.py && \
    python -m pip install poetry

# Set the working directory
WORKDIR /workdir

# Install additional system dependencies
RUN apt-get update -qy && \
    apt-get install -y apt-utils gosu make

# Copy all files to the container
COPY . /workdir

# Install project dependencies using Poetry before running the Makefile
RUN poetry install --no-cache

# Expose the application port
EXPOSE 8501

# Specify default command (if applicable, otherwise keep the entrypoint in your Makefile)
CMD ["make", "run"]