# SellAiArt Image Generation Microservice

This repository contains the image generation microservice for the Sellaiart SaaS platform (see the main [Sellaiart repo](https://github.com/yogesh-bhandare/sellaiart) for project details). It integrates with the Sellaiart ecosystem and provides a scalable, serverless solution for generating AI-powered images using a customized tech stack.

The microservice leverages generative AI models to create personalized images, utilizing tools like Replicate for model training and Upstash for caching, rate limiting, and async task scheduling.

---

## Tech Stack

- **[Python 3.13](https://github.com/python)** - Core programming language.
- **[FastAPI](https://github.com/django/django)** (`pip install "FastAPI>=0.112.0,<0.113.0"`) - Web framework for building the microservice.
- **[Upstash](https://upstash.com)** - Serverless Redis for caching, QStash for async endpoint scheduling, and rate limiting.
- **[Replicate](https://replicate.com)** - Platform to train and run generative AI models (e.g., fine-tuned with your face).
- **[Python Requests](https://github.com/psf/requests)** (`pip install requests`) - HTTP library for API interactions.
- **[Jupyter](https://jupyter.org/)** (`pip install jupyter`) - For experimentation and prototyping.
- **[Python Decouple](https://github.com/HBNetwork/python-decouple)** - Loads environment variables from `.env` files with type casting and defaults.
- **[ostris/flux-dev-lora-trainer](https://replicate.com/ostris/flux-dev-lora-trainer)** - Pre-trained model for fine-tuning FLUX with custom images.

---

## Getting Started

### Prerequisites

Download and install the following tools:
- **[Git](https://git-scm.com/)** - Version control system.
- **[VSCode](https://code.visualstudio.com/)** (or **[Cursor](https://cursor.com/)**) - Recommended IDEs.
- **[Python](https://www.python.org/downloads/)** - Ensure Python 3.13 is installed.

### Setup Instructions

1. **Open a Terminal**
   Use Terminal, VSCode Terminal, Cursor Terminal, PowerShell, or any command-line interface.

2. **Clone the Repository**
   ```bash
   mkdir -p ~/dev/sellaiart-microservice
   cd ~/dev/sellaiart-microservice
   git clone https://github.com/yourusername/sellaiart-microservice .
