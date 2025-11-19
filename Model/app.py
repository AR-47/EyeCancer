import tensorflow as tf
from tensorflow.keras.applications.resnet50 import preprocess_input
import numpy as np
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import io
import base64

# --- 1. CONFIGURATION ---
MODEL_FILE_PATH = 'best_eye_cancer_model.h5'
IMG_SIZE = 224
CLASS_NAMES = ['Normal/Healthy', 'Disease/Abnormal']

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. LOAD MODEL ON STARTUP ---
try:
    
    model = tf.keras.models.load_model(MODEL_FILE_PATH)
    print(f"TensorFlow model loaded successfully from {MODEL_FILE_PATH}")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None 

# --- 3. PREPROCESSING FUNCTION ---
def preprocess_image_tf(image: Image.Image):
    """
    Preprocesses a PIL image for input into the ResNet50 model.
    """
    image = image.resize((IMG_SIZE, IMG_SIZE))
    img_array = tf.keras.preprocessing.image.img_to_array(image)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array

# --- 4. PREDICTION ENDPOINT ---
@app.post("/predict")
async def predict_eye_status(file: UploadFile = File(...)):
    if model is None:
        return JSONResponse(status_code=500, content={"error": "Model failed to load on startup."})
    
    try:
        contents = await file.read()
        original_image_base64_encoded = base64.b64encode(contents).decode('utf-8')
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        width, height = image.size
        # Reject images where the aspect ratio deviates more than 40% from a square (1:1)
        if abs(width - height) / max(width, height) > 0.4:
            return JSONResponse(status_code=400, content={
                "prediction_class": "Error",
                "probability_score": 0.0,
                "message": "Image isn't of eyes, please upload the correct image",
                "original_image_base64": original_image_base64_encoded,
                "segmentation_mask_base64": "", 
                "overlay_image_base64": "",
                "segmentation_shape": [],
            })
        input_tensor = preprocess_image_tf(image)
        
        with tf.device('/cpu:0'):
            prediction = model.predict(input_tensor)
            
        probability_of_disease = prediction[0][0]
        predicted_class_index = int(probability_of_disease > 0.5)
        predicted_class_name = CLASS_NAMES[predicted_class_index]
        return JSONResponse(content={
            "prediction_class": predicted_class_name,
            "probability_score": float(probability_of_disease),
            "message": "Classification successful",
            "original_image_base64": original_image_base64_encoded,
            "segmentation_mask_base64": "", 
            "overlay_image_base64": "",
            "segmentation_shape": [],
        })
            
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/")
async def root():
    return {"message": "TensorFlow Eye Disease Classification Server is running"}

# --- 5. RUN THE SERVER ---
if __name__ == "__main__":
    import uvicorn
    # This runs the server on http://127.0.0.1:8000
    uvicorn.run(app, host="0.0.0.0", port=8000)