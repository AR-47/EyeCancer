import tensorflow as tf
from tensorflow.keras.applications.resnet50 import preprocess_input
import numpy as np
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import io
import base64 # <-- ADDED IMPORT

# --- 1. CONFIGURATION ---
MODEL_FILE_PATH = 'best_eye_cancer_model.h5' # Your saved Keras model file
IMG_SIZE = 224
CLASS_NAMES = ['Normal/Healthy', 'Disease/Abnormal']

app = FastAPI()

# CORS middleware for development/frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. LOAD MODEL ON STARTUP ---
try:
    # Load the model you trained
    model = tf.keras.models.load_model(MODEL_FILE_PATH)
    print(f"TensorFlow model loaded successfully from {MODEL_FILE_PATH}")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None # Set model to None if loading fails

# --- 3. PREPROCESSING FUNCTION ---
def preprocess_image_tf(image: Image.Image):
    """
    Preprocesses a PIL image for input into the ResNet50 model.
    """
    # Resize and convert to numpy array
    image = image.resize((IMG_SIZE, IMG_SIZE))
    img_array = tf.keras.preprocessing.image.img_to_array(image)
    
    # Add a batch dimension (1, 224, 224, 3)
    img_array = np.expand_dims(img_array, axis=0)
    
    # Apply ResNet-specific preprocessing
    img_array = preprocess_input(img_array)
    
    return img_array

# --- 4. PREDICTION ENDPOINT ---
@app.post("/predict")
async def predict_eye_status(file: UploadFile = File(...)):
    if model is None:
        return JSONResponse(status_code=500, content={"error": "Model failed to load on startup."})
    
    try:
        # Read file contents
        contents = await file.read()
        
        # --- NEW LOGIC: Encode Original Image to Base64 ---
        # The file contents (bytes) are the original image data
        original_image_base64_encoded = base64.b64encode(contents).decode('utf-8')
        # --------------------------------------------------
        
        # Open as PIL Image for preprocessing
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        
        # Preprocess the image
        input_tensor = preprocess_image_tf(image)
        
        # Make a prediction
        with tf.device('/cpu:0'): # Force CPU inference if needed, or remove for GPU
            prediction = model.predict(input_tensor)
            
        # The output is a probability (0 to 1) from the sigmoid activation
        probability_of_disease = prediction[0][0]
        
        # Determine the class (0 or 1)
        predicted_class_index = int(probability_of_disease > 0.5)
        predicted_class_name = CLASS_NAMES[predicted_class_index]
        
        return JSONResponse(content={
            "prediction_class": predicted_class_name,
            "probability_score": float(probability_of_disease),
            "message": "Classification successful",
            "original_image_base64": original_image_base64_encoded, # <-- ADDED
            # These are needed by the Node.js server, but set to empty for now
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