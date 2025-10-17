# 👁️ Eye Cancer Detection System

**A Full-Stack, Machine Learning Platform for Ocular Disease Screening**

🔬🧠 This system uses a **Deep Learning (ML)** model to classify eye images, integrated within a modern three-tier microservice architecture.

-----

## ✨ Project Features

  * **Secure Patient Intake:** Captures and validates essential patient demographic and medical history through a dedicated **React** form.
  * **Machine Learning Diagnostics:** Employs a **TensorFlow/Keras ResNet50 model** hosted on a dedicated Python service for binary classification (Normal/Disease).
  * **Historical Data Persistence:** Patient records (`User`) and all associated scan results (`PredictionResult`) are stored and linked in a **MongoDB** database using Mongoose.
  * **API Gateway:** The Node.js Express server manages secure data flow, handling file uploads and routing requests between the client, database, and ML service.
  * **Modern Interface:** Built with **React** and styled using **Tailwind CSS** for a clean, responsive web application.

-----

## 💻 Architecture & Tech Stack

The application is structured into three distinct services:

| Component | Technology | Core Libraries | Port | Directory |
| :--- | :--- | :--- | :--- | :--- |
| **Client** | **React, Vite** | `react-router-dom`, `axios`, `tailwindcss` | `5173` | `Client/` |
| **Server** | **Node.js, Express** | `mongoose`, `multer`, `axios`, `dotenv` | `3001` | `Server/` |
| **ML Model** | **Python, FastAPI** | `tensorflow`, `numpy`, `uvicorn` | `8000` | `AI-Model/` |

-----

## ⚠️ Critical Setup Requirement (ML Model Access)

The trained machine learning model file (`best_eye_cancer_model.h5`) is **essential** for the AI Model service to start and perform diagnostics.

The file is too large to be uploaded to GitHub. **If you need access to the model file, please contact the author via email.**

-----

## 🛠️ Installation and Setup

### Prerequisites

  * **Node.js** (v18+)
  * **Python** (v3.8+)
  * **MongoDB** (accessible via the URI in `Server/.env`)

### 1\. AI Model Service Setup (`AI-Model/`)

1.  Navigate to the AI Model directory:
    ```bash
    cd EyeCancer/AI-Model
    ```
2.  Install Python dependencies:
    ```bash
    pip install tensorflow numpy fastapi uvicorn python-multipart pillow
    ```
3.  **Action Required:** Place the **`best_eye_cancer_model.h5`** file inside this directory.

### 2\. Backend Server Setup (`Server/`)

1.  Navigate to the Server directory:
    ```bash
    cd EyeCancer/Server
    npm install
    ```
2.  Ensure your MongoDB connection string is correctly configured in the `.env` file.

### 3\. Frontend Client Setup (`Client/`)

1.  Navigate to the Client directory:
    ```bash
    cd EyeCancer/Client
    npm install
    ```

-----

## ▶️ Quick Start (Running the Application)

Run all three services concurrently in separate terminal windows for the application to function end-to-end.

### Terminal 1: Start AI Model Server (Port 8000)

```bash
cd EyeCancer/AI-Model
python main.py
```

### Terminal 2: Start Backend API Server (Port 3001)

```bash
cd EyeCancer/Server
npm start
```

### Terminal 3: Start Frontend Client (Port 5173)

```bash
cd EyeCancer/Client
npm run dev
```

The application will be live at `http://localhost:5173`.

-----

## 🤝 Support

For questions, issues, or to request access to the trained model file:

📧 **Email:** adithyayadav641@gmail.com
🐛 **Issues:** [GitHub Issues](https://www.google.com/search?q=https://github.com/AR-47/EyeCancer/issues)

```
```
