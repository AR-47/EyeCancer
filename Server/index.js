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

app.use(cors());
app.use(express.json());
app.use('/api/users', userRoutes);
app.use('/api/patients' , patientRoutes)

const upload = multer({ storage: multer.memoryStorage() });

app.post('/analyze', upload.single('file'), async (req, res) => {
  try {
    const { patientId } = req.query;
    const file = req.file;

    if (!file || !patientId) {
      return res.status(400).json({ success: false, message: 'Missing file or patientId' });
    }

    const user = await User.findOne({ patientId });
    if (!user) {
      return res.status(404).json({ success: false, message: 'User not found with given patientId' });
    }

    const formData = new FormData();
    formData.append('file', file.buffer, {
      filename: file.originalname,
      contentType: file.mimetype,
    });

    const response = await axios.post('http://localhost:8000/predict', formData, {
      headers: formData.getHeaders(),
    });

    const result  = response.data;

     console.log('Saving prediction result:', response.data);

   
    const savedResult = await PredictionResult.create(result);
ts
    user.predictionResults.push(savedResult._id);
    await user.save();

    const updatedUser = await User.findById(user._id).populate('predictionResults');

    res.status(200).json({
      success: true,
      message: 'Prediction successful and saved',
      result: savedResult,
      user: updatedUser,
    });

  } catch (error) {
    console.error('Error in /analyze:', error.message);
    res.status(500).json({ success: false, error: error.message });
  }
});

