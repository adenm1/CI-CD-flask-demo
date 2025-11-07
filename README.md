# CI/CD Flask DEMO 🚀

This project is a minimal **Flask web application** containerized with **Docker** and redy for a simple **CI/CD pipline** deployment using GitHub Actions.

---
## 🧠 Overview

The purpose of this demo is to show how to:
- Build and run a Flask app inside a Docker container
- Expose the service on port **8000**
- Prepare for continuous deployment to a remote server (e.g., Google cloud Ubuntu VPS)

---

## 🏗️ Project Structure
```
.
├── app.py
├── Dockerfile
├── README.md
└── requirements.txt
```

---
## ⚙️ How to Build & Run (Local)

### 1️⃣ Build the Docker image

```bash
docker build -t ci-cd-demo:local .
```

### 2️⃣Run the container
```
docker run --rm -p 8000:8000 ci-cd-demo:local
```

Now open your browser and visit:
```http request
http://127.0.0.1:8000
```

You Should see:
    Hello, Siyng's - CI/CD pipline v1 (Dockerized)!


---


🧰 Requirements
- Python 3.11+
- Docker Engine 24+
- GitHub account for CI/CD setup

---

🚀 Next Steps
s