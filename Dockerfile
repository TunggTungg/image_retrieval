# Stage 1: Build stage
FROM python:3.10-slim AS build-stage

# Install required packages using apt
RUN apt-get update && \
    apt-get install -y libgl1 curl && \
    rm -rf /var/lib/apt/lists/*

# Install UV
ADD --chmod=755 https://astral.sh/uv/install.sh /install.sh
RUN /install.sh && rm /install.sh
COPY ./requirements.txt .
RUN /root/.cargo/bin/uv pip install --system --no-cache -r requirements.txt

# Stage 2: web stage
FROM python:3.10-slim as web-final 

# Install libgl1 from the build stage
COPY --from=build-stage /usr/lib/x86_64-linux-gnu /usr/lib/x86_64-linux-gnu
# Copy built Python libraries from the build stage
COPY --from=build-stage /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=build-stage /usr/local/bin/uvicorn /usr/local/bin/uvicorn
# Set the working directory
WORKDIR /app
