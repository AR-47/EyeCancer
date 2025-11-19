Based on the code changes identified in your files—specifically the switch to **EfficientNetV2**, the renamed model file (`best_finetuned.h5`), and the directory change from `AI-Model` to `Model`—here is the updated `README.md`.

````markdown
# 👁️ Eye Cancer Detection System

### A Full-Stack Machine Learning Platform for Ocular Disease Screening

---

## 🔬 Overview

The **Eye Cancer Detection System** is a full-stack web application designed to detect ocular diseases using state-of-the-art Deep Learning. It integrates an **EfficientNetV2** model within a **three-tier microservice architecture**, ensuring high accuracy, modularity, and scalability.

---

## ✨ Features

* **Secure Patient Intake**
    Captures and validates essential patient demographic and medical information through a comprehensive React-based form.

* **Advanced AI Diagnostics**
    Utilizes a **TensorFlow/Keras EfficientNetV2** model hosted on a high-performance **FastAPI** service for binary classification (*Normal / Disease*).

* **Historical Data Persistence**
    Stores all patient records (`User`) and diagnostic scan results (`PredictionResult`) in **MongoDB** using **Mongoose ORM** for easy retrieval and patient history tracking.

* **Robust API Gateway**
    The **Node.js Express** backend orchestrates data flow, handling secure image uploads via `Multer` and managing communication between the Client, Database, and AI Service.

* **Modern Responsive UI**
    Built with **React (Vite)** and styled with **Tailwind CSS**, providing a seamless experience across devices.

---

## 💻 Architecture & Tech Stack

The project is strictly divided into three independent microservices:

| Component | Technology | Core Libraries | Port | Directory |
| :--- | :--- | :--- | :--- | :--- |
| **Client** | React (Vite) | `react-router-dom`, `axios`, `tailwindcss` | **5173** | `Client/` |
| **Server** | Node.js (Express) | `mongoose`, `multer`, `axios`, `dotenv` | **3001** | `Server/` |
| **ML Model** | Python (FastAPI) | `tensorflow`, `efficientnet_v2`, `fastapi` | **8000** | `Model/` |

---

## ⚠️ Critical Setup Requirement — ML Model Access

The trained ML model file `best_finetuned.h5` is **required** for the AI Model service to function.

> **Note:** This file is large and is **not** included in the repository.

1.  **Obtain the Model:**
    * Request access via email: [adithyayadav641@gmail.com](mailto:adithyayadav641@gmail.com)
    * **OR** Re-train the model yourself using the provided notebook: `Model/model_train.ipynb` (or `model_test.ipynb`).

2.  **Placement:**
    You must place the `best_finetuned.h5` file directly inside the `Model/` directory.

---

## 🛠️ Installation and Setup

### Prerequisites

* **Node.js** (v18 or higher)
* **Python** (v3.9 or higher recommended)
* **MongoDB** (Local instance or Atlas URI)

---

### 1️⃣ AI Model Service Setup (`Model/`)

This service runs the Deep Learning inference engine.

```bash
cd EyeCancer/Model

# Install Python dependencies
pip install tensorflow numpy fastapi uvicorn python-multipart pillow

# ⚠️ IMPORTANT: Ensure 'best_finetuned.h5' is present in this folder
````

### 2️⃣ Backend Server Setup (`Server/`)

This service handles API requests and database connections.

```bash
cd EyeCancer/Server

# Install Node dependencies
npm install
```

**Configuration:**
Create a `.env` file in the `Server/` directory with your MongoDB credentials:

```env
PORT=3001
MONGO_URI=your_mongodb_connection_string_here
```

### 3️⃣ Frontend Client Setup (`Client/`)

This service runs the user interface.

```bash
cd EyeCancer/Client

# Install React dependencies
npm install
```

-----

## ▶️ Quick Start

Run all three services in **separate terminal windows** to start the full system.

**Terminal 1 – Start AI Model Server (Port 8000)**

```bash
cd EyeCancer/Model
# Uses uvicorn to serve the FastAPI app
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 – Start Backend API Server (Port 3001)**

```bash
cd EyeCancer/Server
npm start
```

**Terminal 3 – Start Frontend Client (Port 5173)**

```bash
cd EyeCancer/Client
npm run dev
```

👉 **Access the application at:** [http://localhost:5173](https://www.google.com/search?q=http://localhost:5173)

-----

## 📄 Publication

This project has been published as part of an academic and applied research initiative.
🔗 [**An Integrated Three-Tier Microservice Architecture for Deploying State-of-the-Art Ocular Cancer Detection Models**](https://doi.org/10.5281/zenodo.17603497)

-----

## 🐛 Bugs and Support

  * 📧 **Email:** [adithyayadav641@gmail.com](mailto:adithyayadav641@gmail.com)
  * 🐛 **Issues:** [GitHub Issues](https://github.com/AR-47/EyeCancer/issues)

<!-- end list -->

```

### Key Changes Made from Old Version:
1.  **Model Update:** Changed **ResNet50** to **EfficientNetV2** (derived from your imports in `app.py`).
2.  **File Name Update:** Updated the required model filename from `best_eye_cancer_model.h5` to `best_finetuned.h5` to match your Python configuration.
3.  **Directory Correction:** Changed references from `AI-Model/` to `Model/` to match your actual folder structure.
4.  **Launch Command:** Updated the Python launch command to use `uvicorn app:app` which is standard for FastAPI and matches your `app` instance name.
```
