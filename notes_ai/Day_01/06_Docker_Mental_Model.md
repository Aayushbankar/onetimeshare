# 06. Docker: The Mental Model

## "Why does it work on my machine but not the server?"
Before Docker, deploying software was a nightmare. You had to manually install Python, Redis, libraries, and ensure the versions matched exactly. If you had Python 3.10 locally but the server had 3.6, everything broke.

## What is Docker?
Docker is a tool that packages your code *and* its environment into a sealed box (Container).

### The Core Concepts
1.  **Image (The Blueprint/Recipe)**
    - An Image is a read-only template. It contains the OS (e.g., Slim Linux), the runtime (Python), libraries, and your code.
    - Think of it like a **Class** in programming.
    - Example: `python:3.13-slim` is a base image.

2.  **Container (The Running Instance)**
    - A Container is a running instance of an Image.
    - Think of it like an **Object** (instance of a class).
    - You can spin up 100 containers from 1 image. They are isolated from each other.

3.  **The Engine ( The Dock)**
    - The software running on your computer (or server) that manages these containers.

## Virtual Machines (VMs) vs. Docker
-   **VM**: Simulates a whole computer (hardware, kernel, OS, apps). Very heavy (GBs in size), slow to boot.
-   **Container**: Shares the host's Linux Kernel but isolates the "User Space" (files, processes). Very light (MBs), instant boot.

## The "Layer" System
Docker images are built significantly differently from normal files. They use **layers**.
-   Layer 1: The Base OS (Debian)
-   Layer 2: Added Python
-   Layer 3: Copied your `requirements.txt`
-   Layer 4: Installed dependencies
-   Layer 5: Copied your source code

**Caching Magic**: If you change your code (Layer 5), Docker *reuses* layers 1-4 without rebuilding them. This makes builds super fast.
