import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import DepthwiseConv2D
from tensorflow.keras.applications.efficientnet_v2 import preprocess_input
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import io
import numpy as np
import base64
import os
import sys

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Configuration ---
MODEL_PATH = "best_finetuned.h5"
IMG_SIZE = (224, 224)

# --- Global Model Variable ---
model = None

# --- Fix for 'DepthwiseConv2D' Error ---
class FixedDepthwiseConv2D(DepthwiseConv2D):
    def __init__(self, **kwargs):
        kwargs.pop('groups', None)
        super().__init__(**kwargs)

# --- Load Model at Startup ---
print(f"Current Working Directory: {os.getcwd()}")
if os.path.exists(MODEL_PATH):
    print(f"Found model file at: {MODEL_PATH}")
    try:
        model = load_model(
            MODEL_PATH, 
            compile=False, 
            custom_objects={'DepthwiseConv2D': FixedDepthwiseConv2D}
        )
        print("✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading Keras model: {e}")
else:
    print(f"❌ CRITICAL ERROR: Model file '{MODEL_PATH}' not found!")
    print(f"Please move 'best_finetuned.h5' into the folder: {os.getcwd()}")

def preprocess_image(image: Image.Image):
    """Preprocess the image to match training conditions (EfficientNetV2)"""
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    image = image.resize(IMG_SIZE)
    img_array = np.array(image)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array

def image_to_base64(image: Image.Image) -> str:
    """Helper to convert PIL Image to Base64 string"""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

@app.post("/analyze")
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    global model
    
    if model is None:
        return JSONResponse(
            status_code=500, 
            content={"error": "Model not loaded. Check server terminal."}
        )

    try:
        # 1. Read and Process Image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        processed_img = preprocess_image(image)
        
        # 2. Predict
        raw_score = model.predict(processed_img, verbose=0)[0][0]
        
        # --- FIX: INVERTING LOGIC ---
        # Since folders were likely alphabetical: 0=Cancer, 1=Non_Cancer
        # The model outputs the probability of Class 1 (Non-Cancer).
        
        non_cancer_prob = float(raw_score)
        cancer_prob = 1.0 - non_cancer_prob
        
        # If Cancer probability is higher (>0.5), predict Cancer (1)
        classification_pred = 1 if cancer_prob >= 0.5 else 0
        
        # Order: [Prob(Non-Cancer), Prob(Cancer)]
        classification_probabilities = [non_cancer_prob, cancer_prob]
        
        print(f"Raw Score (Non-Cancer Prob): {raw_score:.4f}")
        print(f"Calculated Cancer Prob: {cancer_prob:.4f} -> Prediction: {'Cancer' if classification_pred == 1 else 'Non-Cancer'}")

        # 3. Output Formatting
        display_image = image.resize((256, 256))
        display_base64 = image_to_base64(display_image)

        return JSONResponse(content={
            "classification_prediction": classification_pred,
            "classification_probabilities": classification_probabilities,
            "segmentation_shape": [224, 224],
            "segmentation_mask_base64": display_base64,
            "original_image_base64": display_base64,
            "overlay_image_base64": display_base64,
            "message": "Prediction successful"
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/")
async def root():
    status = "Model Ready" if model else "Model NOT Loaded"
    return {"message": f"TensorFlow API Running. Status: {status}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)