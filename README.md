# 👁️ Eye Cancer Detection System

This project implements a full-stack, AI-driven application for the automated screening and detection of eye abnormalities associated with cancer. It follows a **three-tier architecture** using React for the frontend, Node.js/Express for the backend, and a Python FastAPI service for machine learning inference.

## ✨ Key Features

* **Patient Intake Form:** Collects and validates essential patient demographic and medical history.
* **AI-Driven Analysis:** Sends uploaded fundus images to a dedicated AI service hosting a **ResNet50 model** for classification.
* **Persistent Data:** Patient records (`User`) and historical scan results (`PredictionResult`) are stored and linked in **MongoDB**.
* **Patient History Lookup:** Allows medical staff to securely retrieve a patient's full history and past scan data using a unique Patient ID.
* **Modern Stack:** Built using React, Tailwind CSS, Node.js (Express), and Python (FastAPI/TensorFlow).

## 💻 Architecture & Tech Stack

| Service | Technology | Role | Port | Directory |
| :--- | :--- | :--- | :--- | :--- |
| **Client** | **React, Vite, Tailwind CSS** | User Interface for data entry and results display. | `http://localhost:5173` | `Eye-Cancer/Client` |
| **Server** | **Node.js, Express, Mongoose** | API Gateway, handles database operations, and routes requests to the AI Model. | `http://localhost:3001` | `Eye-Cancer/Server` |
| **AI-Model** | **Python, FastAPI, TensorFlow** | Image preprocessing, hosts the machine learning classification model. | `http://localhost:8000` | `Eye-Cancer/AI-Model` |

---

## 🛠️ Setup and Installation

### Prerequisites

You must have the following installed on your system:

1.  **Node.js** (v18+)
2.  **Python** (v3.8+)
3.  **MongoDB** (running locally or accessible via a cloud URI)
4.  **Git LFS** (Recommended for downloading/storing the model file)

### Step 1: Clone the Repository and Obtain the Model

Since the model file (`best_eye_cancer_model.h5`) is missing from the repository, you **must** obtain or recreate it.

1.  **Obtain the Model File:**
    * **Option A (Recommended):** If the model is tracked via Git LFS on the source platform, run:
        ```bash
        git lfs pull
        ```
    * **Option B (Manual):** Download the `best_eye_cancer_model.h5` file (size ~170MB) separately and place it inside the `Eye-Cancer/AI-Model` directory. *The Python service will not run without this file.*

### Step 2: Configure the Backend Server

1.  Navigate to the Server directory:
    ```bash
    cd Eye-Cancer/Server
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Ensure your `.env` file contains the MongoDB URI:
    ```env
    MONGO_URI=<Your MongoDB Connection String>
    PORT=3001
    ```

### Step 3: Set up the AI Model Service

1.  Navigate to the AI directory:
    ```bash
    cd Eye-Cancer/AI-Model
    ```
2.  Install Python dependencies (using a virtual environment is recommended):
    ```bash
    pip install tensorflow numpy fastapi uvicorn python-multipart pillow
    ```

### Step 4: Configure the Frontend Client

1.  Navigate to the Client directory:
    ```bash
    cd Eye-Cancer/Client
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```

---

## ▶️ Running the Application

You must run all three services concurrently in separate terminal windows.

### 1. Start the AI Model Service (Terminal 1)

```bash
cd Eye-Cancer/AI-Model
python main.py
