import express from 'express';
import multer from 'multer';
import cors from 'cors';
import axios from 'axios';
import FormData from 'form-data';
import dotenv from 'dotenv'
import connectDB from './database/connect.js'
import userRoutes from './routes/userRoutes.js';
import patientRoutes from './routes/patientRoutes.js'
import User from './models/User.js';
import PredictionResult from './models/PredictionResult.js';

dotenv.config()

const app = express();
const port = process.env.PORT || 3001;

connectDB();

// Middleware
app.use(cors());
app.use(express.json());
app.use('/api/users', userRoutes);
app.use('/api/patients' , patientRoutes)

// Multer for file upload
const upload = multer({ storage: multer.memoryStorage() });

// Accept one image at a time with field name 'file'
app.post('/analyze', upload.single('file'), async (req, res) => {
  try {
    const { patientId } = req.query;
    const file = req.file;

    if (!file || !patientId) {
      return res.status(400).json({ success: false, message: 'Missing file or patientId' });
    }

    // Find the user by patientId
    const user = await User.findOne({ patientId });
    if (!user) {
      return res.status(404).json({ success: false, message: 'User not found with given patientId' });
    }

    // Send image to FastAPI for prediction
    const formData = new FormData();
    formData.append('file', file.buffer, {
      filename: file.originalname,
      contentType: file.mimetype,
    });

    // CRITICAL: Ensure the response structure is handled carefully
    const response = await axios.post('http://localhost:8000/predict', formData, {
      headers: formData.getHeaders(),
    });

    const aiResult  = response.data;

    console.log('Saving prediction result:', aiResult);

    // 🛑 CRITICAL FIX: Explicitly map FastAPI keys to Mongoose schema keys
    const dbPayload = {
        classification_prediction: aiResult.prediction_class === 'Disease/Abnormal' ? 1 : 0, 
        
        classification_probabilities: [aiResult.probability_score], 
        
        original_image_base64: aiResult.original_image_base64,
        overlay_image_base64: aiResult.overlay_image_base64,
        segmentation_mask_base64: aiResult.segmentation_mask_base64,
        segmentation_shape: aiResult.segmentation_shape,
        message: aiResult.message,
    };
   
    // Save the correctly mapped result to DB
    const savedResult = await PredictionResult.create(dbPayload);

    // Add result to user's predictionResults
    user.predictionResults.push(savedResult._id);
    await user.save();

    // Return updated user with populated predictionResults
    const updatedUser = await User.findById(user._id).populate('predictionResults');

    res.status(200).json({
      success: true,
      message: 'Prediction successful and saved',
      result: savedResult,
      user: updatedUser,
    });

  } catch (error) {
    console.error('Error in /analyze:', error.message);
    
    // --- START OF CRITICAL ERROR HANDLING FIX ---
    if (error.response) {
        const statusCode = error.response.status;
        const aiError = error.response.data;

        if (statusCode >= 400 && statusCode < 500) {
            return res.status(statusCode).json({ 
                success: false, 
                message: aiError.message || 'Client-side issue detected by AI service.',
                details: aiError 
            });
        }
    }

    // Default to a 500 server error for all other unhandled issues
    res.status(500).json({ success: false, message: 'Internal server error during analysis.' });
  }
});

app.listen(port, () => {
    console.log(`🚀 Server listening on http://localhost:${port}`);
});
