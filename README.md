# 👁️ Eye Cancer Detection System

**A Full-Stack, AI-Powered Platform for Ocular Disease Screening**

🔬🧠 AI-powered tool for classifying eye images using deep learning (ResNet50) and a three-tier architecture for modern, scalable deployment.

---

## ✨ Project Overview

This project implements an end-to-end medical screening application combining a modern web frontend, a robust Node.js API, and a dedicated Python service hosting the diagnostic AI model.

### 🧬 Architectural Components

The system is split into three independent services that communicate via REST APIs:

| Component | Technology | Role | Port | Directory |
| :--- | :--- | :--- | :--- | :--- |
| **Client** | **React, Vite, Tailwind CSS** | User interface for patient intake, image upload, and result presentation. | `5173` | `Client/` |
| **Server** | **Node.js, Express, Mongoose** | API Gateway, handles database persistence (MongoDB), and directs image files to the AI Model. | `3001` | `Server/` |
| **AI Model** | **Python, FastAPI, TensorFlow** | Hosts the pre-trained ResNet50 classifier to provide predictions. | `8000` | `AI-Model/` |

---

## 🧠 About the AI Model

The diagnostic core uses a **Transfer Learning** approach based on one of the most powerful CNN architectures.

* **Architecture:** Fine-tuned **ResNet-50**.
* **Task:** Binary Classification (Normal/Healthy vs. Disease/Abnormal).
* **Preprocessing:** Implements ResNet-specific image preprocessing, resizing images to $224 \times 224$ pixels.
* **Model Status (Crucial Note):** The trained model file, **`best_eye_cancer_model.h5`**, is not included in this repository due to GitHub's file size limits (100 MB). **You must obtain this file separately and place it in the `AI-Model` directory before running the Python service.**

---

## 🛠️ Installation and Setup

You need **Node.js** (for Client/Server) and **Python** (for AI Model) installed.

### 1. Database and Environment Setup

1.  Ensure **MongoDB** is running locally (default expected URI: `mongodb://localhost:27017/eyeCancerDB`).
2.  Verify your MongoDB connection URI in `Server/.env`.

### 2. Backend Service Setup

Install dependencies for the Node.js Express server.

```bash
# Navigate to the server folder
cd EyeCancer/Server

# Install Node dependencies (Express, Mongoose, etc.)
npm install
