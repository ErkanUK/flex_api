# Minimal, robust devcontainer Dockerfile for Codespaces
FROM mcr.microsoft.com/vscode/devcontainers/base:ubuntu-22.04

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG DEBIAN_FRONTEND=noninteractive

# Ensure apt works non-interactively and install runtime deps
# Added: openjdk-11-jre-headless, graphviz, unzip (for local PlantUML rendering)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates git python3 python3-pip build-essential sudo \
    openjdk-11-jre-headless graphviz unzip \
  && rm -rf /var/lib/apt/lists/*

# (Optional) Install plantuml jar for CLI usage and provide a small wrapper script
# This is useful for CLI rendering or for extensions that can call plantuml locally.
RUN mkdir -p /opt/plantuml && \
    curl -L -o /opt/plantuml/plantuml.jar https://github.com/plantuml/plantuml/releases/latest/download/plantuml.jar && \
    printf '#!/usr/bin/env bash\njava -jar /opt/plantuml/plantuml.jar "$@"' > /usr/local/bin/plantuml && \
    chmod +x /usr/local/bin/plantuml

# Create a non-root user with a home directory and sudo
RUN groupadd --gid $USER_GID $USERNAME || true \
  && useradd --uid $USER_UID --gid $USER_GID -m -s /bin/bash $USERNAME \
  && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME \
  && chmod 0440 /etc/sudoers.d/$USERNAME

# Ensure /home/codespace exists and is owned by the non-root user
RUN mkdir -p /home/codespace /home/vscode || true \
  && chown -R $USERNAME:$USERNAME /home/codespace /home/vscode

# Install global npm tools as the non-root user (optional)
USER $USERNAME
ENV HOME=/home/$USERNAME
WORKDIR /workspaces

# Install npm global tools without needing root (user-level)
RUN npm config set unsafe-perm true || true

# Switch back to root for any last-minute privileged steps (if needed)
USER root
# (no privileged commands here - keep ephemeral)

# Final switch to non-root user for Codespace
USER $USERNAME
WORKDIR /workspaces/${_WORKSPACE_FOLDER:-workspace}
