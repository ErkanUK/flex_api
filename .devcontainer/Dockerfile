# Use a stable base image that works well with Codespaces
FROM mcr.microsoft.com/vscode/devcontainers/base:ubuntu-22.04

# Avoid prompts during package installation
ARG DEBIAN_FRONTEND=noninteractive

# Install Node.js (LTS) and Python
RUN apt-get update && \
    apt-get install -y curl ca-certificates git python3 python3-pip build-essential && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g http-server @stoplight/spectral-cli redoc-cli && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create a non-root user (vscode is expected by Codespaces)
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
  && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
  && apt-get update \
  && apt-get install -y sudo \
  && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME \
  && chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME
WORKDIR /workspace