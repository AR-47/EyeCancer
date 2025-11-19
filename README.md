---

# 👁️ Eye Cancer Detection System

### A Full-Stack Machine Learning Platform for Ocular Disease Screening

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue" />
  <img src="https://img.shields.io/badge/Node.js-18+-green" />
  <img src="https://img.shields.io/badge/React-Vite-blue" />
  <img src="https://img.shields.io/badge/TensorFlow-2.x-orange" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-teal" />
  <img src="https://img.shields.io/badge/MongoDB-Database-brightgreen" />
</p>

---

## 🔬 Overview

The **Eye Cancer Detection System** is a microservice-based full-stack web platform designed to detect **ocular cancer** using **Deep Learning**.

It integrates:

* A **React + Tailwind** modern frontend
* A secure **Node.js/Express Gateway**
* A TensorFlow **EfficientNetV2** ML model exposed via **FastAPI**
* **MongoDB** for patient data & prediction history

This project aims to make early detection of eye cancer more accessible with a **fast, scalable, and accurate** system.

---

# 🏗️ Architecture

```
Client (React + Vite)
      |
      | Axios HTTP Requests
      v
Server (Node.js + Express)
      |
      | 1. Stores user info to MongoDB
      | 2. Sends image to Model API
      v
ML Model (FastAPI + TensorFlow)
      |
      v
Prediction Returned → Stored → Displayed to User
```

Each part runs independently as a **microservice**.

---

# ⚙️ Tech Stack

| Component    | Technology                                  | Port     | Directory |
| ------------ | ------------------------------------------- | -------- | --------- |
| **Client**   | React (Vite), Tailwind                      | **5173** | `/Client` |
| **Server**   | Node.js, Express, Mongoose, Multer          | **3001** | `/Server` |
| **ML Model** | Python, FastAPI, TensorFlow, EfficientNetV2 | **8000** | `/Model`  |

---

# 📁 Folder Structure

```
EyeCancer/
│── Client/               # React Frontend
│── Server/               # Node.js Backend Gateway
│── Model/                # ML Model API (FastAPI + TensorFlow)
│── README.md
```

---

# ⚠️ Required ML Model File

The model **best_finetuned.h5** is required for predictions.

### How to obtain:

📩 Email: **[adithyayadav641@gmail.com](mailto:adithyayadav641@gmail.com)**
or
🧠 Train it using the included notebooks:

```
Model/model_test.ipynb
```

### Place the model here:

```
Model/best_finetuned.h5
```

---

# 🛠️ Installation & Setup Guide

## 1️⃣ Clone the repository

```bash
git clone https://github.com/AR-47/EyeCancer.git
cd EyeCancer
```

---

# 🚀 Microservice Setup

---

## 2️⃣ Start the ML Model Service (`/Model`)

### Install dependencies:

```bash
cd Model
pip install tensorflow fastapi uvicorn numpy pillow python-multipart
```

### Start the model server:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The ML API will be available at:

```
http://localhost:8000/predict
```

---

## 3️⃣ Start the Backend Server (`/Server`)

### Install dependencies:

```bash
cd Server
npm install
```

### Configure environment variables

Create a `.env` file inside `/Server`:

```
MONGO_URI=your_mongodb_connection
PORT=3001
```

### Run the server:

```bash
npm start
```

Server will run on:

```
http://localhost:3001
```

---

## 4️⃣ Start the Frontend Client (`/Client`)

### Install dependencies:

```bash
cd Client
npm install
```

### Start the client:

```bash
npm run dev
```

Frontend will run on:

```
http://localhost:5173
```

---

# 📡 API Documentation (Server)

### **POST** `/upload`

Uploads eye image + patient details.

#### Body (multipart/form-data):

| Field     | Type   | Description     |
| --------- | ------ | --------------- |
| `image`   | File   | Eye scan image  |
| `name`    | String | Patient name    |
| `age`     | Number | Age             |
| `history` | String | Medical history |

#### Response:

```json
{
  "status": "success",
  "prediction": "Normal",
  "confidence": 0.92
}
```

---

### **POST** `/predict`

Server → ML model communication (handled automatically).
You don’t need to call this manually from frontend.

---

### **GET** `/history/:id`

Returns all previous predictions for a user.

---

# 🌟 Features Summary

### ✔ AI-based Ocular Cancer Detection

EfficientNetV2 model with FastAPI inference.

### ✔ Patient Record Management

MongoDB persistence of all predictions.

### ✔ Microservice Architecture

Independent ML, API Gateway, and Client.

### ✔ Modern UI

React + Vite + Tailwind.

### ✔ Secure Image Uploading

Multer middleware + backend validation.

---

# 🧪 Model Training

You can retrain the model using the Jupyter notebooks:

```
Model/model_train.ipynb
Model/model_test.ipynb
```

The dataset should be structured as:

```
data/
│── Normal/
│── Cancer/
```
---
# 📄 Research Publication

This project is supported by a peer-reviewed research paper published on Zenodo.

🔗 DOI: **[10.5281/ZENODO.17603497](https://zenodo.org/records/17603497)**
📘 Paper Title: **[An Integrated Three-Tier Microservice Architecture for Deploying State-of-the-Art Ocular Cancer Detection Models](https://zenodo.org/records/17603497)**
📅 Published: 2025

You can cite the paper when using this project in academic or research work.

---

# 🤝 Contributing

Pull requests are welcome!
You can also open issues for bugs and enhancements.

---

# 📜 License

This project is licensed under the **MIT License**.

---

# 📩 Contact

👤 **Adithya Yadav**
📧 Email: **[adithyayadav641@gmail.com](mailto:adithyayadav641@gmail.com)**
🔗 GitHub: **[https://github.com/AR-47](https://github.com/AR-47)**

---
