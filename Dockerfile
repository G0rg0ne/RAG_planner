FROM python:3.10.10

# Create workdir and set it as the working directory
RUN mkdir -p /workdir
WORKDIR /workdir

# Install system dependencies
RUN apt-get update -qy \
    && apt-get install -y apt-utils gosu make

# Copy all files first so that Makefile can handle everything
COPY . /workdir

# Install Python dependencies via Makefile
RUN make install

EXPOSE 8501