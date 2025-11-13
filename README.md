# 👁️ Eye Cancer Detection System

### A Full-Stack Machine Learning Platform for Ocular Disease Screening

---

## 🔬 Overview

The **Eye Cancer Detection System** is a full-stack web application designed to detect ocular diseases using Deep Learning.
It integrates a **ResNet50** model within a **three-tier microservice architecture**, ensuring modularity, scalability, and security.

---

## ✨ Features

* **Secure Patient Intake**
  Captures and validates essential patient demographic and medical information through a React-based form.

* **Machine Learning Diagnostics**
  Utilizes a **Keras ResNet50** model hosted on a dedicated Python FastAPI service for binary classification (*Normal / Disease*).

* **Historical Data Persistence**
  Stores all patient records (`User`) and scan results (`PredictionResult`) in **MongoDB** using **Mongoose ORM**.

* **API Gateway**
  The **Node.js Express** backend manages data flow, file uploads, and communication between the client, database, and ML service.

* **Modern UI**
  Built with **React (Vite)** and styled with **Tailwind CSS** for a clean, responsive user interface.

---

## 🔬 Model Performance & Validation

The model was trained using a professional, two-phase **transfer learning** approach.
The complete training notebook (`model_train.ipynb`) is included in this repository.

### Final Evaluation on 100-Sample Test Set

| Class        |  Precision | Recall | F1-Score | Support |
| :----------- | :--------: | :----: | :------: | :-----: |
| 0 (Normal)   |   1.0000   | 1.0000 |  1.0000  |    21   |
| 1 (Disease)  |   1.0000   | 1.0000 |  1.0000  |    79   |
| **Accuracy** | **1.0000** |        |          | **100** |

**Confusion Matrix:**

```
[[21  0]
 [ 0 79]]

(True Negatives: 21, False Positives: 0)
(False Negatives: 0, True Positives: 79)
```

---

## 💻 Architecture & Tech Stack

The project is divided into three independent services:

| Component    | Technology        | Core Libraries                             | Port | Directory   |
| :----------- | :---------------- | :----------------------------------------- | :--: | :---------- |
| **Client**   | React (Vite)      | `react-router-dom`, `axios`, `tailwindcss` | 5173 | `Client/`   |
| **Server**   | Node.js (Express) | `mongoose`, `multer`, `axios`, `dotenv`    | 3001 | `Server/`   |
| **ML Model** | Python (FastAPI)  | `tensorflow`, `numpy`, `uvicorn`           | 8000 | `AI-Model/` |

---

## ⚠️ Critical Setup Requirement — ML Model Access

The trained ML model file `best_eye_cancer_model.h5` is **required** for the AI Model service to function.
Due to its large size, it is not uploaded to GitHub.

📩 **To request access:** [adithyayadav641@gmail.com](mailto:adithyayadav641@gmail.com)
Alternatively, you can **re-train** the model using the included notebook (`model_train.ipynb`).

---

## 🛠️ Installation and Setup

### Prerequisites

* **Node.js** (v18 or higher)
* **Python** (v3.8 or higher)
* **MongoDB** (URI configured in `Server/.env`)

---

### 1️⃣ AI Model Service Setup (`AI-Model/`)

```bash
cd EyeCancer/AI-Model
pip install tensorflow numpy fastapi uvicorn python-multipart pillow
```

**Action Required:**
Place `best_eye_cancer_model.h5` inside this directory,
or re-train it using `model_train.ipynb`.

---

### 2️⃣ Backend Server Setup (`Server/`)

```bash
cd EyeCancer/Server
npm install
```

Ensure your MongoDB connection string is correctly configured in `.env`.

---

### 3️⃣ Frontend Client Setup (`Client/`)

```bash
cd EyeCancer/Client
npm install
```

---

## ▶️ Quick Start

Run all three services in **separate terminal windows** for the system to function end-to-end.

**Terminal 1 – Start AI Model Server (Port 8000)**

```bash
cd EyeCancer/AI-Model
python main.py
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

Access the application at:
👉 **[http://localhost:5173](http://localhost:5173)**

---

## 📄 Publication

This project has been published as part of an academic and applied research initiative.
You can read the full paper here:
🔗 [**An Integrated Three-Tier Microservice Architecture for Deploying State-of-the-Art Ocular Cancer Detection Models**](https://doi.org/10.5281/zenodo.17603497)

---

## 🐛 Bugs and Support

For any issues, questions, or model file access requests:

* 📧 **Email:** [adithyayadav641@gmail.com](mailto:adithyayadav641@gmail.com)
* 🐛 **Issues:** [GitHub Issues](https://github.com/AR-47/EyeCancer/issues)
---
